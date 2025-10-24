"""
Admin Cog - Comandos administrativos y estadísticas
Implementa: help, stats, prefix (futuro), configuración del servidor
"""
import discord
from discord.ext import commands
import logging
import time
from datetime import datetime

from ..utils.embeds import (
    create_stats_embed,
    create_info_embed,
    create_error_embed
)
from ..config.settings import Settings


logger = logging.getLogger('MusicBot.Admin')


class Admin(commands.Cog):
    """Comandos administrativos y de información"""

    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.songs_played = 0
        self.commands_executed = 0

    @commands.command(name='help', aliases=['h', 'commands'])
    async def help(self, ctx, command: str = None):
        """
        Mostrar lista de comandos

        Uso:
            !help          - Mostrar todos los comandos
            !help <cmd>    - Ayuda específica de un comando
        """
        if command:
            # Ayuda específica de un comando
            cmd = self.bot.get_command(command)
            if cmd:
                embed = discord.Embed(
                    title=f"📖 Ayuda: {cmd.name}",
                    description=cmd.help or "Sin descripción",
                    color=discord.Color.blue()
                )

                if cmd.aliases:
                    embed.add_field(
                        name="Aliases",
                        value=", ".join([f"`{a}`" for a in cmd.aliases]),
                        inline=False
                    )

                if cmd.usage:
                    embed.add_field(
                        name="Uso",
                        value=f"`{Settings.PREFIX}{cmd.name} {cmd.usage}`",
                        inline=False
                    )

                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=create_error_embed("Error", f"Comando `{command}` no encontrado."))
            return

        # Ayuda general
        embed = discord.Embed(
            title="🎵 Discord Music Bot - Comandos",
            description=f"Prefijo: `{Settings.PREFIX}`\n\nUsa `{Settings.PREFIX}help <comando>` para más información sobre un comando específico.",
            color=discord.Color.purple()
        )

        # Comandos de Música
        music_commands = [
            f"`{Settings.PREFIX}play` / `p` - Reproducir música",
            f"`{Settings.PREFIX}pause` - Pausar reproducción",
            f"`{Settings.PREFIX}resume` - Reanudar reproducción",
            f"`{Settings.PREFIX}skip` / `s` - Saltar canción",
            f"`{Settings.PREFIX}stop` - Detener y limpiar cola",
            f"`{Settings.PREFIX}volume` / `vol` - Ajustar volumen (0-100)",
            f"`{Settings.PREFIX}nowplaying` / `np` - Canción actual",
            f"`{Settings.PREFIX}queue` / `q` - Ver cola",
            f"`{Settings.PREFIX}loop` - Configurar repetición",
            f"`{Settings.PREFIX}shuffle` - Mezclar cola",
            f"`{Settings.PREFIX}join` / `j` - Unirse a voz",
            f"`{Settings.PREFIX}leave` / `dc` - Salir de voz"
        ]

        embed.add_field(
            name="🎵 Reproducción de Música",
            value="\n".join(music_commands),
            inline=False
        )

        # Comandos de Cola
        queue_commands = [
            f"`{Settings.PREFIX}remove` / `rm` - Eliminar canción de cola",
            f"`{Settings.PREFIX}clear` - Limpiar toda la cola",
            f"`{Settings.PREFIX}jump` - Saltar a canción específica",
            f"`{Settings.PREFIX}move` - Mover canción de posición"
        ]

        embed.add_field(
            name="📝 Gestión de Cola",
            value="\n".join(queue_commands),
            inline=False
        )

        # Comandos de Favoritos
        fav_commands = [
            f"`{Settings.PREFIX}favorite` / `fav` - Añadir a favoritos",
            f"`{Settings.PREFIX}favorites` / `favs` - Ver favoritos",
            f"`{Settings.PREFIX}playfavorite` / `pf` - Reproducir favorito",
            f"`{Settings.PREFIX}removefavorite` / `rmfav` - Eliminar favorito",
            f"`{Settings.PREFIX}playallfavs` - Reproducir todos los favoritos"
        ]

        embed.add_field(
            name="❤️ Favoritos",
            value="\n".join(fav_commands),
            inline=False
        )

        # Comandos de Información
        info_commands = [
            f"`{Settings.PREFIX}help` / `h` - Mostrar esta ayuda",
            f"`{Settings.PREFIX}stats` - Estadísticas del bot",
            f"`{Settings.PREFIX}ping` - Ver latencia"
        ]

        embed.add_field(
            name="ℹ️ Información",
            value="\n".join(info_commands),
            inline=False
        )

        embed.set_footer(text="🎵 Bot de música gratuito | GitHub: https://github.com/tu-repo")

        await ctx.send(embed=embed)

    @commands.command(name='stats', aliases=['statistics'])
    async def stats(self, ctx):
        """Mostrar estadísticas del bot"""
        # Calcular uptime
        uptime_seconds = int(time.time() - self.start_time)
        uptime_hours = uptime_seconds // 3600
        uptime_minutes = (uptime_seconds % 3600) // 60
        uptime_str = f"{uptime_hours}h {uptime_minutes}m"

        # Calcular estadísticas
        total_servers = len(self.bot.guilds)
        total_users = sum(guild.member_count for guild in self.bot.guilds)

        # Contar servidores activos (con bot en voz)
        active_servers = 0
        music_cog = self.bot.get_cog('Music')
        if music_cog:
            for guild_id, state in music_cog.guild_states.items():
                if state.get('voice_client') and state['voice_client'].is_connected():
                    active_servers += 1

        stats = {
            'songs_played': self.songs_played,
            'total_time': uptime_str,
            'active_servers': active_servers,
            'total_users': total_users
        }

        embed = create_stats_embed(stats)

        # Añadir información adicional
        embed.add_field(
            name="💿 Total de Servidores",
            value=str(total_servers),
            inline=True
        )

        embed.add_field(
            name="🏓 Latencia",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=True
        )

        embed.add_field(
            name="⏱️ Uptime",
            value=uptime_str,
            inline=True
        )

        embed.add_field(
            name="🔧 Versión",
            value="v1.0.0",
            inline=True
        )

        embed.add_field(
            name="🐍 Python",
            value="3.11+",
            inline=True
        )

        embed.add_field(
            name="📚 discord.py",
            value="2.3+",
            inline=True
        )

        embed.set_footer(text=f"Bot iniciado: {datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')}")

        await ctx.send(embed=embed)

    @commands.command(name='info', aliases=['about', 'botinfo'])
    async def info(self, ctx):
        """Información sobre el bot"""
        embed = discord.Embed(
            title="🎵 Discord Music Bot",
            description="Bot de música gratuito y open source para Discord.\nReproducción desde YouTube y Spotify.",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="✨ Características",
            value="• Reproducción desde YouTube\n• Soporte de Spotify\n• Sistema de cola avanzado\n• Favoritos personalizados\n• Loop y Shuffle\n• 100% Gratuito",
            inline=False
        )

        embed.add_field(
            name="🔗 Enlaces",
            value="[GitHub](https://github.com/tu-repo) | [Documentación](https://github.com/tu-repo/blob/main/README.md) | [Invitar Bot](https://discord.com/oauth2/authorize...)",
            inline=False
        )

        embed.add_field(
            name="💡 Tecnologías",
            value="Python 3.11 • discord.py • yt-dlp • spotipy • FFmpeg",
            inline=False
        )

        embed.add_field(
            name="📊 Estadísticas",
            value=f"Servidores: {len(self.bot.guilds)} | Usuarios: {sum(g.member_count for g in self.bot.guilds)}",
            inline=False
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Hecho con ❤️ | Usa {Settings.PREFIX}help para ver comandos")

        await ctx.send(embed=embed)

    @commands.command(name='invite')
    async def invite(self, ctx):
        """Obtener enlace de invitación del bot"""
        # Generar URL de invitación
        permissions = discord.Permissions(
            send_messages=True,
            embed_links=True,
            attach_files=True,
            add_reactions=True,
            use_external_emojis=True,
            read_message_history=True,
            connect=True,
            speak=True,
            use_voice_activation=True
        )

        invite_url = discord.utils.oauth_url(
            self.bot.user.id,
            permissions=permissions
        )

        embed = discord.Embed(
            title="📨 Invitar Bot",
            description=f"¡Gracias por tu interés!\n\n[Haz clic aquí para invitar el bot a tu servidor]({invite_url})",
            color=discord.Color.green()
        )

        embed.add_field(
            name="⚠️ Permisos Requeridos",
            value="• Enviar mensajes\n• Conectar a voz\n• Hablar\n• Añadir reacciones",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name='support', aliases=['server'])
    async def support(self, ctx):
        """Enlace al servidor de soporte"""
        embed = discord.Embed(
            title="💬 Servidor de Soporte",
            description="¿Necesitas ayuda? ¡Únete a nuestro servidor de Discord!\n\n[Enlace al servidor](https://discord.gg/tu-servidor)",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📝 También puedes:",
            value="• Reportar bugs en [GitHub](https://github.com/tu-repo/issues)\n• Leer la [Documentación](https://github.com/tu-repo)",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Contador de comandos ejecutados"""
        self.commands_executed += 1

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Manejo de errores de comandos"""
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=create_error_embed(
                "Argumento faltante",
                f"Falta el argumento: `{error.param.name}`\nUsa `{Settings.PREFIX}help {ctx.command.name}` para más información."
            ))
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send(embed=create_error_embed(
                "Argumento inválido",
                f"{str(error)}\nUsa `{Settings.PREFIX}help {ctx.command.name}` para más información."
            ))
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=create_error_embed(
                "Cooldown",
                f"Espera {error.retry_after:.1f} segundos antes de usar este comando de nuevo."
            ))
            return

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=create_error_embed(
                "Permisos insuficientes",
                "No tienes permisos para usar este comando."
            ))
            return

        # Error no manejado
        logger.error(f'Unhandled error in command {ctx.command}: {error}', exc_info=error)
        await ctx.send(embed=create_error_embed(
            "Error",
            f"Ocurrió un error inesperado: {str(error)}"
        ))


async def setup(bot):
    await bot.add_cog(Admin(bot))
