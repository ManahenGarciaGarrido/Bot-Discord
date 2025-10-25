"""
Cache Manager - Sistema de caché en memoria para información de videos
Reduce dramáticamente el tiempo de carga al reusar datos ya obtenidos
"""
import asyncio
import time
from typing import Dict, Optional, Any
import logging


logger = logging.getLogger('MusicBot.Cache')


class VideoCache:
    """
    Caché en memoria para información de videos de YouTube.

    Evita llamadas repetidas a yt-dlp para el mismo video,
    reduciendo significativamente el tiempo de respuesta.
    """

    def __init__(self, ttl: int = 3600):
        """
        Inicializar el caché.

        Args:
            ttl: Tiempo de vida en segundos (default: 1 hora)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = ttl
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Dict]:
        """
        Obtener un valor del caché.

        Args:
            key: Clave (URL del video)

        Returns:
            Dict con la información del video o None si no existe/expiró
        """
        async with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache[key]

            # Verificar si expiró
            if time.time() - entry['timestamp'] > self._ttl:
                del self._cache[key]
                logger.debug(f'Cache expired for: {key[:50]}...')
                return None

            logger.debug(f'✅ Cache HIT for: {key[:50]}...')
            return entry['data']

    async def set(self, key: str, value: Dict) -> None:
        """
        Guardar un valor en el caché.

        Args:
            key: Clave (URL del video)
            value: Información del video
        """
        async with self._lock:
            self._cache[key] = {
                'data': value,
                'timestamp': time.time()
            }
            logger.debug(f'💾 Cache SET for: {key[:50]}...')

    async def clear(self) -> None:
        """Limpiar todo el caché."""
        async with self._lock:
            count = len(self._cache)
            self._cache.clear()
            logger.info(f'🗑️  Cache cleared ({count} entries removed)')

    async def remove(self, key: str) -> None:
        """
        Remover una entrada específica del caché.

        Args:
            key: Clave a remover
        """
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f'🗑️  Cache entry removed: {key[:50]}...')

    async def cleanup_expired(self) -> None:
        """Limpiar entradas expiradas del caché."""
        async with self._lock:
            now = time.time()
            expired_keys = [
                key for key, entry in self._cache.items()
                if now - entry['timestamp'] > self._ttl
            ]

            for key in expired_keys:
                del self._cache[key]

            if expired_keys:
                logger.info(f'🗑️  Cleaned {len(expired_keys)} expired cache entries')

    def get_stats(self) -> Dict[str, int]:
        """
        Obtener estadísticas del caché.

        Returns:
            Dict con número de entradas y tamaño estimado
        """
        return {
            'entries': len(self._cache),
            'ttl': self._ttl
        }


# Instancia global del caché
video_cache = VideoCache(ttl=3600)  # 1 hora de TTL
