"""
YouTube Handler - Maneja la extracción de información y streams de YouTube
Utiliza yt-dlp para extraer información sin descargar archivos
"""
import yt_dlp
import asyncio
from typing import Dict, List, Optional
import logging
import os


logger = logging.getLogger('MusicBot.YouTube')


class YouTubeHandler:
    """
    Handler para interactuar con YouTube mediante yt-dlp
    Proporciona métodos para búsqueda, extracción de info, y obtención de URLs de stream
    """

    def __init__(self):
        """Inicializar el handler con opciones de yt-dlp"""
        # Configuración base de yt-dlp
        base_opts = {
            'format': 'bestaudio/best',
            'noplaylist': False,  # Permitir playlists
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0',  # Bind a IPv4
            'extract_flat': False,  # Extraer info completa
            'age_limit': None,
        }

        # Configurar cookies para evitar bloqueos de YouTube
        cookies_config = self._setup_cookies()
        base_opts.update(cookies_config)

        self.ydl_opts = base_opts

        # Opciones específicas para búsqueda
        self.search_opts = {
            **self.ydl_opts,
            'extract_flat': True,  # Solo info básica para búsquedas
            'skip_download': True,
        }

        # Opciones para obtener stream URL
        stream_opts_base = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'source_address': '0.0.0.0',
        }
        stream_opts_base.update(cookies_config)
        self.stream_opts = stream_opts_base

    def _setup_cookies(self) -> dict:
        """
        Configurar cookies para evitar bloqueos de YouTube
        Intenta usar cookies del navegador automáticamente
        """
        cookies_opts = {}

        # Prioridad 1: Variable de entorno con path a archivo de cookies
        cookies_file = os.getenv('YOUTUBE_COOKIES_FILE')
        if cookies_file and os.path.exists(cookies_file):
            logger.info(f'Using cookies from file: {cookies_file}')
            cookies_opts['cookiefile'] = cookies_file
            return cookies_opts

        # Prioridad 2: Usar cookies del navegador automáticamente
        browser = os.getenv('COOKIES_BROWSER', 'chrome')  # chrome, firefox, edge, safari, etc.

        try:
            # Intentar con el navegador especificado
            cookies_opts['cookiesfrombrowser'] = (browser,)
            logger.info(f'✅ Configured to use cookies from {browser}')
            return cookies_opts
        except Exception as e:
            logger.warning(f'Could not setup cookies from {browser}: {e}')

        # Prioridad 3: Intentar con navegadores comunes
        browsers = ['chrome', 'firefox', 'edge', 'brave', 'opera', 'safari']
        for browser_name in browsers:
            try:
                cookies_opts['cookiesfrombrowser'] = (browser_name,)
                logger.info(f'✅ Configured to use cookies from {browser_name}')
                return cookies_opts
            except:
                continue

        # Si no se pudo configurar cookies, advertir
        logger.warning('⚠️  No cookies configured - YouTube may block requests')
        logger.warning('💡 Set COOKIES_BROWSER environment variable (chrome/firefox/edge)')
        return cookies_opts

    async def extract_info(self, url: str) -> Optional[Dict]:
        """
        Extraer información de un video o playlist de YouTube

        Args:
            url: URL del video o playlist de YouTube

        Returns:
            Dict: Información del video/playlist o None si hay error
        """
        try:
            loop = asyncio.get_event_loop()
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = await loop.run_in_executor(
                    None,
                    lambda: ydl.extract_info(url, download=False)
                )
                return info
        except Exception as e:
            logger.error(f'Error extrayendo info de {url}: {e}')
            return None

    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Buscar videos en YouTube

        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados (default: 5)

        Returns:
            List[Dict]: Lista de resultados de búsqueda
        """
        try:
            # Construir query de búsqueda
            search_query = f"ytsearch{limit}:{query}"

            loop = asyncio.get_event_loop()
            with yt_dlp.YoutubeDL(self.search_opts) as ydl:
                info = await loop.run_in_executor(
                    None,
                    lambda: ydl.extract_info(search_query, download=False)
                )

                if 'entries' in info:
                    results = []
                    for entry in info['entries'][:limit]:
                        # Obtener información completa de cada resultado
                        full_info = await self.extract_info(entry['url'])
                        if full_info:
                            results.append(full_info)
                    return results
                return []

        except Exception as e:
            logger.error(f'Error buscando "{query}": {e}')
            return []

    async def get_stream_url(self, url: str) -> Optional[str]:
        """
        Obtener URL de stream de audio de un video

        Args:
            url: URL del video de YouTube

        Returns:
            str: URL del stream de audio o None si hay error
        """
        try:
            loop = asyncio.get_event_loop()
            with yt_dlp.YoutubeDL(self.stream_opts) as ydl:
                info = await loop.run_in_executor(
                    None,
                    lambda: ydl.extract_info(url, download=False)
                )

                if 'url' in info:
                    return info['url']
                elif 'formats' in info:
                    # Buscar el mejor formato de audio
                    for fmt in info['formats']:
                        if fmt.get('acodec') != 'none' and fmt.get('url'):
                            return fmt['url']

                return None

        except Exception as e:
            logger.error(f'Error obteniendo stream URL de {url}: {e}')
            return None

    async def get_playlist(self, url: str, max_songs: int = 50) -> List[Dict]:
        """
        Obtener información de todos los videos en una playlist

        Args:
            url: URL de la playlist de YouTube
            max_songs: Número máximo de canciones a extraer (default: 50)

        Returns:
            List[Dict]: Lista de información de videos
        """
        try:
            loop = asyncio.get_event_loop()
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = await loop.run_in_executor(
                    None,
                    lambda: ydl.extract_info(url, download=False)
                )

                if 'entries' in info:
                    return [entry for entry in info['entries'][:max_songs] if entry]
                return []

        except Exception as e:
            logger.error(f'Error obteniendo playlist {url}: {e}')
            return []

    @staticmethod
    def is_url(query: str) -> bool:
        """
        Verificar si un string es una URL de YouTube

        Args:
            query: String a verificar

        Returns:
            bool: True si es una URL de YouTube
        """
        youtube_domains = ['youtube.com', 'youtu.be', 'youtube', 'www.youtube.com']
        return any(domain in query.lower() for domain in youtube_domains)

    @staticmethod
    def is_playlist(url: str) -> bool:
        """
        Verificar si una URL es una playlist

        Args:
            url: URL a verificar

        Returns:
            bool: True si es una playlist
        """
        return 'list=' in url or 'playlist' in url.lower()

    @staticmethod
    def format_duration(seconds: int) -> str:
        """
        Formatear duración en segundos a formato legible

        Args:
            seconds: Duración en segundos

        Returns:
            str: Duración formateada (MM:SS o HH:MM:SS)
        """
        if seconds == 0:
            return "??:??"

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"

    async def validate_url(self, url: str) -> bool:
        """
        Validar que una URL de YouTube es accesible

        Args:
            url: URL a validar

        Returns:
            bool: True si la URL es válida y accesible
        """
        try:
            info = await self.extract_info(url)
            return info is not None
        except:
            return False
