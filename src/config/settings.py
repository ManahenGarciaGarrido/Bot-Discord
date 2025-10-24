"""
Settings - Configuración centralizada del bot
"""
import os
from dotenv import load_dotenv


# Cargar variables de entorno
load_dotenv()


class Settings:
    """Clase para almacenar toda la configuración del bot"""

    # Discord Configuration
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    PREFIX = os.getenv('PREFIX', '!')

    # Spotify Configuration
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Bot Configuration
    DEFAULT_VOLUME = int(os.getenv('DEFAULT_VOLUME', 50))
    MAX_QUEUE_SIZE = int(os.getenv('MAX_QUEUE_SIZE', 100))
    MAX_SONG_DURATION = int(os.getenv('MAX_SONG_DURATION', 7200))  # 2 horas en segundos
    MAX_FAVORITES_PER_USER = int(os.getenv('MAX_FAVORITES_PER_USER', 50))

    # Search Configuration
    SEARCH_RESULTS_LIMIT = 5
    SEARCH_TIMEOUT = 30  # segundos

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'favorites.db')

    # FFmpeg Options
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    # Cooldown Configuration (en segundos)
    COMMAND_COOLDOWN = 5
    SEARCH_COOLDOWN = 10

    # Embed Colors
    COLOR_SUCCESS = 0x00FF00
    COLOR_ERROR = 0xFF0000
    COLOR_INFO = 0x0099FF
    COLOR_MUSIC = 0x9B59B6

    # Server Configuration for deployment
    HEALTH_CHECK_PORT = int(os.getenv('PORT', 8080))
    HEALTH_CHECK_HOST = '0.0.0.0'

    @classmethod
    def validate(cls) -> bool:
        """
        Validar que la configuración esencial está presente

        Returns:
            bool: True si la configuración es válida
        """
        if not cls.DISCORD_TOKEN:
            print("❌ ERROR: DISCORD_TOKEN no encontrado en variables de entorno")
            return False

        if not cls.SPOTIFY_CLIENT_ID or not cls.SPOTIFY_CLIENT_SECRET:
            print("⚠️ WARNING: Spotify credentials no encontrados. Las funciones de Spotify estarán deshabilitadas.")
            # No es crítico, el bot puede funcionar sin Spotify
            return True

        return True

    @classmethod
    def get_info(cls) -> dict:
        """
        Obtener información de configuración (sin secrets)

        Returns:
            dict: Diccionario con configuración no sensible
        """
        return {
            'prefix': cls.PREFIX,
            'default_volume': cls.DEFAULT_VOLUME,
            'max_queue_size': cls.MAX_QUEUE_SIZE,
            'max_song_duration': cls.MAX_SONG_DURATION,
            'max_favorites': cls.MAX_FAVORITES_PER_USER,
            'log_level': cls.LOG_LEVEL,
            'spotify_enabled': bool(cls.SPOTIFY_CLIENT_ID and cls.SPOTIFY_CLIENT_SECRET),
            'health_check_port': cls.HEALTH_CHECK_PORT
        }
