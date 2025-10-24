"""
Spotify Handler - Maneja la extracción de metadatos de Spotify
Convierte enlaces de Spotify a búsquedas de YouTube
"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from typing import Dict, List, Optional
import logging


logger = logging.getLogger('MusicBot.Spotify')


class SpotifyHandler:
    """
    Handler para interactuar con la API de Spotify
    Extrae metadatos de tracks, álbumes y playlists para buscarlos en YouTube
    """

    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        Inicializar el handler de Spotify

        Args:
            client_id: Client ID de Spotify (usa variable de entorno si no se provee)
            client_secret: Client Secret de Spotify (usa variable de entorno si no se provee)
        """
        self.client_id = client_id or os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')

        if not self.client_id or not self.client_secret:
            logger.warning('Spotify credentials not found. Spotify features will be disabled.')
            self.sp = None
            return

        try:
            # Autenticación con Spotify
            auth_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            logger.info('✅ Spotify API initialized successfully')
        except Exception as e:
            logger.error(f'Error initializing Spotify API: {e}')
            self.sp = None

    def is_available(self) -> bool:
        """
        Verificar si el handler de Spotify está disponible

        Returns:
            bool: True si Spotify está configurado correctamente
        """
        return self.sp is not None

    @staticmethod
    def is_spotify_url(url: str) -> bool:
        """
        Verificar si una URL es de Spotify

        Args:
            url: URL a verificar

        Returns:
            bool: True si es una URL de Spotify
        """
        return 'spotify.com' in url.lower()

    @staticmethod
    def get_url_type(url: str) -> Optional[str]:
        """
        Determinar el tipo de URL de Spotify

        Args:
            url: URL de Spotify

        Returns:
            str: 'track', 'album', 'playlist', o None
        """
        if 'track' in url:
            return 'track'
        elif 'album' in url:
            return 'album'
        elif 'playlist' in url:
            return 'playlist'
        return None

    async def get_track_info(self, url: str) -> Optional[Dict]:
        """
        Obtener información de un track de Spotify

        Args:
            url: URL del track

        Returns:
            Dict: Información del track o None si hay error
        """
        if not self.sp:
            logger.error('Spotify API not initialized')
            return None

        try:
            # Extraer ID del track de la URL
            track_id = url.split('track/')[-1].split('?')[0]

            # Obtener información del track
            track = self.sp.track(track_id)

            return {
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'url': track['external_urls']['spotify'],
                'thumbnail': track['album']['images'][0]['url'] if track['album']['images'] else None
            }
        except Exception as e:
            logger.error(f'Error getting track info from {url}: {e}')
            return None

    async def get_album_tracks(self, url: str) -> List[Dict]:
        """
        Obtener todos los tracks de un álbum

        Args:
            url: URL del álbum

        Returns:
            List[Dict]: Lista de información de tracks
        """
        if not self.sp:
            return []

        try:
            # Extraer ID del álbum
            album_id = url.split('album/')[-1].split('?')[0]

            # Obtener información del álbum
            album = self.sp.album(album_id)

            tracks = []
            for track in album['tracks']['items']:
                tracks.append({
                    'name': track['name'],
                    'artists': [artist['name'] for artist in track['artists']],
                    'album': album['name'],
                    'duration_ms': track['duration_ms'],
                    'url': track['external_urls']['spotify'],
                    'thumbnail': album['images'][0]['url'] if album['images'] else None
                })

            return tracks
        except Exception as e:
            logger.error(f'Error getting album tracks from {url}: {e}')
            return []

    async def get_playlist_tracks(self, url: str) -> List[Dict]:
        """
        Obtener todos los tracks de una playlist

        Args:
            url: URL de la playlist

        Returns:
            List[Dict]: Lista de información de tracks
        """
        if not self.sp:
            return []

        try:
            # Extraer ID de la playlist
            playlist_id = url.split('playlist/')[-1].split('?')[0]

            # Obtener información de la playlist
            playlist = self.sp.playlist(playlist_id)

            tracks = []
            for item in playlist['tracks']['items']:
                track = item['track']
                if track:  # Algunos tracks pueden ser None
                    tracks.append({
                        'name': track['name'],
                        'artists': [artist['name'] for artist in track['artists']],
                        'album': track['album']['name'],
                        'duration_ms': track['duration_ms'],
                        'url': track['external_urls']['spotify'],
                        'thumbnail': track['album']['images'][0]['url'] if track['album']['images'] else None
                    })

            return tracks
        except Exception as e:
            logger.error(f'Error getting playlist tracks from {url}: {e}')
            return []

    def to_youtube_query(self, track_info: Dict) -> str:
        """
        Convertir información de track de Spotify a query de búsqueda de YouTube

        Args:
            track_info: Diccionario con información del track

        Returns:
            str: Query optimizado para búsqueda en YouTube
        """
        # Construir query con artistas y nombre del track
        artists = ' '.join(track_info['artists'])
        name = track_info['name']

        # Formato: "Artist - Track Name official audio"
        query = f"{artists} - {name} official audio"

        return query

    async def process_url(self, url: str) -> List[Dict]:
        """
        Procesar cualquier URL de Spotify y devolver lista de tracks

        Args:
            url: URL de Spotify (track, album, o playlist)

        Returns:
            List[Dict]: Lista de información de tracks
        """
        url_type = self.get_url_type(url)

        if url_type == 'track':
            track_info = await self.get_track_info(url)
            return [track_info] if track_info else []

        elif url_type == 'album':
            return await self.get_album_tracks(url)

        elif url_type == 'playlist':
            return await self.get_playlist_tracks(url)

        logger.warning(f'Unknown Spotify URL type: {url}')
        return []

    @staticmethod
    def format_duration(duration_ms: int) -> str:
        """
        Formatear duración de milisegundos a formato MM:SS

        Args:
            duration_ms: Duración en milisegundos

        Returns:
            str: Duración formateada
        """
        seconds = duration_ms // 1000
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"
