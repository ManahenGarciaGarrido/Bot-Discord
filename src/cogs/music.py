"""
Music Cog - Comandos principales de reproducción de música
Implementa: play, pause, resume, skip, stop, volume, nowplaying, queue, loop, shuffle, seek, jump, move, remove, clear, join, leave
"""
import discord
from discord.ext import commands
import asyncio
from typing import Optional
import logging

from ..utils.song import Song
from ..utils.queue_manager import QueueManager
from ..utils.youtube_handler import YouTubeHandler
from ..utils.spotify_handler import SpotifyHandler
from ..utils.embeds import (
    create_now_playing_embed,
    create_queue_embed,
    create_search_results_embed,
    create_error_embed,
    create_success_embed
)
from ..config.settings import Settings


logger = logging.getLogger('MusicBot.Music')


class Music(commands.Cog):
    """Comandos de reproducción de música desde YouTube y Spotify"""

    def __init__(self, bot):
        self.bot = bot
        self.youtube = YouTubeHandler()
        self.spotify = SpotifyHandler()
        self.guild_states = {}  # Estado por servidor

    def get_guild_state(self, guild_id):
        """Obtener o crear estado del servidor"""
        if guild_id not in self.guild_states:
            self.guild_states[guild_id] = {
                'voice_client': None,
                'queue': QueueManager(max_size=Settings.MAX_QUEUE_SIZE),
                'current_song': None,
                'volume': Settings.DEFAULT_VOLUME / 100,
                'last_channel': None,
                'auto_shuffle': True  # Auto-shuffle para playlists
            }
        return self.guild_states[guild_id]

    async def join_voice_channel(self, ctx):
        """Unir el bot a un canal de voz"""
        state = self.get_guild_state(ctx.guild.id)

        if not ctx.author.voice:
            await ctx.send(embed=create_error_embed("Error", "Debes estar en un canal de voz."))
            return False

        channel = ctx.author.voice.channel

        if state['voice_client'] and state['voice_client'].is_connected():
            if state['voice_client'].channel == channel:
                return True
            await state['voice_client'].move_to(channel)
        else:
            state['voice_client'] = await channel.connect()

        return True

    @commands.command(name='join', aliases=['j', 'connect'])
    async def join(self, ctx):
        """Unir el bot al canal de voz"""
        if await self.join_voice_channel(ctx):
            await ctx.send(embed=create_success_embed(
                "Conectado",
                f"Me uní a {ctx.author.voice.channel.name}"
            ))

    @commands.command(name='leave', aliases=['disconnect', 'dc'])
    async def leave(self, ctx):
        """Desconectar el bot del canal de voz"""
        state = self.get_guild_state(ctx.guild.id)

        if not state['voice_client']:
            await ctx.send(embed=create_error_embed("Error", "No estoy en un canal de voz."))
            return

        if state['voice_client'].is_playing():
            state['voice_client'].stop()

        state['queue'].clear()
        state['current_song'] = None

        await state['voice_client'].disconnect()
        state['voice_client'] = None

        await ctx.send(embed=create_success_embed("Desconectado", "Salí del canal de voz."))

    @commands.command(name='play', aliases=['p'])
    @commands.cooldown(1, Settings.COMMAND_COOLDOWN, commands.BucketType.user)
    async def play(self, ctx, *, query: str):
        """
        Reproducir música desde YouTube, Spotify o búsqueda

        Uso:
            !play <URL de YouTube>
            !play <URL de Spotify>
            !play <nombre de canción>
        """
        if not await self.join_voice_channel(ctx):
            return

        state = self.get_guild_state(ctx.guild.id)
        state['last_channel'] = ctx.channel

        async with ctx.typing():
            songs = None

            # Determinar tipo de input
            if self.youtube.is_url(query):
                # URL de YouTube
                songs = await self._handle_youtube_url(query, ctx.author)
            elif self.spotify.is_spotify_url(query):
                # URL de Spotify
                songs = await self._handle_spotify_url(query, ctx.author)
            else:
                # Búsqueda
                songs = await self._handle_search(ctx, query)

            if not songs:
                await ctx.send(embed=create_error_embed("Error", "No se pudo encontrar la canción."))
                return

            # Añadir canciones a la cola
            added_count = 0
            for song in songs:
                if state['queue'].add(song):
                    added_count += 1
                else:
                    break  # Cola llena

            # Auto-shuffle para playlists
            if added_count > 1 and state.get('auto_shuffle', True):
                state['queue'].shuffle()
                logger.info(f'Auto-shuffled playlist with {added_count} songs')

            # Si no hay nada reproduciéndose, empezar
            if not state['voice_client'].is_playing() and not state['voice_client'].is_paused():
                await self._play_next(ctx.guild.id)
            else:
                # Informar que se añadió a la cola
                if added_count == 1:
                    embed = create_success_embed(
                        "Añadido a la cola",
                        f"**{songs[0].title}**"
                    )
                    embed.set_thumbnail(url=songs[0].thumbnail)
                    await ctx.send(embed=embed)
                else:
                    shuffle_text = " (mezcladas aleatoriamente)" if state.get('auto_shuffle', True) else ""
                    await ctx.send(embed=create_success_embed(
                        "Añadido a la cola",
                        f"{added_count} canciones añadidas a la cola{shuffle_text}."
                    ))

    async def _handle_youtube_url(self, url, requester):
        """Manejar URL de YouTube"""
        try:
            if self.youtube.is_playlist(url):
                # Es una playlist
                entries = await self.youtube.get_playlist(url, max_songs=Settings.MAX_QUEUE_SIZE)
                songs = []
                for entry in entries:
                    song = Song.from_youtube_info(entry, requester)
                    songs.append(song)
                return songs
            else:
                # Video individual
                info = await self.youtube.extract_info(url)
                if info:
                    song = Song.from_youtube_info(info, requester)
                    return [song]
            return None
        except Exception as e:
            logger.error(f'Error handling YouTube URL: {e}')
            return None

    async def _handle_spotify_url(self, url, requester):
        """Manejar URL de Spotify"""
        if not self.spotify.is_available():
            logger.error('Spotify not available')
            return None

        try:
            # Obtener tracks de Spotify
            tracks = await self.spotify.process_url(url)

            if not tracks:
                return None

            # Convertir cada track a YouTube
            songs = []
            for track in tracks[:Settings.MAX_QUEUE_SIZE]:
                query = self.spotify.to_youtube_query(track)
                results = await self.youtube.search(query, limit=1)

                if results:
                    song = Song.from_youtube_info(results[0], requester)
                    song.source = 'spotify'
                    songs.append(song)

            return songs if songs else None

        except Exception as e:
            logger.error(f'Error handling Spotify URL: {e}')
            return None

    async def _handle_search(self, ctx, query):
        """Manejar búsqueda por nombre"""
        try:
            results = await self.youtube.search(query, limit=Settings.SEARCH_RESULTS_LIMIT)

            if not results:
                return None

            # Si solo hay un resultado, usarlo directamente
            if len(results) == 1:
                song = Song.from_youtube_info(results[0], ctx.author)
                return [song]

            # Mostrar resultados para selección
            embed = create_search_results_embed(results, query)
            message = await ctx.send(embed=embed)

            # Añadir reacciones
            emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
            for emoji in emojis[:len(results)]:
                await message.add_reaction(emoji)

            # Esperar reacción del usuario
            def check(reaction, user):
                return (user == ctx.author and
                        str(reaction.emoji) in emojis[:len(results)] and
                        reaction.message.id == message.id)

            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=Settings.SEARCH_TIMEOUT, check=check)
                index = emojis.index(str(reaction.emoji))
                song = Song.from_youtube_info(results[index], ctx.author)
                await message.delete()
                return [song]

            except asyncio.TimeoutError:
                await message.delete()
                await ctx.send(embed=create_error_embed("Tiempo agotado", "Se agotó el tiempo para seleccionar."))
                return None

        except Exception as e:
            logger.error(f'Error in search: {e}')
            return None

    async def _play_next(self, guild_id):
        """Reproducir siguiente canción en la cola"""
        state = self.guild_states.get(guild_id)
        if not state:
            return

        # Obtener siguiente canción
        next_song = state['queue'].next()

        if not next_song:
            state['current_song'] = None
            if state['last_channel']:
                await state['last_channel'].send(embed=create_success_embed(
                    "Cola finalizada",
                    "Se terminaron las canciones en la cola."
                ))
            return

        state['current_song'] = next_song

        try:
            # Obtener URL de stream
            stream_url = await self.youtube.get_stream_url(next_song.url)

            if not stream_url:
                logger.error(f'Failed to get stream URL for {next_song.url}')
                await self._play_next(guild_id)  # Intentar con siguiente
                return

            # Crear source de audio
            audio_source = discord.FFmpegPCMAudio(stream_url, **Settings.FFMPEG_OPTIONS)

            # Ajustar volumen
            audio_source = discord.PCMVolumeTransformer(audio_source, volume=state['volume'])

            # Reproducir
            state['voice_client'].play(
                audio_source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self._play_next(guild_id),
                    self.bot.loop
                )
            )

            # Enviar mensaje de "Now Playing"
            if state['last_channel']:
                embed = create_now_playing_embed(
                    next_song,
                    loop_mode=state['queue'].get_loop_mode(),
                    volume=int(state['volume'] * 100)
                )
                await state['last_channel'].send(embed=embed)

        except Exception as e:
            logger.error(f'Error playing song: {e}')
            if state['last_channel']:
                await state['last_channel'].send(embed=create_error_embed(
                    "Error",
                    f"Error reproduciendo: {next_song.title}"
                ))
            await self._play_next(guild_id)

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pausar reproducción actual"""
        state = self.get_guild_state(ctx.guild.id)

        if not state['voice_client'] or not state['voice_client'].is_playing():
            await ctx.send(embed=create_error_embed("Error", "No hay nada reproduciéndose."))
            return

        state['voice_client'].pause()
        await ctx.send(embed=create_success_embed("Pausado", "⏸️ Reproducción pausada."))

    @commands.command(name='resume', aliases=['unpause'])
    async def resume(self, ctx):
        """Reanudar reproducción"""
        state = self.get_guild_state(ctx.guild.id)

        if not state['voice_client'] or not state['voice_client'].is_paused():
            await ctx.send(embed=create_error_embed("Error", "No hay nada pausado."))
            return

        state['voice_client'].resume()
        await ctx.send(embed=create_success_embed("Reanudado", "▶️ Reproducción reanudada."))

    @commands.command(name='skip', aliases=['s', 'next'])
    async def skip(self, ctx):
        """Saltar canción actual"""
        state = self.get_guild_state(ctx.guild.id)

        if not state['voice_client'] or not state['voice_client'].is_playing():
            await ctx.send(embed=create_error_embed("Error", "No hay nada reproduciéndose."))
            return

        state['voice_client'].stop()  # Trigger next song via after callback
        await ctx.send(embed=create_success_embed("Saltado", "⏭️ Canción saltada."))

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Detener reproducción y limpiar cola"""
        state = self.get_guild_state(ctx.guild.id)

        if not state['voice_client']:
            await ctx.send(embed=create_error_embed("Error", "No estoy en un canal de voz."))
            return

        state['queue'].clear()
        state['current_song'] = None

        if state['voice_client'].is_playing():
            state['voice_client'].stop()

        await ctx.send(embed=create_success_embed("Detenido", "⏹️ Reproducción detenida y cola limpiada."))

    @commands.command(name='volume', aliases=['vol', 'v'])
    async def volume(self, ctx, volume: int):
        """
        Ajustar volumen (0-100)

        Uso: !volume 50
        """
        if not 0 <= volume <= 100:
            await ctx.send(embed=create_error_embed("Error", "El volumen debe estar entre 0 y 100."))
            return

        state = self.get_guild_state(ctx.guild.id)
        state['volume'] = volume / 100

        if state['voice_client'] and state['voice_client'].source:
            state['voice_client'].source.volume = state['volume']

        await ctx.send(embed=create_success_embed("Volumen ajustado", f"🔊 Volumen: {volume}%"))

    @commands.command(name='nowplaying', aliases=['np', 'current'])
    async def nowplaying(self, ctx):
        """Mostrar canción actual"""
        state = self.get_guild_state(ctx.guild.id)

        if not state['current_song']:
            await ctx.send(embed=create_error_embed("Error", "No hay nada reproduciéndose."))
            return

        embed = create_now_playing_embed(
            state['current_song'],
            loop_mode=state['queue'].get_loop_mode(),
            volume=int(state['volume'] * 100)
        )
        await ctx.send(embed=embed)

    @commands.command(name='queue', aliases=['q'])
    async def queue_command(self, ctx, page: int = 1):
        """Mostrar cola de reproducción"""
        state = self.get_guild_state(ctx.guild.id)
        queue_list = state['queue'].get_queue()

        embed = create_queue_embed(queue_list, state['current_song'], page=page, per_page=10)
        await ctx.send(embed=embed)

    @commands.command(name='loop', aliases=['repeat'])
    async def loop(self, ctx, mode: str = None):
        """
        Configurar modo de repetición

        Uso:
            !loop off     - Desactivar loop
            !loop song    - Repetir canción actual
            !loop queue   - Repetir toda la cola
            !loop         - Alternar entre modos
        """
        state = self.get_guild_state(ctx.guild.id)

        if mode is None:
            # Alternar modos
            current = state['queue'].get_loop_mode()
            modes = ['off', 'song', 'queue']
            next_mode = modes[(modes.index(current) + 1) % len(modes)]
            state['queue'].set_loop_mode(next_mode)
            mode = next_mode
        else:
            mode = mode.lower()
            if not state['queue'].set_loop_mode(mode):
                await ctx.send(embed=create_error_embed(
                    "Error",
                    "Modo inválido. Usa: off, song, o queue"
                ))
                return

        mode_text = {
            'off': '➡️ Desactivado',
            'song': '🔂 Canción actual',
            'queue': '🔁 Cola completa'
        }

        await ctx.send(embed=create_success_embed(
            "Loop configurado",
            f"Modo de repetición: {mode_text.get(mode, mode)}"
        ))

    @commands.command(name='shuffle')
    async def shuffle(self, ctx):
        """Mezclar el orden de la cola"""
        state = self.get_guild_state(ctx.guild.id)

        if state['queue'].is_empty():
            await ctx.send(embed=create_error_embed("Error", "La cola está vacía."))
            return

        state['queue'].shuffle()
        await ctx.send(embed=create_success_embed("Cola mezclada", "🔀 La cola ha sido mezclada aleatoriamente."))

    @commands.command(name='remove', aliases=['rm'])
    async def remove(self, ctx, index: int):
        """
        Eliminar canción de la cola

        Uso: !remove 3
        """
        state = self.get_guild_state(ctx.guild.id)

        # Convert to 0-based index
        if state['queue'].remove(index - 1):
            await ctx.send(embed=create_success_embed("Eliminado", f"🗑️ Canción #{index} eliminada de la cola."))
        else:
            await ctx.send(embed=create_error_embed("Error", "Índice inválido."))

    @commands.command(name='clear')
    async def clear(self, ctx):
        """Limpiar toda la cola"""
        state = self.get_guild_state(ctx.guild.id)

        if state['queue'].is_empty():
            await ctx.send(embed=create_error_embed("Error", "La cola ya está vacía."))
            return

        state['queue'].clear()
        await ctx.send(embed=create_success_embed("Cola limpiada", "🗑️ Se limpiaron todas las canciones de la cola."))

    @commands.command(name='jump')
    async def jump(self, ctx, position: int):
        """
        Saltar a una canción específica en la cola

        Uso: !jump 5
        """
        state = self.get_guild_state(ctx.guild.id)

        if position < 1 or position > len(state['queue']):
            await ctx.send(embed=create_error_embed("Error", "Posición inválida."))
            return

        # Detener canción actual
        if state['voice_client'] and state['voice_client'].is_playing():
            state['voice_client'].stop()

        # Saltar a la posición
        song = state['queue'].jump_to(position - 1)

        if song:
            await ctx.send(embed=create_success_embed("Saltando", f"⏩ Saltando a: **{song.title}**"))
        else:
            await ctx.send(embed=create_error_embed("Error", "Error saltando a la canción."))

    @commands.command(name='move')
    async def move(self, ctx, from_pos: int, to_pos: int):
        """
        Mover canción a otra posición

        Uso: !move 5 2
        """
        state = self.get_guild_state(ctx.guild.id)

        if state['queue'].move(from_pos - 1, to_pos - 1):
            await ctx.send(embed=create_success_embed(
                "Movido",
                f"↕️ Canción movida de posición {from_pos} a {to_pos}."
            ))
        else:
            await ctx.send(embed=create_error_embed("Error", "Posiciones inválidas."))

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Ver latencia del bot"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(embed=create_success_embed("Pong!", f"🏓 Latencia: {latency}ms"))

    @commands.command(name='autoshuffle')
    async def autoshuffle(self, ctx, enabled: bool = None):
        """
        Activar/desactivar auto-shuffle para playlists
        Cuando está activo, las playlists se mezclan automáticamente

        Uso:
            !autoshuffle        - Ver estado actual
            !autoshuffle on     - Activar
            !autoshuffle off    - Desactivar
        """
        state = self.get_guild_state(ctx.guild.id)

        if enabled is None:
            # Mostrar estado actual
            current = state.get('auto_shuffle', True)
            status = "✅ Activado" if current else "❌ Desactivado"
            await ctx.send(embed=create_success_embed(
                "Auto-Shuffle",
                f"Estado actual: {status}\n\nLas playlists {'se mezclarán' if current else 'NO se mezclarán'} automáticamente al añadirlas."
            ))
        else:
            # Cambiar estado
            state['auto_shuffle'] = enabled
            status = "✅ Activado" if enabled else "❌ Desactivado"
            await ctx.send(embed=create_success_embed(
                "Auto-Shuffle Configurado",
                f"{status}\n\nLas playlists ahora {'se mezclarán' if enabled else 'NO se mezclarán'} automáticamente."
            ))


async def setup(bot):
    await bot.add_cog(Music(bot))
