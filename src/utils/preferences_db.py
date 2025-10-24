"""
Preferences Database - Base de datos para guardar preferencias musicales de usuarios
Sistema de aprendizaje de gustos musicales basado en likes/dislikes
"""
import aiosqlite
import logging
from typing import List, Dict, Optional
from datetime import datetime


logger = logging.getLogger('MusicBot.Preferences')


class PreferencesDB:
    """
    Base de datos para gestionar preferencias musicales de usuarios
    Almacena likes, dislikes, géneros preferidos, y patrones de escucha
    """

    def __init__(self, db_path: str = 'preferences.db'):
        self.db_path = db_path

    async def init_database(self):
        """Inicializar todas las tablas de la base de datos"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Tabla de likes/dislikes
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS song_ratings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        guild_id INTEGER NOT NULL,
                        song_title TEXT NOT NULL,
                        song_url TEXT NOT NULL,
                        artist TEXT,
                        rating INTEGER NOT NULL,  -- 1 = like, -1 = dislike
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, guild_id, song_url)
                    )
                ''')

                # Tabla de géneros/categorías preferidas
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS genre_preferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        guild_id INTEGER NOT NULL,
                        genre TEXT NOT NULL,
                        preference_score INTEGER DEFAULT 0,  -- Puntuación acumulativa
                        UNIQUE(user_id, guild_id, genre)
                    )
                ''')

                # Tabla de historial de reproducción
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS play_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        guild_id INTEGER NOT NULL,
                        song_title TEXT NOT NULL,
                        song_url TEXT NOT NULL,
                        artist TEXT,
                        skipped BOOLEAN DEFAULT 0,
                        completed BOOLEAN DEFAULT 0,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Tabla de artistas preferidos
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS artist_preferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        guild_id INTEGER NOT NULL,
                        artist TEXT NOT NULL,
                        preference_score INTEGER DEFAULT 0,
                        UNIQUE(user_id, guild_id, artist)
                    )
                ''')

                await db.commit()
                logger.info('✅ Preferences database initialized')
        except Exception as e:
            logger.error(f'Error initializing preferences database: {e}')

    async def add_rating(self, user_id: int, guild_id: int, song_title: str,
                        song_url: str, rating: int, artist: str = None) -> bool:
        """
        Añadir o actualizar rating de una canción

        Args:
            user_id: ID del usuario
            guild_id: ID del servidor
            song_title: Título de la canción
            song_url: URL de la canción
            rating: 1 para like, -1 para dislike
            artist: Nombre del artista (opcional)
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT INTO song_ratings (user_id, guild_id, song_title, song_url, artist, rating)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(user_id, guild_id, song_url)
                    DO UPDATE SET rating = ?, timestamp = CURRENT_TIMESTAMP
                ''', (user_id, guild_id, song_title, song_url, artist, rating, rating))
                await db.commit()

                # Actualizar preferencias de artista si existe
                if artist:
                    await self._update_artist_preference(db, user_id, guild_id, artist, rating)

                return True
        except Exception as e:
            logger.error(f'Error adding rating: {e}')
            return False

    async def _update_artist_preference(self, db, user_id: int, guild_id: int,
                                       artist: str, score_change: int):
        """Actualizar preferencia de artista basado en rating"""
        await db.execute('''
            INSERT INTO artist_preferences (user_id, guild_id, artist, preference_score)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, guild_id, artist)
            DO UPDATE SET preference_score = preference_score + ?
        ''', (user_id, guild_id, artist, score_change, score_change))
        await db.commit()

    async def get_liked_songs(self, user_id: int, guild_id: int, limit: int = 50) -> List[Dict]:
        """Obtener canciones con like del usuario"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute('''
                    SELECT * FROM song_ratings
                    WHERE user_id = ? AND guild_id = ? AND rating = 1
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (user_id, guild_id, limit)) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f'Error getting liked songs: {e}')
            return []

    async def get_disliked_songs(self, user_id: int, guild_id: int, limit: int = 50) -> List[Dict]:
        """Obtener canciones con dislike del usuario"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute('''
                    SELECT * FROM song_ratings
                    WHERE user_id = ? AND guild_id = ? AND rating = -1
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (user_id, guild_id, limit)) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f'Error getting disliked songs: {e}')
            return []

    async def get_favorite_artists(self, user_id: int, guild_id: int, limit: int = 10) -> List[Dict]:
        """Obtener artistas favoritos basado en preferencias"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute('''
                    SELECT * FROM artist_preferences
                    WHERE user_id = ? AND guild_id = ? AND preference_score > 0
                    ORDER BY preference_score DESC
                    LIMIT ?
                ''', (user_id, guild_id, limit)) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f'Error getting favorite artists: {e}')
            return []

    async def get_disliked_artists(self, user_id: int, guild_id: int) -> List[str]:
        """Obtener lista de artistas que no le gustan al usuario"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute('''
                    SELECT artist FROM artist_preferences
                    WHERE user_id = ? AND guild_id = ? AND preference_score < -2
                ''', (user_id, guild_id)) as cursor:
                    rows = await cursor.fetchall()
                    return [row[0] for row in rows]
        except Exception as e:
            logger.error(f'Error getting disliked artists: {e}')
            return []

    async def add_play_history(self, user_id: int, guild_id: int, song_title: str,
                              song_url: str, artist: str = None, skipped: bool = False,
                              completed: bool = False) -> bool:
        """Registrar reproducción en el historial"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT INTO play_history (user_id, guild_id, song_title, song_url, artist, skipped, completed)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, guild_id, song_title, song_url, artist, skipped, completed))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f'Error adding play history: {e}')
            return False

    async def get_skip_rate(self, user_id: int, guild_id: int, artist: str) -> float:
        """
        Calcular tasa de skip de un artista
        Returns: Ratio entre 0 y 1 (1 = siempre salta)
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Total de reproducciones del artista
                async with db.execute('''
                    SELECT COUNT(*) FROM play_history
                    WHERE user_id = ? AND guild_id = ? AND artist = ?
                ''', (user_id, guild_id, artist)) as cursor:
                    total = (await cursor.fetchone())[0]

                if total == 0:
                    return 0.0

                # Total de skips del artista
                async with db.execute('''
                    SELECT COUNT(*) FROM play_history
                    WHERE user_id = ? AND guild_id = ? AND artist = ? AND skipped = 1
                ''', (user_id, guild_id, artist)) as cursor:
                    skipped = (await cursor.fetchone())[0]

                return skipped / total
        except Exception as e:
            logger.error(f'Error calculating skip rate: {e}')
            return 0.0

    async def should_avoid_artist(self, user_id: int, guild_id: int, artist: str) -> bool:
        """
        Determinar si se debe evitar un artista basado en patrones de uso
        """
        try:
            # Obtener preferencia del artista
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute('''
                    SELECT preference_score FROM artist_preferences
                    WHERE user_id = ? AND guild_id = ? AND artist = ?
                ''', (user_id, guild_id, artist)) as cursor:
                    result = await cursor.fetchone()

                    if result and result[0] < -3:  # Puntuación muy negativa
                        return True

            # Calcular skip rate
            skip_rate = await self.get_skip_rate(user_id, guild_id, artist)
            if skip_rate > 0.7:  # Más del 70% de las veces salta este artista
                return True

            return False
        except Exception as e:
            logger.error(f'Error checking if should avoid artist: {e}')
            return False

    async def get_user_preferences_summary(self, user_id: int, guild_id: int) -> Dict:
        """Obtener resumen de preferencias del usuario"""
        try:
            liked_songs = await self.get_liked_songs(user_id, guild_id, 10)
            favorite_artists = await self.get_favorite_artists(user_id, guild_id, 5)
            disliked_artists = await self.get_disliked_artists(user_id, guild_id)

            return {
                'liked_songs_count': len(liked_songs),
                'favorite_artists': [a['artist'] for a in favorite_artists],
                'disliked_artists': disliked_artists,
                'top_liked_songs': liked_songs[:5]
            }
        except Exception as e:
            logger.error(f'Error getting preferences summary: {e}')
            return {}
