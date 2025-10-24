"""
Discord Music Bot - Punto de entrada principal
Bot de música gratuito con soporte para YouTube y Spotify
"""
import os
import asyncio
import logging
import discord
from discord.ext import commands
from aiohttp import web

from .config.settings import Settings


# Configurar logging
logging.basicConfig(
    level=getattr(logging, Settings.LOG_LEVEL),
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('MusicBot')


class MusicBot(commands.Bot):
    """Bot principal de música para Discord"""

    def __init__(self):
        """Inicializar el bot con configuración"""
        # Configurar intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.guilds = True

        super().__init__(
            command_prefix=Settings.PREFIX,
            intents=intents,
            help_command=None  # Usaremos nuestro propio comando help
        )

        self.initial_extensions = [
            'src.cogs.music',
            'src.cogs.playlist',
            'src.cogs.admin',
            'src.cogs.radio'
        ]

    async def setup_hook(self):
        """Cargar extensiones al iniciar"""
        logger.info('🔧 Cargando extensiones...')

        for ext in self.initial_extensions:
            try:
                await self.load_extension(ext)
                logger.info(f'✅ Cargado: {ext}')
            except Exception as e:
                logger.error(f'❌ Error cargando {ext}: {e}')

    async def on_ready(self):
        """Evento cuando el bot está listo"""
        logger.info('=' * 50)
        logger.info(f'✅ Bot conectado como {self.user}')
        logger.info(f'📊 ID: {self.user.id}')
        logger.info(f'💿 Servidores: {len(self.guilds)}')
        logger.info(f'👥 Usuarios: {sum(g.member_count for g in self.guilds)}')
        logger.info(f'🎵 Prefijo: {Settings.PREFIX}')
        logger.info('=' * 50)

        # Establecer estado del bot
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{Settings.PREFIX}help | 🎵 Music Bot"
            ),
            status=discord.Status.online
        )

        logger.info('✨ Bot listo para recibir comandos')

    async def on_guild_join(self, guild):
        """Evento cuando el bot se une a un servidor"""
        logger.info(f'➕ Bot añadido al servidor: {guild.name} (ID: {guild.id})')

        # Intentar enviar mensaje de bienvenida al primer canal disponible
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="🎵 ¡Gracias por añadirme!",
                    description=f"Hola, soy un bot de música gratuito.\n\nUsa `{Settings.PREFIX}help` para ver todos mis comandos.\nUsa `{Settings.PREFIX}play <canción>` para empezar a reproducir música.",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="🚀 Inicio Rápido",
                    value=f"1. Únete a un canal de voz\n2. Usa `{Settings.PREFIX}play <nombre o URL>`\n3. ¡Disfruta de la música!",
                    inline=False
                )
                embed.set_footer(text="Bot de música 100% gratuito y open source")

                try:
                    await channel.send(embed=embed)
                    break
                except:
                    continue

    async def on_guild_remove(self, guild):
        """Evento cuando el bot es removido de un servidor"""
        logger.info(f'➖ Bot removido del servidor: {guild.name} (ID: {guild.id})')

    async def on_command(self, ctx):
        """Evento cuando se ejecuta un comando"""
        logger.info(f'📝 Comando: {ctx.command} | Usuario: {ctx.author} | Servidor: {ctx.guild}')

    async def on_command_error(self, ctx, error):
        """Manejo global de errores"""
        # El manejo detallado de errores está en el Admin Cog
        # Aquí solo manejamos errores críticos
        if isinstance(error, commands.CommandNotFound):
            return

        logger.error(f'❌ Error en comando {ctx.command}: {error}', exc_info=error)


async def run_health_server():
    """
    Servidor HTTP para health checks
    Mantiene el bot activo en plataformas gratuitas como Railway/Render
    """
    app = web.Application()

    async def health_check(request):
        """Endpoint de health check"""
        return web.Response(text="Bot is alive! 🎵")

    async def root(request):
        """Endpoint raíz con información"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Discord Music Bot</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #2c2f33;
                    color: #ffffff;
                }
                h1 { color: #7289da; }
                .status { color: #43b581; }
                a { color: #7289da; }
            </style>
        </head>
        <body>
            <h1>🎵 Discord Music Bot</h1>
            <p class="status">✅ Bot is online and running!</p>
            <p>Un bot de música gratuito para Discord con soporte de YouTube y Spotify.</p>
            <h2>Enlaces:</h2>
            <ul>
                <li><a href="https://github.com/tu-repo">GitHub Repository</a></li>
                <li><a href="https://github.com/tu-repo/blob/main/README.md">Documentación</a></li>
            </ul>
        </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')

    # Registrar rutas
    app.router.add_get('/', root)
    app.router.add_get('/health', health_check)
    app.router.add_get('/ping', health_check)

    # Crear runner
    runner = web.AppRunner(app)
    await runner.setup()

    # Iniciar sitio
    site = web.TCPSite(
        runner,
        Settings.HEALTH_CHECK_HOST,
        Settings.HEALTH_CHECK_PORT
    )

    await site.start()

    logger.info(f'🌐 Health check server running on http://{Settings.HEALTH_CHECK_HOST}:{Settings.HEALTH_CHECK_PORT}')


async def main():
    """Función principal para iniciar el bot"""
    # Validar configuración
    if not Settings.validate():
        logger.error('❌ Configuración inválida. Verifica tus variables de entorno.')
        return

    logger.info('🚀 Iniciando Discord Music Bot...')
    logger.info(f'🎵 Prefijo: {Settings.PREFIX}')
    logger.info(f'📊 Max queue size: {Settings.MAX_QUEUE_SIZE}')
    logger.info(f'🔊 Default volume: {Settings.DEFAULT_VOLUME}%')

    # Mostrar información de configuración
    config_info = Settings.get_info()
    logger.info('⚙️  Configuración:')
    for key, value in config_info.items():
        logger.info(f'   {key}: {value}')

    # Crear bot
    bot = MusicBot()

    try:
        # Iniciar health check server en background
        asyncio.create_task(run_health_server())

        # Iniciar bot
        async with bot:
            await bot.start(Settings.DISCORD_TOKEN)

    except KeyboardInterrupt:
        logger.info('👋 Bot detenido por el usuario')
    except Exception as e:
        logger.error(f'❌ Error fatal: {e}', exc_info=e)
    finally:
        logger.info('🛑 Bot apagado')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('👋 Programa terminado por el usuario')
