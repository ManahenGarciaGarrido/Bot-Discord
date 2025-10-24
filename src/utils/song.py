"""
Song Model - Representa una canción en el sistema
"""
from dataclasses import dataclass
import discord
from typing import Optional


@dataclass
class Song:
    """Modelo de datos para una canción"""
    title: str
    url: str
    duration: int  # en segundos
    thumbnail: str
    requester: discord.Member
    source: str = 'youtube'  # 'youtube' o 'spotify'
    uploader: str = 'Unknown'

    @classmethod
    def from_youtube_info(cls, info: dict, requester: discord.Member):
        """
        Crear Song desde información de yt-dlp

        Args:
            info: Diccionario con información del video de yt-dlp
            requester: Miembro de Discord que solicitó la canción

        Returns:
            Song: Instancia de Song con la información extraída
        """
        return cls(
            title=info.get('title', 'Sin título'),
            url=info.get('webpage_url') or info.get('url', ''),
            duration=info.get('duration', 0),
            thumbnail=info.get('thumbnail', ''),
            requester=requester,
            source='youtube',
            uploader=info.get('uploader', 'Unknown')
        )

    def format_duration(self) -> str:
        """
        Formatear duración como MM:SS o HH:MM:SS

        Returns:
            str: Duración formateada
        """
        if self.duration == 0:
            return "??:??"

        hours = self.duration // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"

    def to_embed_field(self, position: Optional[int] = None) -> tuple:
        """
        Convertir a field de embed de Discord

        Args:
            position: Posición en la cola (opcional)

        Returns:
            tuple: (name, value, inline) para usar en embed.add_field()
        """
        if position:
            name = f"**{position}.** {self.title[:50]}"
        else:
            name = self.title[:50]

        value = f"⏱️ `{self.format_duration()}` | 👤 {self.requester.mention}"

        return (name, value, False)

    def __str__(self):
        """Representación en string de la canción"""
        return f"{self.title} - {self.uploader} [{self.format_duration()}]"

    def __repr__(self):
        """Representación para debugging"""
        return f"Song(title='{self.title}', url='{self.url}', duration={self.duration})"
