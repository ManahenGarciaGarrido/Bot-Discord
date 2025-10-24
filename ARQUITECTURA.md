# 🏗️ ARQUITECTURA.md - Diseño del Sistema

## 1. Visión General de la Arquitectura

### 1.1 Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                        Discord Servers                       │
│                    (Múltiples servidores)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Discord Gateway (WebSocket)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                                                               │
│                    Discord Music Bot                         │
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Bot Core  │  │  Cogs Layer  │  │ Utils Layer  │       │
│  │  (discord.py│◄─┤   (Commands) │◄─┤  (Handlers)  │       │
│  │   Client)   │  │              │  │              │       │
│  └──────┬──────┘  └──────────────┘  └──────────────┘       │
│         │                                                    │
│         │         ┌──────────────────────────────┐         │
│         └────────►│  Queue Manager (per guild)   │         │
│                   │  - FIFO queue                │         │
│                   │  - Loop/Shuffle logic        │         │
│                   └──────────────────────────────┘         │
│                                                               │
└───────────┬──────────────────────────┬──────────────────────┘
            │                          │
            │                          │
    ┌───────▼────────┐        ┌───────▼────────┐
    │  YouTube API   │        │  Spotify API   │
    │   (yt-dlp)     │        │   (spotipy)    │
    └───────┬────────┘        └───────┬────────┘
            │                          │
            │ Audio Stream             │ Metadata
            │                          │
    ┌───────▼──────────────────────────▼────────┐
    │           FFmpeg Audio Pipeline            │
    │    (Decode, Process, Encode, Stream)       │
    └────────────────────────────────────────────┘
```

### 1.2 Patrón de Diseño

El bot utiliza una **arquitectura modular basada en Cogs** (extensiones de discord.py):

- **Separation of Concerns:** Cada Cog maneja un dominio específico
- **Event-Driven:** Reacciona a eventos de Discord (mensajes, reacciones, voice state)
- **Asynchronous:** Usa async/await para operaciones no bloqueantes
- **Stateful per Guild:** Cada servidor mantiene su propio estado

## 2. Componentes Principales

### 2.1 Bot Core (`src/bot.py`)

**Responsabilidad:** Inicialización y gestión del bot principal.

```python
class MusicBot(commands.Bot):
    - __init__(): Inicializar cliente Discord
    - setup_hook(): Cargar Cogs y configuración
    - on_ready(): Evento de conexión exitosa
    - on_error(): Manejo global de errores
```

**Características:**
- Carga dinámica de Cogs
- Configuración de intents (voice, messages, message_content)
- Sistema de logging
- Manejo de reconexión automática

### 2.2 Music Cog (`src/cogs/music.py`)

**Responsabilidad:** Comandos principales de reproducción de música.

**Comandos implementados:**
```python
@commands.command()
async def join(ctx)        # Unirse a canal de voz
async def leave(ctx)       # Salir de canal de voz
async def play(ctx, *, query)  # Reproducir música
async def pause(ctx)       # Pausar reproducción
async def resume(ctx)      # Reanudar reproducción
async def stop(ctx)        # Detener y limpiar
async def skip(ctx)        # Saltar canción
async def volume(ctx, vol) # Ajustar volumen
async def nowplaying(ctx)  # Info de canción actual
async def queue(ctx)       # Mostrar cola
async def loop(ctx, mode)  # Modo de repetición
async def shuffle(ctx)     # Mezclar cola
async def seek(ctx, time)  # Saltar a timestamp
```

**Estado por Guild:**
```python
guild_states = {
    guild_id: {
        'voice_client': VoiceClient,
        'queue': QueueManager,
        'current_song': Song,
        'volume': float,
        'loop_mode': str,
    }
}
```

### 2.3 Playlist Cog (`src/cogs/playlist.py`)

**Responsabilidad:** Gestión de favoritos y playlists personalizadas.

**Comandos implementados:**
```python
@commands.command()
async def favorite(ctx)           # Añadir a favoritos
async def favorites(ctx)          # Listar favoritos
async def playfavorite(ctx, num)  # Reproducir favorito
async def removefavorite(ctx, num)# Eliminar favorito
```

**Almacenamiento:**
- SQLite database: `favorites.db`
- Schema: `(user_id, song_title, song_url, added_date)`

### 2.4 Admin Cog (`src/cogs/admin.py`)

**Responsabilidad:** Comandos administrativos y estadísticas.

**Comandos implementados:**
```python
@commands.command()
@commands.has_permissions(administrator=True)
async def stats(ctx)      # Estadísticas del bot
async def prefix(ctx, new)# Cambiar prefijo
async def reset(ctx)      # Reset configuración
```

## 3. Capa de Utilidades

### 3.1 Music Player (`src/utils/music_player.py`)

**Responsabilidad:** Lógica de reproducción de audio.

```python
class MusicPlayer:
    def __init__(self, voice_client)
    async def play_song(self, song)
    def pause(self)
    def resume(self)
    def stop(self)
    def set_volume(self, volume)
    async def seek(self, timestamp)
    def is_playing(self) -> bool
    def is_paused(self) -> bool
```

**Características:**
- Gestión de FFmpegPCMAudio
- Control de volumen (0.0 - 1.0)
- Callbacks de finalización
- Manejo de errores de stream

### 3.2 Queue Manager (`src/utils/queue_manager.py`)

**Responsabilidad:** Gestión de cola de reproducción.

```python
class QueueManager:
    def __init__(self)
    def add(self, song)
    def next(self) -> Song | None
    def remove(self, index)
    def clear(self)
    def shuffle(self)
    def get_queue(self) -> List[Song]
    def get_position(self) -> int
    def jump_to(self, index)
    def set_loop_mode(self, mode: str)  # 'off', 'song', 'queue'
```

**Estructura de datos:**
```python
queue = deque([Song, Song, ...])  # FIFO
history = deque([Song, Song, ...], maxlen=10)  # Últimas 10
loop_mode = 'off'  # 'off', 'song', 'queue'
```

### 3.3 YouTube Handler (`src/utils/youtube_handler.py`)

**Responsabilidad:** Interacción con YouTube via yt-dlp.

```python
class YouTubeHandler:
    def __init__(self)
    async def extract_info(self, url: str) -> Dict
    async def search(self, query: str, limit: int = 5) -> List[Dict]
    async def get_playlist(self, url: str) -> List[Dict]
    def get_stream_url(self, info: Dict) -> str
```

**Configuración yt-dlp:**
```python
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
    }],
    'noplaylist': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',  # IPv4
}
```

### 3.4 Spotify Handler (`src/utils/spotify_handler.py`)

**Responsabilidad:** Conversión de Spotify a YouTube.

```python
class SpotifyHandler:
    def __init__(self, client_id, client_secret)
    async def get_track_info(self, url: str) -> Dict
    async def get_playlist_tracks(self, url: str) -> List[Dict]
    async def get_album_tracks(self, url: str) -> List[Dict]
    def to_youtube_query(self, track_info: Dict) -> str
```

**Proceso de conversión:**
1. Extraer metadata de Spotify (artista, título)
2. Construir query: `"artista - título official audio"`
3. Buscar en YouTube usando YouTubeHandler
4. Seleccionar primer resultado

### 3.5 Song Model (`src/utils/song.py`)

**Responsabilidad:** Modelo de datos para canciones.

```python
@dataclass
class Song:
    title: str
    url: str
    duration: int  # en segundos
    thumbnail: str
    requester: discord.Member
    source: str  # 'youtube' o 'spotify'
    
    def format_duration(self) -> str
    def to_embed(self) -> discord.Embed
```

## 4. Flujo de Datos

### 4.1 Flujo de Comando `!play`

```
User: !play <query/url>
   │
   ▼
[Music Cog] parse_query()
   │
   ├─► YouTube URL detected
   │   └─► YouTubeHandler.extract_info()
   │       └─► Get stream URL
   │
   ├─► Spotify URL detected
   │   └─► SpotifyHandler.get_track_info()
   │       └─► Convert to YouTube query
   │           └─► YouTubeHandler.search()
   │
   └─► Search query detected
       └─► YouTubeHandler.search()
           └─► Show results with reactions
               └─► Wait for user selection
   │
   ▼
[Create Song object]
   │
   ▼
[QueueManager] add_to_queue()
   │
   ▼
If nothing playing:
   └─► [MusicPlayer] play_song()
       └─► FFmpegPCMAudio stream
           └─► Discord Voice Gateway
               └─► Audio to voice channel
   │
   ▼
On song finish:
   └─► [QueueManager] next()
       └─► Loop back to play next song
```

### 4.2 Gestión de Estado por Servidor

Cada servidor de Discord mantiene su propio estado:

```python
guild_state = {
    'voice_client': VoiceClient or None,
    'player': MusicPlayer or None,
    'queue': QueueManager,
    'current_song': Song or None,
    'volume': 0.5,  # 50%
    'loop_mode': 'off',
    'last_channel': TextChannel,
}
```

## 5. Manejo de Errores

### 5.1 Jerarquía de Excepciones

```python
class MusicBotException(Exception):
    """Base exception"""
    pass

class NotInVoiceChannel(MusicBotException):
    """User not in voice channel"""
    pass

class BotAlreadyInVoice(MusicBotException):
    """Bot already in different channel"""
    pass

class QueueEmpty(MusicBotException):
    """No songs in queue"""
    pass

class InvalidURL(MusicBotException):
    """Invalid YouTube/Spotify URL"""
    pass

class ExtractionError(MusicBotException):
    """Failed to extract audio info"""
    pass

class PlaybackError(MusicBotException):
    """Error during playback"""
    pass
```

### 5.2 Estrategia de Recuperación

```python
try:
    await play_song()
except ExtractionError:
    # Skip song, try next in queue
    await skip_current()
except PlaybackError:
    # Reconnect voice client
    await reconnect_voice()
    await retry_playback()
except Exception as e:
    # Log error, notify user
    logger.error(f"Unexpected error: {e}")
    await ctx.send(f"❌ Error inesperado: {e}")
```

## 6. Optimizaciones

### 6.1 Performance

**Streaming en lugar de descarga:**
```python
# ❌ MAL - Descarga completa
await download_file(url)
await play_file('song.mp3')

# ✅ BIEN - Stream directo
stream_url = get_stream_url(url)
audio_source = FFmpegPCMAudio(stream_url)
voice_client.play(audio_source)
```

**Caché de búsquedas:**
```python
search_cache = TTLCache(maxsize=100, ttl=3600)  # 1 hora

async def search(query):
    if query in search_cache:
        return search_cache[query]
    results = await youtube_search(query)
    search_cache[query] = results
    return results
```

### 6.2 Concurrencia

**Uso de asyncio para operaciones I/O:**
```python
async def process_playlist(urls):
    tasks = [extract_info(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
```

### 6.3 Gestión de Memoria

**Límites de cola:**
```python
MAX_QUEUE_SIZE = 100

def add_to_queue(song):
    if len(queue) >= MAX_QUEUE_SIZE:
        raise QueueFullError()
    queue.append(song)
```

**Limpieza de estados inactivos:**
```python
@tasks.loop(minutes=30)
async def cleanup_inactive():
    for guild_id, state in guild_states.items():
        if not state['voice_client'] or not state['voice_client'].is_connected():
            del guild_states[guild_id]
```

## 7. Seguridad

### 7.1 Validación de Entrada

```python
def validate_youtube_url(url):
    pattern = r'(youtube\.com|youtu\.be)'
    return re.search(pattern, url) is not None

def sanitize_query(query):
    # Remover caracteres especiales peligrosos
    return re.sub(r'[^\w\s-]', '', query)
```

### 7.2 Rate Limiting

```python
from discord.ext import commands

@commands.cooldown(1, 5, commands.BucketType.user)
async def play(ctx, *, query):
    # Máximo 1 comando cada 5 segundos por usuario
    ...
```

### 7.3 Permisos

```python
@commands.has_permissions(manage_guild=True)
async def admin_command(ctx):
    # Solo administradores
    ...

# Verificar permisos del bot
def check_bot_permissions(guild):
    bot_member = guild.me
    required = ['connect', 'speak', 'use_voice_activation']
    return all(getattr(bot_member.guild_permissions, perm) for perm in required)
```

## 8. Logging y Monitoreo

### 8.1 Estructura de Logs

```python
import logging

# Configuración
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('MusicBot')

# Uso
logger.info(f"Playing {song.title} in {guild.name}")
logger.warning(f"Queue full in {guild.name}")
logger.error(f"Failed to extract: {url}", exc_info=True)
```

### 8.2 Métricas

```python
class BotMetrics:
    songs_played = 0
    total_playtime = 0
    commands_executed = 0
    errors_count = 0
    
    @staticmethod
    def record_play(duration):
        BotMetrics.songs_played += 1
        BotMetrics.total_playtime += duration
    
    @staticmethod
    def record_error():
        BotMetrics.errors_count += 1
```

## 9. Testing

### 9.1 Estructura de Tests

```python
tests/
├── test_youtube_handler.py
├── test_spotify_handler.py
├── test_queue_manager.py
├── test_music_player.py
└── test_commands.py
```

### 9.2 Ejemplo de Test

```python
import pytest
from src.utils.queue_manager import QueueManager

@pytest.fixture
def queue_manager():
    return QueueManager()

def test_add_to_queue(queue_manager):
    song = create_test_song()
    queue_manager.add(song)
    assert len(queue_manager.get_queue()) == 1

def test_shuffle(queue_manager):
    songs = [create_test_song() for _ in range(10)]
    for song in songs:
        queue_manager.add(song)
    original_order = queue_manager.get_queue()
    queue_manager.shuffle()
    shuffled_order = queue_manager.get_queue()
    assert original_order != shuffled_order
```

## 10. Deployment Architecture

### 10.1 Entorno de Producción

```
┌─────────────────────────────────────┐
│   Hosting Platform (Railway/Render) │
│                                      │
│   ┌──────────────────────────────┐  │
│   │    Docker Container          │  │
│   │  ┌────────────────────────┐  │  │
│   │  │  Python 3.11           │  │  │
│   │  │  + discord.py          │  │  │
│   │  │  + yt-dlp              │  │  │
│   │  │  + FFmpeg              │  │  │
│   │  └────────────────────────┘  │  │
│   │                              │  │
│   │  ┌────────────────────────┐  │  │
│   │  │  Bot Process           │  │  │
│   │  │  (Always Running)      │  │  │
│   │  └────────────────────────┘  │  │
│   └──────────────────────────────┘  │
│                                      │
│   Environment Variables:             │
│   - DISCORD_TOKEN                    │
│   - SPOTIFY_CLIENT_ID                │
│   - SPOTIFY_CLIENT_SECRET            │
└─────────────────────────────────────┘
```

### 10.2 Dockerfile

```dockerfile
FROM python:3.11-slim

# Instalar FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "-m", "src.bot"]
```

## 11. Escalabilidad Futura

### 11.1 Sharding (Para >2500 servidores)

```python
bot = commands.AutoShardedBot(
    command_prefix='!',
    intents=intents,
    shard_count=4  # Automático si None
)
```

### 11.2 Base de Datos Distribuida

Para escalar más allá de SQLite:
- PostgreSQL para favoritos y estadísticas
- Redis para caché de búsquedas y sesiones

### 11.3 Load Balancing

Para múltiples instancias:
- Particionamiento por guild_id
- Queue distribuida (RabbitMQ/Redis)
- Shared state via Redis

---

**Esta arquitectura está diseñada para:**
- ✅ Fácil mantenimiento y extensión
- ✅ Performance óptimo con recursos limitados
- ✅ Deployment gratuito
- ✅ Escalabilidad horizontal futura
