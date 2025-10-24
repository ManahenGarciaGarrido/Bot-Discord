"""
Radio Cog - Sistema de radio inteligente y recomendaciones
Implementa: like, dislike, radio, recommendations, smart shuffle
"""
import discord
from discord.ext import commands
import logging
from typing import Optional

from ..utils.preferences_db import PreferencesDB
from ..utils.recommendation_engine import RecommendationEngine
from ..utils.youtube_handler import YouTubeHandler
from ..utils.song import Song
from ..utils.embeds import (
    create_success_embed,
    create_error_embed,
    create_info_embed
)
from ..config.settings import Settings


logger = logging.getLogger('MusicBot.Radio')


class Radio(commands.Cog):
    """Comandos de radio inteligente, likes/dislikes y recomendaciones"""

    def __init__(self, bot):
        self.bot = bot
        self.prefs_db = PreferencesDB()
        self.youtube = YouTubeHandler()
        self.recommendation_engine = RecommendationEngine(self.prefs_db, self.youtube)
        self.bot.loop.create_task(self.prefs_db.init_database())

        # Estado de radio por servidor
        self.radio_states = {}  # {guild_id: {'active': bool, 'user_id': int}}

    def get_radio_state(self, guild_id):
        """Obtener o crear estado de radio del servidor"""
        if guild_id not in self.radio_states:
            self.radio_states[guild_id] = {
                'active': False,
                'user_id': None
            }
        return self.radio_states[guild_id]

    @commands.command(name='like', aliases=['👍', 'love'])
    async def like(self, ctx):
        """
        Dar like a la canción actual
        El bot aprenderá de tus gustos y recomendará música similar
        """
        # Obtener canción actual del Music Cog
        music_cog = self.bot.get_cog('Music')
        if not music_cog:
            await ctx.send(embed=create_error_embed("Error", "Sistema de música no disponible."))
            return

        state = music_cog.get_guild_state(ctx.guild.id)
        current_song = state.get('current_song')

        if not current_song:
            await ctx.send(embed=create_error_embed("Error", "No hay ninguna canción reproduciéndose."))
            return

        # Guardar like en la base de datos
        success = await self.prefs_db.add_rating(
            ctx.author.id,
            ctx.guild.id,
            current_song.title,
            current_song.url,
            rating=1,  # 1 = like
            artist=current_song.uploader
        )

        if success:
            embed = create_success_embed(
                "¡Te gustó!",
                f"👍 **{current_song.title}**\n\nEl bot recordará que te gusta esta canción y {current_song.uploader}."
            )
            embed.set_thumbnail(url=current_song.thumbnail)
            await ctx.send(embed=embed)

            logger.info(f'User {ctx.author} liked: {current_song.title}')
        else:
            await ctx.send(embed=create_error_embed("Error", "No se pudo guardar tu preferencia."))

    @commands.command(name='dislike', aliases=['👎', 'hate'])
    async def dislike(self, ctx):
        """
        Dar dislike a la canción actual
        El bot evitará reproducir canciones similares
        """
        music_cog = self.bot.get_cog('Music')
        if not music_cog:
            await ctx.send(embed=create_error_embed("Error", "Sistema de música no disponible."))
            return

        state = music_cog.get_guild_state(ctx.guild.id)
        current_song = state.get('current_song')

        if not current_song:
            await ctx.send(embed=create_error_embed("Error", "No hay ninguna canción reproduciéndose."))
            return

        # Guardar dislike
        success = await self.prefs_db.add_rating(
            ctx.author.id,
            ctx.guild.id,
            current_song.title,
            current_song.url,
            rating=-1,  # -1 = dislike
            artist=current_song.uploader
        )

        if success:
            embed = create_success_embed(
                "No te gustó",
                f"👎 **{current_song.title}**\n\nEl bot evitará reproducir canciones de {current_song.uploader} en el futuro."
            )
            embed.set_thumbnail(url=current_song.thumbnail)
            await ctx.send(embed=embed)

            # Auto-skip si está en modo radio
            radio_state = self.get_radio_state(ctx.guild.id)
            if radio_state['active']:
                await ctx.send(embed=create_info_embed("Auto-Skip", "⏭️ Saltando canción automáticamente..."))
                if state['voice_client'] and state['voice_client'].is_playing():
                    state['voice_client'].stop()

            logger.info(f'User {ctx.author} disliked: {current_song.title}')
        else:
            await ctx.send(embed=create_error_embed("Error", "No se pudo guardar tu preferencia."))

    @commands.command(name='radio', aliases=['autoplay', 'smartplay'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def radio(self, ctx, *, genre: str = None):
        """
        Activar modo Radio inteligente
        Reproducción continua basada en tus gustos musicales

        Uso:
            !radio              - Radio personalizada basada en tus gustos
            !radio rock         - Radio de rock
            !radio chill vibes  - Radio de música relajante
            !radio hits 2010    - Radio de hits del 2010
        """
        music_cog = self.bot.get_cog('Music')
        if not music_cog:
            await ctx.send(embed=create_error_embed("Error", "Sistema de música no disponible."))
            return

        # Verificar que el usuario esté en voz
        if not ctx.author.voice:
            await ctx.send(embed=create_error_embed("Error", "Debes estar en un canal de voz."))
            return

        # Unir a canal de voz si no está conectado
        if not await music_cog.join_voice_channel(ctx):
            return

        state = music_cog.get_guild_state(ctx.guild.id)
        radio_state = self.get_radio_state(ctx.guild.id)

        # Activar modo radio
        radio_state['active'] = True
        radio_state['user_id'] = ctx.author.id

        await ctx.send(embed=create_info_embed(
            "🎵 Modo Radio Activado",
            f"Generando cola de reproducción{'personalizada' if not genre else f' de {genre}'}...\n\nUsa `!like` 👍 y `!dislike` 👎 para mejorar las recomendaciones."
        ))

        async with ctx.typing():
            # Generar cola de radio
            if genre:
                # Buscar playlist relacionada con el género
                playlists = await self.recommendation_engine.find_playlist_by_query(genre, limit=1)

                if playlists:
                    # Obtener canciones de la playlist
                    playlist_url = playlists[0].get('webpage_url') or playlists[0].get('url')
                    songs_data = await self.youtube.get_playlist(playlist_url, max_songs=20)

                    # Añadir a la cola
                    for song_data in songs_data:
                        song = Song.from_youtube_info(song_data, ctx.author)
                        state['queue'].add(song)
                else:
                    # Si no encuentra playlist, buscar canciones individuales
                    results = await self.youtube.search(f"{genre} music", limit=10)
                    for result in results:
                        song = Song.from_youtube_info(result, ctx.author)
                        state['queue'].add(song)
            else:
                # Radio personalizada basada en gustos del usuario
                radio_queue = await self.recommendation_engine.generate_radio_queue(
                    ctx.author.id,
                    ctx.guild.id,
                    queue_size=20
                )

                if not radio_queue:
                    await ctx.send(embed=create_error_embed(
                        "Sin preferencias",
                        "No tengo suficiente información sobre tus gustos. Usa `!like` en canciones que te gusten primero, o prueba `!radio <género>`."
                    ))
                    radio_state['active'] = False
                    return

                # Añadir canciones a la cola
                for song_data in radio_queue:
                    song = Song.from_youtube_info(song_data, ctx.author)
                    state['queue'].add(song)

            # Si no hay nada reproduciéndose, empezar
            if not state['voice_client'].is_playing():
                await music_cog._play_next(ctx.guild.id)

            embed = create_success_embed(
                "🎵 Radio Iniciada",
                f"{'Personalizada' if not genre else genre.capitalize()} • {len(state['queue'].get_queue())} canciones en cola\n\n"
                f"👍 `!like` - Me gusta\n"
                f"👎 `!dislike` - No me gusta\n"
                f"⏭️ `!skip` - Siguiente\n"
                f"🛑 `!radiooff` - Desactivar radio"
            )
            await ctx.send(embed=embed)

    @commands.command(name='radiooff', aliases=['stopradio'])
    async def radiooff(self, ctx):
        """Desactivar modo Radio"""
        radio_state = self.get_radio_state(ctx.guild.id)

        if not radio_state['active']:
            await ctx.send(embed=create_error_embed("Error", "El modo Radio no está activo."))
            return

        radio_state['active'] = False
        radio_state['user_id'] = None

        await ctx.send(embed=create_success_embed(
            "Radio Desactivada",
            "🛑 Modo Radio desactivado. La cola actual seguirá reproduciéndose normalmente."
        ))

    @commands.command(name='mypreferences', aliases=['myprefs', 'mytaste'])
    async def mypreferences(self, ctx):
        """Ver resumen de tus preferencias musicales"""
        summary = await self.prefs_db.get_user_preferences_summary(ctx.author.id, ctx.guild.id)

        if not summary or summary.get('liked_songs_count', 0) == 0:
            await ctx.send(embed=create_info_embed(
                "Sin Preferencias",
                "Aún no tienes preferencias guardadas.\n\nUsa `!like` en canciones que te gusten para que el bot aprenda tus gustos musicales."
            ))
            return

        embed = discord.Embed(
            title=f"🎵 Preferencias Musicales de {ctx.author.display_name}",
            color=discord.Color.purple()
        )

        # Canciones con like
        embed.add_field(
            name="👍 Canciones que te gustan",
            value=str(summary.get('liked_songs_count', 0)),
            inline=True
        )

        # Artistas favoritos
        fav_artists = summary.get('favorite_artists', [])
        if fav_artists:
            embed.add_field(
                name="⭐ Artistas Favoritos",
                value="\n".join([f"• {artist}" for artist in fav_artists[:5]]) or "Ninguno",
                inline=False
            )

        # Artistas que no le gustan
        disliked = summary.get('disliked_artists', [])
        if disliked:
            embed.add_field(
                name="👎 Artistas Evitados",
                value="\n".join([f"• {artist}" for artist in disliked[:5]]) or "Ninguno",
                inline=False
            )

        # Top canciones que le gustaron
        top_songs = summary.get('top_liked_songs', [])
        if top_songs:
            songs_text = "\n".join([f"• {song['song_title'][:40]}" for song in top_songs[:5]])
            embed.add_field(
                name="🔝 Top Canciones",
                value=songs_text,
                inline=False
            )

        embed.set_footer(text="Usa !like y !dislike para mejorar las recomendaciones")
        await ctx.send(embed=embed)

    @commands.command(name='recommend', aliases=['reco', 'suggestions'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def recommend(self, ctx, count: int = 5):
        """
        Obtener recomendaciones personalizadas sin iniciar reproducción

        Uso: !recommend [cantidad]
        Ejemplo: !recommend 10
        """
        if count < 1 or count > 20:
            await ctx.send(embed=create_error_embed("Error", "La cantidad debe estar entre 1 y 20."))
            return

        await ctx.send(embed=create_info_embed(
            "Generando Recomendaciones",
            f"🔍 Buscando {count} canciones basadas en tus gustos..."
        ))

        async with ctx.typing():
            recommendations = await self.recommendation_engine.get_recommendations(
                ctx.author.id,
                ctx.guild.id,
                count
            )

            if not recommendations:
                await ctx.send(embed=create_error_embed(
                    "Sin Recomendaciones",
                    "No pude generar recomendaciones. Usa `!like` en canciones que te gusten primero."
                ))
                return

            embed = discord.Embed(
                title="🎵 Recomendaciones Personalizadas",
                description=f"Basado en tus gustos musicales:",
                color=discord.Color.blue()
            )

            for i, song in enumerate(recommendations, 1):
                title = song.get('title', 'Sin título')[:50]
                uploader = song.get('uploader', 'Desconocido')[:30]
                embed.add_field(
                    name=f"{i}. {title}",
                    value=f"👤 {uploader}",
                    inline=False
                )

            embed.set_footer(text="Usa !radio para reproducir música personalizada automáticamente")
            await ctx.send(embed=embed)

    @commands.command(name='findplaylist', aliases=['searchplaylist', 'playlist'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def findplaylist(self, ctx, *, query: str):
        """
        Buscar y reproducir playlists por género o tema

        Ejemplos:
            !findplaylist rock
            !findplaylist hits 2010
            !findplaylist chill vibes
            !findplaylist workout music
        """
        await ctx.send(embed=create_info_embed(
            "Buscando Playlist",
            f"🔍 Buscando playlist de: **{query}**..."
        ))

        async with ctx.typing():
            playlists = await self.recommendation_engine.find_playlist_by_query(query, limit=3)

            if not playlists:
                await ctx.send(embed=create_error_embed(
                    "Sin Resultados",
                    f"No encontré playlists para: **{query}**\n\nIntenta con términos diferentes."
                ))
                return

            # Mostrar resultados para selección
            embed = discord.Embed(
                title="📝 Playlists Encontradas",
                description=f"Búsqueda: **{query}**\n\nReacciona con el número para seleccionar:",
                color=discord.Color.blue()
            )

            emojis = ['1️⃣', '2️⃣', '3️⃣']

            for i, playlist in enumerate(playlists[:3]):
                title = playlist.get('title', 'Sin título')[:60]
                uploader = playlist.get('uploader', 'Desconocido')[:30]

                embed.add_field(
                    name=f"{emojis[i]} {title}",
                    value=f"👤 {uploader}",
                    inline=False
                )

            message = await ctx.send(embed=embed)

            # Añadir reacciones
            for emoji in emojis[:len(playlists)]:
                await message.add_reaction(emoji)

            # Esperar selección
            def check(reaction, user):
                return (user == ctx.author and
                        str(reaction.emoji) in emojis[:len(playlists)] and
                        reaction.message.id == message.id)

            try:
                import asyncio
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                index = emojis.index(str(reaction.emoji))
                selected_playlist = playlists[index]

                await message.delete()

                # Reproducir la playlist seleccionada usando el comando play
                music_cog = self.bot.get_cog('Music')
                if music_cog:
                    playlist_url = selected_playlist.get('webpage_url') or selected_playlist.get('url')
                    await ctx.invoke(self.bot.get_command('play'), query=playlist_url)

            except asyncio.TimeoutError:
                await message.delete()
                await ctx.send(embed=create_error_embed("Tiempo agotado", "Se agotó el tiempo para seleccionar."))


async def setup(bot):
    await bot.add_cog(Radio(bot))
