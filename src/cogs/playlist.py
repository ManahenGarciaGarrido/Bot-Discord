"""
Playlist Cog - Gestión de favoritos y playlists personalizadas
Implementa: favorite, favorites, playfavorite, removefavorite, playallfavs
"""
import discord
from discord.ext import commands
import aiosqlite
import logging
from typing import List, Dict

from ..utils.embeds import (
    create_favorites_embed,
    create_error_embed,
    create_success_embed
)
from ..config.settings import Settings


logger = logging.getLogger('MusicBot.Playlist')


class Playlist(commands.Cog):
    """Gestión de canciones favoritas por usuario"""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = Settings.DATABASE_PATH
        self.bot.loop.create_task(self._init_database())

    async def _init_database(self):
        """Inicializar base de datos SQLite"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    CREATE TABLE IF NOT EXISTS favorites (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        guild_id INTEGER NOT NULL,
                        title TEXT NOT NULL,
                        url TEXT NOT NULL,
                        thumbnail TEXT,
                        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, guild_id, url)
                    )
                ''')
                await db.commit()
                logger.info('✅ Favorites database initialized')
        except Exception as e:
            logger.error(f'Error initializing database: {e}')

    async def get_favorites(self, user_id: int, guild_id: int) -> List[Dict]:
        """
        Obtener favoritos de un usuario en un servidor

        Args:
            user_id: ID del usuario de Discord
            guild_id: ID del servidor de Discord

        Returns:
            List[Dict]: Lista de favoritos
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    'SELECT * FROM favorites WHERE user_id = ? AND guild_id = ? ORDER BY added_date DESC',
                    (user_id, guild_id)
                ) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f'Error getting favorites: {e}')
            return []

    async def add_favorite(self, user_id: int, guild_id: int, title: str, url: str, thumbnail: str = None) -> bool:
        """
        Añadir canción a favoritos

        Args:
            user_id: ID del usuario
            guild_id: ID del servidor
            title: Título de la canción
            url: URL de la canción
            thumbnail: URL del thumbnail (opcional)

        Returns:
            bool: True si se añadió, False si ya existe o hay error
        """
        try:
            # Verificar límite de favoritos
            favorites = await self.get_favorites(user_id, guild_id)
            if len(favorites) >= Settings.MAX_FAVORITES_PER_USER:
                return False

            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'INSERT OR IGNORE INTO favorites (user_id, guild_id, title, url, thumbnail) VALUES (?, ?, ?, ?, ?)',
                    (user_id, guild_id, title, url, thumbnail)
                )
                await db.commit()
                return True
        except Exception as e:
            logger.error(f'Error adding favorite: {e}')
            return False

    async def remove_favorite(self, user_id: int, guild_id: int, index: int) -> bool:
        """
        Eliminar favorito por índice

        Args:
            user_id: ID del usuario
            guild_id: ID del servidor
            index: Índice del favorito (1-based)

        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            favorites = await self.get_favorites(user_id, guild_id)

            if index < 1 or index > len(favorites):
                return False

            fav = favorites[index - 1]

            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'DELETE FROM favorites WHERE id = ?',
                    (fav['id'],)
                )
                await db.commit()
                return True
        except Exception as e:
            logger.error(f'Error removing favorite: {e}')
            return False

    @commands.command(name='favorite', aliases=['fav', '♥'])
    async def favorite(self, ctx):
        """Añadir canción actual a favoritos"""
        # Obtener canción actual del Music Cog
        music_cog = self.bot.get_cog('Music')
        if not music_cog:
            await ctx.send(embed=create_error_embed("Error", "Cog de música no encontrado."))
            return

        state = music_cog.get_guild_state(ctx.guild.id)
        current_song = state.get('current_song')

        if not current_song:
            await ctx.send(embed=create_error_embed("Error", "No hay ninguna canción reproduciéndose."))
            return

        # Añadir a favoritos
        success = await self.add_favorite(
            ctx.author.id,
            ctx.guild.id,
            current_song.title,
            current_song.url,
            current_song.thumbnail
        )

        if success:
            await ctx.send(embed=create_success_embed(
                "Añadido a favoritos",
                f"❤️ **{current_song.title}** fue añadido a tus favoritos."
            ))
        else:
            await ctx.send(embed=create_error_embed(
                "Error",
                "No se pudo añadir a favoritos. Puede que ya esté en tu lista o hayas alcanzado el límite."
            ))

    @commands.command(name='favorites', aliases=['favs', 'flist'])
    async def favorites(self, ctx):
        """Ver lista de favoritos"""
        favorites = await self.get_favorites(ctx.author.id, ctx.guild.id)

        embed = create_favorites_embed(favorites, ctx.author.display_name)
        await ctx.send(embed=embed)

    @commands.command(name='playfavorite', aliases=['playfav', 'pf'])
    async def playfavorite(self, ctx, index: int):
        """
        Reproducir canción desde favoritos

        Uso: !playfav 1
        """
        favorites = await self.get_favorites(ctx.author.id, ctx.guild.id)

        if index < 1 or index > len(favorites):
            await ctx.send(embed=create_error_embed("Error", "Índice inválido."))
            return

        fav = favorites[index - 1]

        # Usar el comando play del Music Cog
        music_cog = self.bot.get_cog('Music')
        if not music_cog:
            await ctx.send(embed=create_error_embed("Error", "Cog de música no encontrado."))
            return

        # Invocar comando play con la URL del favorito
        await ctx.invoke(self.bot.get_command('play'), query=fav['url'])

    @commands.command(name='removefavorite', aliases=['rmfav'])
    async def removefavorite(self, ctx, index: int):
        """
        Eliminar canción de favoritos

        Uso: !rmfav 2
        """
        success = await self.remove_favorite(ctx.author.id, ctx.guild.id, index)

        if success:
            await ctx.send(embed=create_success_embed(
                "Eliminado",
                f"🗑️ Canción #{index} eliminada de tus favoritos."
            ))
        else:
            await ctx.send(embed=create_error_embed("Error", "Índice inválido o error al eliminar."))

    @commands.command(name='playallfavs')
    async def playallfavs(self, ctx):
        """Reproducir todos los favoritos"""
        favorites = await self.get_favorites(ctx.author.id, ctx.guild.id)

        if not favorites:
            await ctx.send(embed=create_error_embed("Error", "No tienes canciones favoritas."))
            return

        # Obtener Music Cog
        music_cog = self.bot.get_cog('Music')
        if not music_cog:
            await ctx.send(embed=create_error_embed("Error", "Cog de música no encontrado."))
            return

        # Añadir todos los favoritos a la cola
        await ctx.send(embed=create_success_embed(
            "Añadiendo favoritos",
            f"🎵 Añadiendo {len(favorites)} canciones a la cola..."
        ))

        for fav in favorites:
            await ctx.invoke(self.bot.get_command('play'), query=fav['url'])

    @commands.command(name='clearfavorites', aliases=['clearfavs'])
    async def clearfavorites(self, ctx):
        """Limpiar todos los favoritos (requiere confirmación)"""
        # Pedir confirmación
        embed = discord.Embed(
            title="⚠️ Confirmación requerida",
            description="¿Estás seguro de que quieres eliminar TODOS tus favoritos?\nReacciona con ✅ para confirmar.",
            color=discord.Color.orange()
        )
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❌')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == message.id

        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

            if str(reaction.emoji) == '✅':
                # Eliminar todos los favoritos
                try:
                    async with aiosqlite.connect(self.db_path) as db:
                        await db.execute(
                            'DELETE FROM favorites WHERE user_id = ? AND guild_id = ?',
                            (ctx.author.id, ctx.guild.id)
                        )
                        await db.commit()

                    await message.delete()
                    await ctx.send(embed=create_success_embed(
                        "Favoritos eliminados",
                        "🗑️ Todos tus favoritos han sido eliminados."
                    ))
                except Exception as e:
                    logger.error(f'Error clearing favorites: {e}')
                    await ctx.send(embed=create_error_embed("Error", "Error al eliminar favoritos."))
            else:
                await message.delete()
                await ctx.send(embed=create_success_embed("Cancelado", "Operación cancelada."))

        except Exception:
            await message.delete()
            await ctx.send(embed=create_error_embed("Tiempo agotado", "Operación cancelada por tiempo."))


async def setup(bot):
    await bot.add_cog(Playlist(bot))
