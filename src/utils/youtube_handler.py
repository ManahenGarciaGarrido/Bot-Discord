"""
YouTube Handler - Maneja la extracción de información y streams de YouTube
Utiliza yt-dlp para extraer información sin descargar archivos
"""
import yt_dlp
import asyncio
from typing import Dict, List, Optional
import logging
import os
import shutil


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

        IMPORTANTE: Para servidores de producción, usa YOUTUBE_COOKIES_FILE
        Las cookies del navegador solo funcionan si el bot corre en tu PC local.
        """
        cookies_opts = {}

        # Prioridad 1: Archivo de cookies (RECOMENDADO PARA SERVIDORES)
        cookies_file = os.getenv('YOUTUBE_COOKIES_FILE')
        if cookies_file:
            if os.path.exists(cookies_file):
                # Copiar archivo a ubicación escribible si está en sistema read-only
                final_cookies_path = self._ensure_writable_cookies(cookies_file)
                logger.info(f'✅ Usando cookies desde archivo: {final_cookies_path}')
                cookies_opts['cookiefile'] = final_cookies_path
                return cookies_opts
            else:
                logger.error(f'❌ Archivo de cookies no encontrado: {cookies_file}')
                logger.error(f'💡 Genera el archivo con: python scripts/export_cookies.py')
                # Continuar intentando otras opciones

        # Prioridad 2: Cookies del navegador (SOLO FUNCIONA EN PC LOCAL)
        browser = os.getenv('COOKIES_BROWSER')
        if browser:
            logger.info(f'🔍 Intentando usar cookies de {browser}...')
            # Verificar que estamos en un entorno con navegador instalado
            if not os.path.exists(os.path.expanduser('~')):
                logger.error('❌ No se detectó directorio home - probablemente estás en un servidor')
                logger.error('💡 SOLUCIÓN: Usa YOUTUBE_COOKIES_FILE en vez de COOKIES_BROWSER')
            else:
                try:
                    # Intentar configurar cookies del navegador
                    cookies_opts['cookiesfrombrowser'] = (browser,)
                    logger.info(f'⚙️  Configurado para usar cookies de {browser}')
                    # Nota: yt-dlp validará esto cuando se use
                    return cookies_opts
                except Exception as e:
                    logger.error(f'❌ Error configurando cookies de {browser}: {e}')

        # Si llegamos aquí, no hay cookies configuradas
        logger.error('=' * 70)
        logger.error('❌ NO HAY COOKIES CONFIGURADAS - YOUTUBE BLOQUEARÁ LAS PETICIONES')
        logger.error('=' * 70)
        logger.error('')
        logger.error('📋 SOLUCIÓN RECOMENDADA (para servidores):')
        logger.error('   1. Ejecuta: python scripts/export_cookies.py')
        logger.error('   2. Sube el archivo cookies.txt a tu servidor')
        logger.error('   3. Añade a .env: YOUTUBE_COOKIES_FILE=/path/to/cookies.txt')
        logger.error('')
        logger.error('💻 Alternativa (solo para PC local):')
        logger.error('   1. Asegúrate de tener Chrome/Edge/Firefox instalado')
        logger.error('   2. Inicia sesión en youtube.com en ese navegador')
        logger.error('   3. Añade a .env: COOKIES_BROWSER=chrome')
        logger.error('')
        logger.error('=' * 70)

        return cookies_opts

    def _ensure_writable_cookies(self, cookies_path: str) -> str:
        """
        Asegura que el archivo de cookies esté en una ubicación escribible.

        En plataformas como Render, los Secret Files se montan en /etc/secrets/
        que es read-only. yt-dlp necesita escribir en el archivo de cookies,
        así que lo copiamos a /tmp/ que es escribible.

        Args:
            cookies_path: Ruta original del archivo de cookies

        Returns:
            str: Ruta del archivo de cookies escribible
        """
        # Si el archivo está en una ubicación conocida como read-only, copiarlo
        readonly_paths = ['/etc/secrets/', '/run/secrets/']

        is_readonly = any(cookies_path.startswith(path) for path in readonly_paths)

        if is_readonly:
            # Copiar a /tmp/ que es escribible
            tmp_cookies_path = '/tmp/youtube_cookies.txt'
            try:
                shutil.copy2(cookies_path, tmp_cookies_path)
                logger.info(f'📋 Cookies copiadas de {cookies_path} a {tmp_cookies_path} (ubicación escribible)')
                return tmp_cookies_path
            except Exception as e:
                logger.warning(f'⚠️  No se pudo copiar cookies a /tmp/: {e}')
                logger.warning(f'⚠️  Intentando usar archivo original (puede fallar si es read-only)')
                return cookies_path

        # Si no está en ubicación read-only, verificar si es escribible
        try:
            # Intentar abrir en modo append para verificar permisos de escritura
            with open(cookies_path, 'a'):
                pass
            # Si funciona, el archivo es escribible
            logger.info(f'✓ Archivo de cookies es escribible: {cookies_path}')
            return cookies_path
        except (PermissionError, OSError) as e:
            # El archivo no es escribible, copiar a /tmp/
            logger.warning(f'⚠️  Archivo de cookies no es escribible: {e}')
            tmp_cookies_path = '/tmp/youtube_cookies.txt'
            try:
                shutil.copy2(cookies_path, tmp_cookies_path)
                logger.info(f'📋 Cookies copiadas a {tmp_cookies_path} (ubicación escribible)')
                return tmp_cookies_path
            except Exception as copy_error:
                logger.error(f'❌ Error copiando cookies a /tmp/: {copy_error}')
                logger.error(f'⚠️  Usando archivo original (puede no funcionar)')
                return cookies_path

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
