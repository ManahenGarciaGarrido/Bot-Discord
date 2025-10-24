"""
Embeds - Funciones para crear embeds bonitos de Discord
"""
import discord
from typing import List, Optional
from .song import Song


def create_now_playing_embed(song: Song, loop_mode: str = 'off', volume: int = 50) -> discord.Embed:
    """
    Crear embed de "Now Playing"

    Args:
        song: Canción actual
        loop_mode: Modo de loop ('off', 'song', 'queue')
        volume: Volumen actual (0-100)

    Returns:
        discord.Embed: Embed formateado
    """
    embed = discord.Embed(
        title="🎵 Reproduciendo Ahora",
        description=f"**{song.title}**",
        color=discord.Color.green()
    )

    # Información del canal/artista
    embed.add_field(
        name="📺 Canal",
        value=song.uploader,
        inline=True
    )

    # Duración
    embed.add_field(
        name="⏱️ Duración",
        value=song.format_duration(),
        inline=True
    )

    # Solicitado por
    embed.add_field(
        name="👤 Solicitado por",
        value=song.requester.mention,
        inline=True
    )

    # Volumen
    volume_emoji = "🔊" if volume > 50 else "🔉" if volume > 0 else "🔇"
    embed.add_field(
        name=f"{volume_emoji} Volumen",
        value=f"{volume}%",
        inline=True
    )

    # Loop mode
    loop_emoji = {
        'off': '➡️',
        'song': '🔂',
        'queue': '🔁'
    }
    loop_text = {
        'off': 'Desactivado',
        'song': 'Canción',
        'queue': 'Cola'
    }
    embed.add_field(
        name=f"{loop_emoji.get(loop_mode, '➡️')} Loop",
        value=loop_text.get(loop_mode, 'Desactivado'),
        inline=True
    )

    # Source
    source_emoji = "🎵" if song.source == 'youtube' else "🎧"
    embed.add_field(
        name=f"{source_emoji} Fuente",
        value=song.source.capitalize(),
        inline=True
    )

    # Thumbnail
    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)

    # URL
    embed.add_field(
        name="🔗 Enlace",
        value=f"[Click aquí]({song.url})",
        inline=False
    )

    embed.set_footer(text="Usa !queue para ver la cola completa")

    return embed


def create_queue_embed(queue: List[Song], current_song: Optional[Song] = None, page: int = 1, per_page: int = 10) -> discord.Embed:
    """
    Crear embed de cola de reproducción

    Args:
        queue: Lista de canciones en cola
        current_song: Canción actual (opcional)
        page: Página actual para paginación
        per_page: Canciones por página

    Returns:
        discord.Embed: Embed formateado
    """
    embed = discord.Embed(
        title="📝 Cola de Reproducción",
        color=discord.Color.blue()
    )

    # Canción actual
    if current_song:
        embed.add_field(
            name="▶️ Reproduciendo Ahora:",
            value=f"**{current_song.title}**\n⏱️ `{current_song.format_duration()}` | 👤 {current_song.requester.mention}",
            inline=False
        )
        embed.add_field(name="\u200b", value="\u200b", inline=False)  # Separador

    # Cola
    if not queue:
        embed.add_field(
            name="📭 Cola Vacía",
            value="No hay canciones en la cola. Usa `!play` para añadir música.",
            inline=False
        )
    else:
        # Calcular páginas
        total_pages = (len(queue) - 1) // per_page + 1
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, len(queue))

        # Añadir canciones de la página actual
        queue_text = ""
        for i in range(start_idx, end_idx):
            song = queue[i]
            queue_text += f"**{i + 1}.** {song.title[:50]}\n"
            queue_text += f"⏱️ `{song.format_duration()}` | 👤 {song.requester.mention}\n\n"

        embed.add_field(
            name=f"🎵 En Cola (Página {page}/{total_pages}):",
            value=queue_text or "Sin canciones",
            inline=False
        )

        # Duración total
        total_duration = sum(song.duration for song in queue)
        hours = total_duration // 3600
        minutes = (total_duration % 3600) // 60
        seconds = total_duration % 60

        if hours > 0:
            duration_str = f"{hours}h {minutes}m {seconds}s"
        else:
            duration_str = f"{minutes}m {seconds}s"

        embed.add_field(
            name="⏱️ Duración Total",
            value=duration_str,
            inline=True
        )

        embed.add_field(
            name="🔢 Total de Canciones",
            value=str(len(queue)),
            inline=True
        )

    embed.set_footer(text="Usa !remove <número> para quitar canciones de la cola")

    return embed


def create_search_results_embed(results: List[dict], query: str) -> discord.Embed:
    """
    Crear embed de resultados de búsqueda

    Args:
        results: Lista de resultados de búsqueda
        query: Query de búsqueda

    Returns:
        discord.Embed: Embed formateado
    """
    embed = discord.Embed(
        title="🔍 Resultados de Búsqueda",
        description=f"Búsqueda: **{query}**\n\nReacciona con el número para seleccionar:",
        color=discord.Color.blue()
    )

    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

    for i, result in enumerate(results[:5]):
        title = result.get('title', 'Sin título')
        duration = result.get('duration', 0)
        uploader = result.get('uploader', 'Desconocido')

        # Formatear duración
        if duration:
            minutes = duration // 60
            seconds = duration % 60
            duration_str = f"{minutes}:{seconds:02d}"
        else:
            duration_str = "??:??"

        embed.add_field(
            name=f"{emojis[i]} {title[:50]}",
            value=f"👤 {uploader[:30]}\n⏱️ {duration_str}",
            inline=False
        )

    embed.set_footer(text="Selecciona en 30 segundos o se cancelará")

    return embed


def create_error_embed(title: str, description: str) -> discord.Embed:
    """
    Crear embed de error

    Args:
        title: Título del error
        description: Descripción del error

    Returns:
        discord.Embed: Embed formateado
    """
    embed = discord.Embed(
        title=f"❌ {title}",
        description=description,
        color=discord.Color.red()
    )
    return embed


def create_success_embed(title: str, description: str) -> discord.Embed:
    """
    Crear embed de éxito

    Args:
        title: Título del mensaje
        description: Descripción del mensaje

    Returns:
        discord.Embed: Embed formateado
    """
    embed = discord.Embed(
        title=f"✅ {title}",
        description=description,
        color=discord.Color.green()
    )
    return embed


def create_info_embed(title: str, description: str) -> discord.Embed:
    """
    Crear embed de información

    Args:
        title: Título del mensaje
        description: Descripción del mensaje

    Returns:
        discord.Embed: Embed formateado
    """
    embed = discord.Embed(
        title=f"ℹ️ {title}",
        description=description,
        color=discord.Color.blue()
    )
    return embed


def create_favorites_embed(favorites: List[dict], user_name: str) -> discord.Embed:
    """
    Crear embed de lista de favoritos

    Args:
        favorites: Lista de canciones favoritas
        user_name: Nombre del usuario

    Returns:
        discord.Embed: Embed formateado
    """
    embed = discord.Embed(
        title=f"❤️ Favoritos de {user_name}",
        color=discord.Color.red()
    )

    if not favorites:
        embed.description = "No tienes canciones favoritas aún.\nUsa `!favorite` mientras reproduces una canción para añadirla."
        return embed

    favorites_text = ""
    for i, fav in enumerate(favorites[:25], 1):  # Máximo 25 para no exceder límites
        favorites_text += f"**{i}.** {fav['title'][:50]}\n"

    embed.description = favorites_text
    embed.set_footer(text=f"Total: {len(favorites)} canciones | Usa !playfav <número> para reproducir")

    return embed


def create_stats_embed(stats: dict) -> discord.Embed:
    """
    Crear embed de estadísticas del bot

    Args:
        stats: Diccionario con estadísticas

    Returns:
        discord.Embed: Embed formateado
    """
    embed = discord.Embed(
        title="📊 Estadísticas del Bot",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="🎵 Canciones Reproducidas",
        value=str(stats.get('songs_played', 0)),
        inline=True
    )

    embed.add_field(
        name="⏱️ Tiempo Total",
        value=stats.get('total_time', '0h 0m'),
        inline=True
    )

    embed.add_field(
        name="💿 Servidores Activos",
        value=str(stats.get('active_servers', 0)),
        inline=True
    )

    embed.add_field(
        name="👥 Usuarios Totales",
        value=str(stats.get('total_users', 0)),
        inline=True
    )

    if 'top_songs' in stats and stats['top_songs']:
        top_text = "\n".join([f"**{i+1}.** {song}" for i, song in enumerate(stats['top_songs'][:5])])
        embed.add_field(
            name="🔝 Top 5 Canciones",
            value=top_text,
            inline=False
        )

    return embed
