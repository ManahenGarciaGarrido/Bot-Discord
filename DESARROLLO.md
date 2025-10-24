# 💻 DESARROLLO.md - Guía de Desarrollo

## Tabla de Contenidos
1. [Configuración del Entorno de Desarrollo](#1-configuración-del-entorno-de-desarrollo)
2. [Estructura del Proyecto](#2-estructura-del-proyecto)
3. [Desarrollo de Funcionalidades Core](#3-desarrollo-de-funcionalidades-core)
4. [Testing](#4-testing)
5. [Buenas Prácticas](#5-buenas-prácticas)
6. [Debugging](#6-debugging)

---

## 1. Configuración del Entorno de Desarrollo

### 1.1 Herramientas Recomendadas

#### Editor de Código
- **Visual Studio Code** (recomendado)
  - Extensiones:
    - Python
    - Pylance
    - Discord Developer Tools
    - GitLens

#### Linter y Formatter
```bash
pip install black flake8 pylint

# Formatear código
black src/

# Verificar estilo
flake8 src/
```

### 1.2 Configuración de VSCode

Crear `.vscode/settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.linting.flake8Enabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

---

## 2. Estructura del Proyecto

### 2.1 Estructura Completa

```
discord-music-bot/
│
├── .env                      # Variables de entorno (NO subir a Git)
├── .env.example              # Ejemplo de variables
├── .gitignore                # Archivos a ignorar
├── requirements.txt          # Dependencias Python
├── README.md                 # Documentación principal
├── DESARROLLO.md             # Esta guía
│
├── src/                      # Código fuente
│   ├── __init__.py
│   ├── bot.py                # Punto de entrada principal
│   │
│   ├── cogs/                 # Comandos organizados por categoría
│   │   ├── __init__.py
│   │   ├── music.py          # Comandos de música
│   │   ├── playlist.py       # Gestión de favoritos
│   │   └── admin.py          # Comandos administrativos
│   │
│   ├── utils/                # Utilidades y helpers
│   │   ├── __init__.py
│   │   ├── music_player.py   # Lógica de reproducción
│   │   ├── queue_manager.py  # Gestión de cola
│   │   ├── youtube_handler.py # Interacción con YouTube
│   │   ├── spotify_handler.py # Interacción con Spotify
│   │   ├── song.py           # Modelo de datos
│   │   └── embeds.py         # Creación de embeds
│   │
│   └── config/               # Configuración
│       ├── __init__.py
│       └── settings.py       # Configuración del bot
│
├── tests/                    # Tests unitarios
│   ├── __init__.py
│   ├── test_queue.py
│   └── test_handlers.py
│
└── docs/                     # Documentación adicional
    └── API.md
```

---

## 3. Desarrollo de Funcionalidades Core

### 3.1 Bot Principal (`src/bot.py`)

```python
import os
import asyncio
import logging
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('MusicBot')

# Cargar variables de entorno
load_dotenv()

class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix=os.getenv('PREFIX', '!'),
            intents=intents,
            help_command=None
        )
        
        self.initial_extensions = [
            'cogs.music',
            'cogs.playlist',
            'cogs.admin'
        ]
    
    async def setup_hook(self):
        """Cargar extensiones al iniciar"""
        for ext in self.initial_extensions:
            try:
                await self.load_extension(f'src.{ext}')
                logger.info(f'✅ Cargado: {ext}')
            except Exception as e:
                logger.error(f'❌ Error cargando {ext}: {e}')
    
    async def on_ready(self):
        """Evento cuando el bot está listo"""
        logger.info(f'✅ Bot conectado como {self.user}')
        logger.info(f'📊 Servidores: {len(self.guilds)}')
        logger.info(f'👥 Usuarios: {sum(g.member_count for g in self.guilds)}')
        
        # Establecer estado
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{self.command_prefix}help | 🎵"
            )
        )
    
    async def on_command_error(self, ctx, error):
        """Manejo global de errores"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignorar comandos no encontrados
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'❌ Argumento faltante: `{error.param.name}`')
        
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'❌ Argumento inválido: {error}')
        
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('❌ No tienes permisos para usar este comando.')
        
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'❌ El bot no tiene los permisos necesarios: {error.missing_permissions}')
        
        else:
            logger.error(f'Error no manejado: {error}', exc_info=error)
            await ctx.send(f'❌ Error inesperado: {error}')

async def main():
    """Función principal"""
    bot = MusicBot()
    
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error('❌ DISCORD_TOKEN no encontrado')
        return
    
    async with bot:
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
```

### 3.2 Music Cog (`src/cogs/music.py`)

```python
import discord
from discord.ext import commands
import asyncio
from typing import Optional
import logging

from ..utils.music_player import MusicPlayer
from ..utils.queue_manager import QueueManager
from ..utils.youtube_handler import YouTubeHandler
from ..utils.spotify_handler import SpotifyHandler
from ..utils.song import Song
from ..utils.embeds import create_now_playing_embed, create_queue_embed

logger = logging.getLogger('MusicBot.Music')

class Music(commands.Cog):
    """Comandos de reproducción de música"""
    
    def __init__(self, bot):
        self.bot = bot
        self.youtube_handler = YouTubeHandler()
        self.spotify_handler = SpotifyHandler()
        self.guild_states = {}  # Estado por servidor
    
    def get_guild_state(self, guild_id):
        """Obtener o crear estado del servidor"""
        if guild_id not in self.guild_states:
            self.guild_states[guild_id] = {
                'voice_client': None,
                'queue': QueueManager(),
                'current_song': None,
                'player': None,
                'volume': 0.5,
                'loop_mode': 'off',
                'last_channel': None
            }
        return self.guild_states[guild_id]
    
    async def join_voice_channel(self, ctx):
        """Unir el bot a un canal de voz"""
        state = self.get_guild_state(ctx.guild.id)
        
        # Verificar que el usuario está en voz
        if not ctx.author.voice:
            await ctx.send('❌ Debes estar en un canal de voz.')
            return False
        
        channel = ctx.author.voice.channel
        
        # Si ya está conectado
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
            await ctx.send(f'✅ Conectado a {ctx.author.voice.channel.name}')
    
    @commands.command(name='leave', aliases=['disconnect', 'dc'])
    async def leave(self, ctx):
        """Desconectar el bot del canal de voz"""
        state = self.get_guild_state(ctx.guild.id)
        
        if not state['voice_client']:
            await ctx.send('❌ No estoy en un canal de voz.')
            return
        
        # Limpiar estado
        if state['player']:
            state['player'].stop()
        state['queue'].clear()
        state['current_song'] = None
        
        await state['voice_client'].disconnect()
        state['voice_client'] = None
        
        await ctx.send('👋 Desconectado del canal de voz.')
    
    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, *, query: str):
        """
        Reproducir música desde YouTube o Spotify
        
        Uso:
            !play <URL de YouTube>
            !play <URL de Spotify>
            !play <nombre de canción>
        """
        # Unir al canal de voz si no está conectado
        if not await self.join_voice_channel(ctx):
            return
        
        state = self.get_guild_state(ctx.guild.id)
        state['last_channel'] = ctx.channel
        
        async with ctx.typing():
            # Determinar tipo de input
            if 'youtube.com' in query or 'youtu.be' in query:
                # URL de YouTube
                songs = await self._handle_youtube_url(query, ctx.author)
            
            elif 'spotify.com' in query:
                # URL de Spotify
                songs = await self._handle_spotify_url(query, ctx.author)
            
            else:
                # Búsqueda
                songs = await self._handle_search(ctx, query)
            
            if not songs:
                await ctx.send('❌ No se pudo encontrar la canción.')
                return
            
            # Añadir canciones a la cola
            added_count = 0
            for song in songs:
                if state['queue'].add(song):
                    added_count += 1
            
            # Si no hay nada reproduciéndose, empezar
            if not state['voice_client'].is_playing():
                await self._play_next(ctx.guild.id)
            else:
                # Informar que se añadió a la cola
                if added_count == 1:
                    embed = discord.Embed(
                        title='✅ Añadido a la cola',
                        description=f'**{songs[0].title}**',
                        color=discord.Color.green()
                    )
                    embed.set_thumbnail(url=songs[0].thumbnail)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'✅ {added_count} canciones añadidas a la cola.')
    
    async def _handle_youtube_url(self, url, requester):
        """Manejar URL de YouTube"""
        try:
            info = await self.youtube_handler.extract_info(url)
            
            # Playlist o video individual
            if 'entries' in info:
                # Es una playlist
                songs = []
                for entry in info['entries'][:50]:  # Máximo 50
                    song = Song.from_youtube_info(entry, requester)
                    songs.append(song)
                return songs
            else:
                # Video individual
                song = Song.from_youtube_info(info, requester)
                return [song]
        
        except Exception as e:
            logger.error(f'Error extrayendo YouTube: {e}')
            return None
    
    async def _handle_spotify_url(self, url, requester):
        """Manejar URL de Spotify"""
        try:
            # Obtener info de Spotify
            if 'track' in url:
                track_info = await self.spotify_handler.get_track_info(url)
                query = self.spotify_handler.to_youtube_query(track_info)
                results = await self.youtube_handler.search(query, limit=1)
                if results:
                    song = Song.from_youtube_info(results[0], requester)
                    song.source = 'spotify'
                    return [song]
            
            elif 'playlist' in url or 'album' in url:
                # Playlist o álbum
                if 'playlist' in url:
                    tracks = await self.spotify_handler.get_playlist_tracks(url)
                else:
                    tracks = await self.spotify_handler.get_album_tracks(url)
                
                songs = []
                for track_info in tracks[:50]:  # Máximo 50
                    query = self.spotify_handler.to_youtube_query(track_info)
                    results = await self.youtube_handler.search(query, limit=1)
                    if results:
                        song = Song.from_youtube_info(results[0], requester)
                        song.source = 'spotify'
                        songs.append(song)
                
                return songs
        
        except Exception as e:
            logger.error(f'Error procesando Spotify: {e}')
            return None
    
    async def _handle_search(self, ctx, query):
        """Manejar búsqueda por nombre"""
        try:
            results = await self.youtube_handler.search(query, limit=5)
            
            if not results:
                return None
            
            # Si solo hay un resultado, usarlo directamente
            if len(results) == 1:
                song = Song.from_youtube_info(results[0], ctx.author)
                return [song]
            
            # Mostrar resultados para selección
            embed = discord.Embed(
                title='🔍 Resultados de búsqueda',
                description='Reacciona con el número para seleccionar:',
                color=discord.Color.blue()
            )
            
            emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
            for i, result in enumerate(results[:5]):
                embed.add_field(
                    name=f"{emojis[i]} {result['title'][:50]}",
                    value=f"Duración: {result.get('duration_string', 'N/A')}",
                    inline=False
                )
            
            message = await ctx.send(embed=embed)
            
            # Añadir reacciones
            for emoji in emojis[:len(results)]:
                await message.add_reaction(emoji)
            
            # Esperar reacción del usuario
            def check(reaction, user):
                return (user == ctx.author and 
                        str(reaction.emoji) in emojis[:len(results)] and
                        reaction.message.id == message.id)
            
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                index = emojis.index(str(reaction.emoji))
                song = Song.from_youtube_info(results[index], ctx.author)
                await message.delete()
                return [song]
            
            except asyncio.TimeoutError:
                await message.delete()
                await ctx.send('⏱️ Tiempo de selección agotado.')
                return None
        
        except Exception as e:
            logger.error(f'Error en búsqueda: {e}')
            return None
    
    async def _play_next(self, guild_id):
        """Reproducir siguiente canción en la cola"""
        state = self.guild_states[guild_id]
        
        # Obtener siguiente canción
        next_song = state['queue'].next()
        
        if not next_song:
            # Cola vacía
            state['current_song'] = None
            if state['last_channel']:
                await state['last_channel'].send('✅ Cola de reproducción finalizada.')
            return
        
        state['current_song'] = next_song
        
        try:
            # Obtener URL de stream
            stream_url = await self.youtube_handler.get_stream_url(next_song.url)
            
            # Crear source de audio
            audio_source = discord.FFmpegPCMAudio(
                stream_url,
                before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
            )
            
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
                embed = create_now_playing_embed(next_song)
                await state['last_channel'].send(embed=embed)
        
        except Exception as e:
            logger.error(f'Error reproduciendo canción: {e}')
            if state['last_channel']:
                await state['last_channel'].send(f'❌ Error reproduciendo: {next_song.title}')
            # Intentar con la siguiente
            await self._play_next(guild_id)
    
    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pausar reproducción actual"""
        state = self.get_guild_state(ctx.guild.id)
        
        if not state['voice_client'] or not state['voice_client'].is_playing():
            await ctx.send('❌ No hay nada reproduciéndose.')
            return
        
        state['voice_client'].pause()
        await ctx.send('⏸️ Reproducción pausada.')
    
    @commands.command(name='resume', aliases=['unpause'])
    async def resume(self, ctx):
        """Reanudar reproducción"""
        state = self.get_guild_state(ctx.guild.id)
        
        if not state['voice_client'] or not state['voice_client'].is_paused():
            await ctx.send('❌ No hay nada pausado.')
            return
        
        state['voice_client'].resume()
        await ctx.send('▶️ Reproducción reanudada.')
    
    @commands.command(name='skip', aliases=['s', 'next'])
    async def skip(self, ctx):
        """Saltar canción actual"""
        state = self.get_guild_state(ctx.guild.id)
        
        if not state['voice_client'] or not state['voice_client'].is_playing():
            await ctx.send('❌ No hay nada reproduciéndose.')
            return
        
        state['voice_client'].stop()  # Trigger next song
        await ctx.send('⏭️ Canción saltada.')
    
    @commands.command(name='stop')
    async def stop(self, ctx):
        """Detener reproducción y limpiar cola"""
        state = self.get_guild_state(ctx.guild.id)
        
        if not state['voice_client']:
            await ctx.send('❌ No estoy en un canal de voz.')
            return
        
        state['queue'].clear()
        state['current_song'] = None
        state['voice_client'].stop()
        
        await ctx.send('⏹️ Reproducción detenida y cola limpiada.')
    
    @commands.command(name='volume', aliases=['vol', 'v'])
    async def volume(self, ctx, volume: int):
        """
        Ajustar volumen (0-100)
        
        Uso: !volume 50
        """
        if not 0 <= volume <= 100:
            await ctx.send('❌ El volumen debe estar entre 0 y 100.')
            return
        
        state = self.get_guild_state(ctx.guild.id)
        state['volume'] = volume / 100
        
        if state['voice_client'] and state['voice_client'].source:
            state['voice_client'].source.volume = state['volume']
        
        await ctx.send(f'🔊 Volumen ajustado a {volume}%')
    
    @commands.command(name='nowplaying', aliases=['np', 'current'])
    async def nowplaying(self, ctx):
        """Mostrar canción actual"""
        state = self.get_guild_state(ctx.guild.id)
        
        if not state['current_song']:
            await ctx.send('❌ No hay nada reproduciéndose.')
            return
        
        embed = create_now_playing_embed(state['current_song'])
        await ctx.send(embed=embed)
    
    @commands.command(name='queue', aliases=['q'])
    async def queue_command(self, ctx):
        """Mostrar cola de reproducción"""
        state = self.get_guild_state(ctx.guild.id)
        queue_list = state['queue'].get_queue()
        
        if not queue_list and not state['current_song']:
            await ctx.send('❌ La cola está vacía.')
            return
        
        embed = create_queue_embed(queue_list, state['current_song'])
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
```

### 3.3 Utilidades

#### Song Model (`src/utils/song.py`)

```python
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
    
    @classmethod
    def from_youtube_info(cls, info: dict, requester: discord.Member):
        """Crear Song desde info de yt-dlp"""
        return cls(
            title=info.get('title', 'Sin título'),
            url=info.get('webpage_url') or info.get('url'),
            duration=info.get('duration', 0),
            thumbnail=info.get('thumbnail', ''),
            requester=requester,
            source='youtube'
        )
    
    def format_duration(self) -> str:
        """Formatear duración como MM:SS"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"
    
    def to_embed_field(self, position: Optional[int] = None) -> tuple:
        """Convertir a field de embed"""
        name = f"**{position}.** {self.title[:50]}" if position else self.title[:50]
        value = f"Duración: `{self.format_duration()}` | Por: {self.requester.mention}"
        return (name, value, False)
```

#### Queue Manager (`src/utils/queue_manager.py`)

```python
from collections import deque
import random
from typing import List, Optional
from .song import Song

class QueueManager:
    """Gestor de cola de reproducción"""
    
    def __init__(self, max_size: int = 100):
        self.queue = deque()
        self.history = deque(maxlen=10)
        self.max_size = max_size
        self.loop_mode = 'off'  # 'off', 'song', 'queue'
        self.current_index = -1
    
    def add(self, song: Song) -> bool:
        """Añadir canción a la cola"""
        if len(self.queue) >= self.max_size:
            return False
        self.queue.append(song)
        return True
    
    def next(self) -> Optional[Song]:
        """Obtener siguiente canción"""
        # Modo loop song
        if self.loop_mode == 'song' and self.history:
            return self.history[-1]
        
        # Cola vacía
        if not self.queue:
            # Modo loop queue
            if self.loop_mode == 'queue' and self.history:
                # Recargar desde history
                self.queue = deque(self.history)
                self.history.clear()
        
        if not self.queue:
            return None
        
        song = self.queue.popleft()
        self.history.append(song)
        return song
    
    def remove(self, index: int) -> bool:
        """Eliminar canción por índice"""
        if 0 <= index < len(self.queue):
            del self.queue[index]
            return True
        return False
    
    def clear(self):
        """Limpiar cola"""
        self.queue.clear()
    
    def shuffle(self):
        """Mezclar cola"""
        temp = list(self.queue)
        random.shuffle(temp)
        self.queue = deque(temp)
    
    def get_queue(self) -> List[Song]:
        """Obtener lista de canciones"""
        return list(self.queue)
    
    def set_loop_mode(self, mode: str):
        """Establecer modo de loop"""
        if mode in ['off', 'song', 'queue']:
            self.loop_mode = mode
    
    def __len__(self):
        return len(self.queue)
```

---

## 4. Testing

### 4.1 Estructura de Tests

```python
# tests/test_queue_manager.py
import pytest
from src.utils.queue_manager import QueueManager
from src.utils.song import Song
from unittest.mock import Mock

@pytest.fixture
def queue():
    return QueueManager(max_size=10)

@pytest.fixture
def mock_song():
    return Song(
        title="Test Song",
        url="https://test.com",
        duration=180,
        thumbnail="",
        requester=Mock(),
        source="youtube"
    )

def test_add_song(queue, mock_song):
    assert queue.add(mock_song) == True
    assert len(queue) == 1

def test_max_size(queue, mock_song):
    for _ in range(10):
        queue.add(mock_song)
    assert queue.add(mock_song) == False  # Excede máximo

def test_next_song(queue, mock_song):
    queue.add(mock_song)
    next_song = queue.next()
    assert next_song == mock_song
    assert len(queue) == 0

def test_shuffle(queue):
    songs = [Song(f"Song {i}", f"url{i}", 180, "", Mock(), "youtube") for i in range(10)]
    for song in songs:
        queue.add(song)
    
    original_order = list(queue.queue)
    queue.shuffle()
    shuffled_order = list(queue.queue)
    
    assert set(original_order) == set(shuffled_order)
    # Probabilidad de que sean diferentes
    assert original_order != shuffled_order
```

### 4.2 Ejecutar Tests

```bash
# Instalar pytest
pip install pytest pytest-asyncio

# Ejecutar todos los tests
pytest

# Con cobertura
pip install pytest-cov
pytest --cov=src tests/
```

---

## 5. Buenas Prácticas

### 5.1 Código

- ✅ Usar async/await para operaciones I/O
- ✅ Manejar excepciones apropiadamente
- ✅ Documentar funciones con docstrings
- ✅ Usar type hints
- ✅ Mantener funciones pequeñas y enfocadas
- ✅ Evitar variables globales

### 5.2 Git Workflow

```bash
# Crear rama para feature
git checkout -b feature/nueva-funcionalidad

# Hacer commits descriptivos
git commit -m "feat: añadir comando de loop"
git commit -m "fix: corregir búsqueda en YouTube"

# Push a remote
git push origin feature/nueva-funcionalidad
```

### 5.3 Logging

```python
import logging

logger = logging.getLogger(__name__)

# Niveles apropiados
logger.debug('Información de debugging')
logger.info('Información general')
logger.warning('Advertencia')
logger.error('Error recuperable')
logger.critical('Error crítico')
```

---

## 6. Debugging

### 6.1 Logging Detallado

```python
# En bot.py, cambiar nivel a DEBUG
logging.basicConfig(level=logging.DEBUG)
```

### 6.2 Comandos de Debug

```python
@commands.command(name='debug', hidden=True)
@commands.is_owner()
async def debug(self, ctx):
    """Información de debugging (solo owner)"""
    state = self.get_guild_state(ctx.guild.id)
    
    info = f"""
    **Debug Info:**
    Voice Connected: {state['voice_client'].is_connected() if state['voice_client'] else False}
    Is Playing: {state['voice_client'].is_playing() if state['voice_client'] else False}
    Queue Size: {len(state['queue'])}
    Current Song: {state['current_song'].title if state['current_song'] else 'None'}
    Loop Mode: {state['loop_mode']}
    Volume: {int(state['volume'] * 100)}%
    """
    
    await ctx.send(info)
```

### 6.3 Usar Python Debugger

```python
# Añadir breakpoint
import pdb; pdb.set_trace()

# O usar breakpoint() en Python 3.7+
breakpoint()
```

---

**Siguiente:** Leer [DESPLIEGUE.md](DESPLIEGUE.md) para publicar el bot
