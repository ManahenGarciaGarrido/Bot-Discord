"""
Recommendation Engine - Motor de recomendaciones musicales inteligente
Sistema que aprende de los gustos del usuario y recomienda canciones similares
"""
import logging
from typing import List, Dict, Optional
import random

from .preferences_db import PreferencesDB
from .youtube_handler import YouTubeHandler


logger = logging.getLogger('MusicBot.Recommendations')


class RecommendationEngine:
    """
    Motor de recomendaciones que aprende de los gustos del usuario
    y genera sugerencias musicales personalizadas
    """

    def __init__(self, preferences_db: PreferencesDB, youtube: YouTubeHandler):
        self.prefs_db = preferences_db
        self.youtube = youtube

    async def get_recommendations(self, user_id: int, guild_id: int,
                                 count: int = 10) -> List[Dict]:
        """
        Obtener recomendaciones personalizadas basadas en gustos del usuario

        Args:
            user_id: ID del usuario
            guild_id: ID del servidor
            count: Número de recomendaciones a generar

        Returns:
            List[Dict]: Lista de canciones recomendadas
        """
        recommendations = []

        # Obtener canciones que le gustaron
        liked_songs = await self.prefs_db.get_liked_songs(user_id, guild_id, 20)

        if not liked_songs:
            # Si no hay datos, buscar música popular genérica
            logger.info(f'No preferences found for user {user_id}, returning popular music')
            return await self._get_popular_music(count)

        # Obtener artistas favoritos
        favorite_artists = await self.prefs_db.get_favorite_artists(user_id, guild_id, 5)

        # Obtener artistas a evitar
        disliked_artists = await self.prefs_db.get_disliked_artists(user_id, guild_id)

        # Estrategia 1: Buscar más canciones de artistas favoritos (40%)
        artist_recs = await self._recommend_from_favorite_artists(
            favorite_artists,
            disliked_artists,
            int(count * 0.4)
        )
        recommendations.extend(artist_recs)

        # Estrategia 2: Buscar canciones similares a las que le gustaron (40%)
        similar_recs = await self._recommend_similar_songs(
            liked_songs,
            disliked_artists,
            int(count * 0.4)
        )
        recommendations.extend(similar_recs)

        # Estrategia 3: Exploración - nuevas canciones relacionadas (20%)
        explore_recs = await self._explore_new_music(
            liked_songs,
            favorite_artists,
            disliked_artists,
            count - len(recommendations)
        )
        recommendations.extend(explore_recs)

        # Mezclar recomendaciones
        random.shuffle(recommendations)

        return recommendations[:count]

    async def _recommend_from_favorite_artists(self, favorite_artists: List[Dict],
                                               disliked_artists: List[str],
                                               count: int) -> List[Dict]:
        """Buscar más canciones de artistas favoritos"""
        recommendations = []

        for artist_data in favorite_artists[:3]:  # Top 3 artistas
            artist = artist_data['artist']

            if artist in disliked_artists:
                continue

            try:
                # Buscar canciones populares del artista
                query = f"{artist} popular songs"
                results = await self.youtube.search(query, limit=3)

                recommendations.extend(results)

                if len(recommendations) >= count:
                    break
            except Exception as e:
                logger.error(f'Error searching for artist {artist}: {e}')

        return recommendations[:count]

    async def _recommend_similar_songs(self, liked_songs: List[Dict],
                                      disliked_artists: List[str],
                                      count: int) -> List[Dict]:
        """Buscar canciones similares a las que le gustaron"""
        recommendations = []

        # Tomar muestras aleatorias de canciones que le gustaron
        sample_size = min(5, len(liked_songs))
        sampled_songs = random.sample(liked_songs, sample_size)

        for song in sampled_songs:
            try:
                # Buscar canciones similares usando el título como referencia
                query = f"{song['song_title']} similar songs"
                results = await self.youtube.search(query, limit=2)

                # Filtrar artistas no deseados
                filtered_results = [
                    r for r in results
                    if r.get('uploader', '') not in disliked_artists
                ]

                recommendations.extend(filtered_results)

                if len(recommendations) >= count:
                    break
            except Exception as e:
                logger.error(f'Error finding similar songs: {e}')

        return recommendations[:count]

    async def _explore_new_music(self, liked_songs: List[Dict],
                                favorite_artists: List[Dict],
                                disliked_artists: List[str],
                                count: int) -> List[Dict]:
        """Explorar nueva música basada en géneros/estilos que le gustan"""
        recommendations = []

        # Extraer palabras clave de títulos de canciones que le gustaron
        keywords = self._extract_keywords(liked_songs)

        for keyword in keywords[:3]:
            try:
                query = f"{keyword} music"
                results = await self.youtube.search(query, limit=2)

                # Filtrar artistas no deseados
                filtered_results = [
                    r for r in results
                    if r.get('uploader', '') not in disliked_artists
                ]

                recommendations.extend(filtered_results)

                if len(recommendations) >= count:
                    break
            except Exception as e:
                logger.error(f'Error exploring new music: {e}')

        return recommendations[:count]

    def _extract_keywords(self, liked_songs: List[Dict]) -> List[str]:
        """Extraer palabras clave relevantes de canciones que le gustaron"""
        # Palabras comunes de géneros musicales
        genre_keywords = [
            'rock', 'pop', 'jazz', 'classical', 'electronic', 'hip hop',
            'country', 'reggae', 'blues', 'metal', 'indie', 'folk',
            'r&b', 'soul', 'funk', 'disco', 'house', 'techno', 'dubstep',
            'rap', 'latin', 'salsa', 'reggaeton', 'bachata', 'cumbia'
        ]

        keywords = []

        for song in liked_songs:
            title = song.get('song_title', '').lower()

            # Buscar palabras clave de género en el título
            for genre in genre_keywords:
                if genre in title:
                    if genre not in keywords:
                        keywords.append(genre)

        # Si no encontramos géneros, usar artistas favoritos
        if not keywords and liked_songs:
            # Usar el artista de la canción más reciente que le gustó
            latest_song = liked_songs[0]
            if latest_song.get('artist'):
                keywords.append(latest_song['artist'])

        return keywords

    async def _get_popular_music(self, count: int) -> List[Dict]:
        """Obtener música popular genérica cuando no hay preferencias"""
        try:
            queries = [
                "top hits 2024",
                "popular music",
                "trending songs",
                "best songs 2024"
            ]

            query = random.choice(queries)
            results = await self.youtube.search(query, limit=count)
            return results
        except Exception as e:
            logger.error(f'Error getting popular music: {e}')
            return []

    async def should_skip_song(self, user_id: int, guild_id: int,
                              artist: str) -> bool:
        """
        Determinar si se debe saltar automáticamente una canción
        basado en el historial del usuario
        """
        return await self.prefs_db.should_avoid_artist(user_id, guild_id, artist)

    async def find_playlist_by_query(self, query: str, limit: int = 1) -> List[Dict]:
        """
        Buscar playlists en YouTube basadas en una query contextual
        Ejemplos: "rock music", "hits 2010", "chill vibes", etc.

        Args:
            query: Query de búsqueda (ej: "rock", "hits 2010")
            limit: Número de playlists a buscar

        Returns:
            List[Dict]: Lista de playlists encontradas
        """
        try:
            # Mejorar la query para buscar específicamente playlists
            enhanced_queries = [
                f"{query} playlist",
                f"{query} mix",
                f"best {query}",
                f"{query} compilation"
            ]

            all_results = []

            for enhanced_query in enhanced_queries[:2]:  # Probar 2 variaciones
                results = await self.youtube.search(enhanced_query, limit=limit * 2)

                # Filtrar por resultados que parezcan playlists/compilaciones
                playlist_results = [
                    r for r in results
                    if any(keyword in r.get('title', '').lower()
                          for keyword in ['playlist', 'mix', 'compilation', 'best of', 'top'])
                ]

                all_results.extend(playlist_results)

                if len(all_results) >= limit:
                    break

            return all_results[:limit]

        except Exception as e:
            logger.error(f'Error finding playlist by query: {e}')
            return []

    async def generate_radio_queue(self, user_id: int, guild_id: int,
                                  seed_song: Optional[Dict] = None,
                                  queue_size: int = 20) -> List[Dict]:
        """
        Generar una cola de reproducción estilo 'radio' personalizada

        Args:
            user_id: ID del usuario
            guild_id: ID del servidor
            seed_song: Canción semilla opcional para basar recomendaciones
            queue_size: Tamaño de la cola a generar

        Returns:
            List[Dict]: Cola de canciones recomendadas
        """
        queue = []

        if seed_song:
            # Si hay canción semilla, buscar similares
            try:
                query = f"{seed_song.get('title', '')} radio"
                results = await self.youtube.search(query, limit=queue_size // 2)
                queue.extend(results)
            except:
                pass

        # Rellenar el resto con recomendaciones personalizadas
        recommendations = await self.get_recommendations(
            user_id,
            guild_id,
            queue_size - len(queue)
        )
        queue.extend(recommendations)

        # Mezclar para variedad
        random.shuffle(queue)

        return queue[:queue_size]
