"""
Queue Manager - Gestiona la cola de reproducción de música
"""
from collections import deque
import random
from typing import List, Optional
from .song import Song


class QueueManager:
    """
    Gestor de cola de reproducción FIFO con funcionalidades avanzadas
    Soporta loop, shuffle, y mantiene historial
    """

    def __init__(self, max_size: int = 100):
        """
        Inicializar el gestor de cola

        Args:
            max_size: Tamaño máximo de la cola (default: 100)
        """
        self.queue = deque()
        self.history = deque(maxlen=10)  # Mantiene últimas 10 canciones
        self.max_size = max_size
        self.loop_mode = 'off'  # 'off', 'song', 'queue'
        self._original_queue = None  # Para restaurar después de shuffle

    def add(self, song: Song) -> bool:
        """
        Añadir canción a la cola

        Args:
            song: Canción a añadir

        Returns:
            bool: True si se añadió, False si la cola está llena
        """
        if len(self.queue) >= self.max_size:
            return False
        self.queue.append(song)
        return True

    def add_multiple(self, songs: List[Song]) -> int:
        """
        Añadir múltiples canciones a la cola

        Args:
            songs: Lista de canciones a añadir

        Returns:
            int: Número de canciones añadidas
        """
        added = 0
        for song in songs:
            if len(self.queue) >= self.max_size:
                break
            self.queue.append(song)
            added += 1
        return added

    def next(self) -> Optional[Song]:
        """
        Obtener siguiente canción según el modo de loop

        Returns:
            Song o None: Siguiente canción o None si no hay más
        """
        # Modo loop song - repetir la última canción del historial
        if self.loop_mode == 'song' and self.history:
            return self.history[-1]

        # Si la cola está vacía
        if not self.queue:
            # Modo loop queue - recargar toda la cola desde el historial
            if self.loop_mode == 'queue' and self.history:
                self.queue = deque(self.history)
                self.history.clear()
            else:
                return None

        if not self.queue:
            return None

        song = self.queue.popleft()
        self.history.append(song)
        return song

    def remove(self, index: int) -> bool:
        """
        Eliminar canción por índice (0-based)

        Args:
            index: Índice de la canción a eliminar

        Returns:
            bool: True si se eliminó, False si el índice es inválido
        """
        if 0 <= index < len(self.queue):
            del self.queue[index]
            return True
        return False

    def clear(self):
        """Limpiar completamente la cola"""
        self.queue.clear()

    def shuffle(self):
        """
        Mezclar aleatoriamente el orden de la cola
        Guarda el orden original por si se quiere restaurar
        """
        if len(self.queue) < 2:
            return

        # Guardar orden original
        self._original_queue = list(self.queue)

        # Convertir a lista, mezclar, y reconvertir a deque
        temp = list(self.queue)
        random.shuffle(temp)
        self.queue = deque(temp)

    def unshuffle(self):
        """Restaurar el orden original antes del shuffle"""
        if self._original_queue:
            self.queue = deque(self._original_queue)
            self._original_queue = None

    def move(self, from_index: int, to_index: int) -> bool:
        """
        Mover una canción de una posición a otra

        Args:
            from_index: Índice actual de la canción
            to_index: Nuevo índice deseado

        Returns:
            bool: True si se movió exitosamente
        """
        if not (0 <= from_index < len(self.queue) and 0 <= to_index < len(self.queue)):
            return False

        temp_list = list(self.queue)
        song = temp_list.pop(from_index)
        temp_list.insert(to_index, song)
        self.queue = deque(temp_list)
        return True

    def jump_to(self, index: int) -> Optional[Song]:
        """
        Saltar a una canción específica en la cola,
        eliminando todas las anteriores

        Args:
            index: Índice de la canción (0-based)

        Returns:
            Song o None: La canción en ese índice o None
        """
        if not (0 <= index < len(self.queue)):
            return None

        # Remover todas las canciones hasta ese índice
        for _ in range(index):
            if self.queue:
                skipped = self.queue.popleft()
                self.history.append(skipped)

        # Obtener la canción objetivo
        if self.queue:
            song = self.queue.popleft()
            self.history.append(song)
            return song

        return None

    def get_queue(self) -> List[Song]:
        """
        Obtener lista completa de canciones en la cola

        Returns:
            List[Song]: Lista de canciones
        """
        return list(self.queue)

    def get_history(self) -> List[Song]:
        """
        Obtener historial de canciones reproducidas

        Returns:
            List[Song]: Lista de canciones del historial
        """
        return list(self.history)

    def set_loop_mode(self, mode: str) -> bool:
        """
        Establecer modo de repetición

        Args:
            mode: 'off', 'song', o 'queue'

        Returns:
            bool: True si el modo es válido
        """
        if mode in ['off', 'song', 'queue']:
            self.loop_mode = mode
            return True
        return False

    def get_loop_mode(self) -> str:
        """
        Obtener modo de loop actual

        Returns:
            str: Modo actual ('off', 'song', o 'queue')
        """
        return self.loop_mode

    def get_total_duration(self) -> int:
        """
        Calcular duración total de todas las canciones en la cola

        Returns:
            int: Duración total en segundos
        """
        return sum(song.duration for song in self.queue)

    def is_empty(self) -> bool:
        """
        Verificar si la cola está vacía

        Returns:
            bool: True si está vacía
        """
        return len(self.queue) == 0

    def is_full(self) -> bool:
        """
        Verificar si la cola está llena

        Returns:
            bool: True si está llena
        """
        return len(self.queue) >= self.max_size

    def get_song_at(self, index: int) -> Optional[Song]:
        """
        Obtener canción en un índice específico sin removerla

        Args:
            index: Índice de la canción

        Returns:
            Song o None: Canción en ese índice o None
        """
        if 0 <= index < len(self.queue):
            return list(self.queue)[index]
        return None

    def __len__(self):
        """Número de canciones en la cola"""
        return len(self.queue)

    def __str__(self):
        """Representación en string de la cola"""
        return f"Queue({len(self.queue)} songs, loop={self.loop_mode})"

    def __repr__(self):
        """Representación para debugging"""
        return f"QueueManager(size={len(self.queue)}, max={self.max_size}, loop='{self.loop_mode}')"
