# 🚀 INICIO-RAPIDO.md - Comienza en 15 Minutos

## Objetivo
Tener tu bot de música de Discord funcionando localmente en menos de 15 minutos.

---

## Paso 1: Requisitos (2 min)

### Descargar e Instalar:
1. **Python 3.10+**: https://python.org/downloads
2. **Git**: https://git-scm.com
3. **FFmpeg**: https://ffmpeg.org/download.html

### Verificar instalación:
```bash
python --version    # Debe ser 3.10+
git --version
ffmpeg -version
```

---

## Paso 2: Crear Bot en Discord (3 min)

### A. Discord Developer Portal
1. Ir a https://discord.com/developers/applications
2. Click "New Application" → Nombrar "Mi Music Bot"
3. Ir a "Bot" → "Add Bot" → "Reset Token" → **COPIAR TOKEN**
4. Activar intents:
   - ✅ Message Content Intent
5. Ir a "OAuth2" → "URL Generator"
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Connect`, `Speak`, etc.
6. Copiar URL e invitar bot a tu servidor

### B. Spotify Developer
1. Ir a https://developer.spotify.com/dashboard
2. "Create an App" → Nombrar "Music Bot"
3. **COPIAR** Client ID y Client Secret

---

## Paso 3: Setup del Proyecto (5 min)

### Crear estructura:
```bash
# Crear directorio
mkdir discord-music-bot
cd discord-music-bot

# Crear carpetas
mkdir -p src/cogs src/utils src/config

# Crear archivos vacíos
touch src/__init__.py src/bot.py
touch src/cogs/__init__.py src/cogs/music.py
touch src/utils/__init__.py
touch .env requirements.txt
```

### Crear entorno virtual:
```bash
python -m venv venv

# Activar
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Crear requirements.txt:
```txt
discord.py[voice]>=2.3.0
PyNaCl>=1.5.0
yt-dlp>=2023.10.13
spotipy>=2.23.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
```

### Instalar:
```bash
pip install -r requirements.txt
```

---

## Paso 4: Configuración (2 min)

### Crear archivo .env:
```env
DISCORD_TOKEN=tu_token_de_discord_aquí
SPOTIFY_CLIENT_ID=tu_client_id_aquí
SPOTIFY_CLIENT_SECRET=tu_client_secret_aquí
PREFIX=!
```

**⚠️ IMPORTANTE:** Reemplazar con tus valores reales.

---

## Paso 5: Código Básico (3 min)

### Crear src/bot.py:
```python
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix=os.getenv('PREFIX', '!'),
    intents=intents
)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado: {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))
```

---

## Paso 6: Primera Ejecución (1 min)

```bash
python src/bot.py
```

Deberías ver:
```
✅ Bot conectado: TuBot#1234
```

### Probar en Discord:
```
!ping
```

---

## ✅ ¡Listo! Bot Funcionando

Ahora puedes:
1. Leer **DESARROLLO.md** para añadir funcionalidades de música
2. Seguir **INSTALACION.md** para setup completo
3. Leer **DESPLIEGUE.md** cuando quieras publicarlo 24/7

---

## Próximos Pasos

### Para Reproducir Música:
Implementar los archivos completos según **DESARROLLO.md**:
- `src/cogs/music.py` - Comandos de música
- `src/utils/youtube_handler.py` - Manejo de YouTube
- `src/utils/spotify_handler.py` - Manejo de Spotify
- `src/utils/queue_manager.py` - Gestión de cola

### Templates Disponibles:
Todos los templates y código completo están en:
- **ARQUITECTURA.md** - Diseño del sistema
- **DESARROLLO.md** - Código completo comentado

---

## Troubleshooting Rápido

### "DISCORD_TOKEN is empty"
→ Revisar archivo .env

### "discord.py not found"
→ `pip install discord.py[voice]`

### "FFmpeg not found"
→ Reinstalar FFmpeg y añadir al PATH

### Bot no responde
→ Verificar Message Content Intent activado

---

## Comandos Útiles

```bash
# Instalar dependencia
pip install nombre

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Limpiar caché
find . -name __pycache__ -exec rm -rf {} +

# Ver logs en tiempo real
python src/bot.py
```

---

## Estructura Final del Proyecto

```
discord-music-bot/
├── .env                    # Configuración (NO subir a Git)
├── requirements.txt        # Dependencias
├── README.md              # Documentación principal
├── ARQUITECTURA.md        # Diseño del sistema
├── DESARROLLO.md          # Guía de desarrollo
├── DESPLIEGUE.md          # Guía de deployment
├── COMANDOS.md            # Lista de comandos
├── INICIO-RAPIDO.md       # Esta guía
│
└── src/
    ├── bot.py             # Punto de entrada
    │
    ├── cogs/
    │   ├── music.py       # Comandos de música
    │   ├── playlist.py    # Gestión de favoritos
    │   └── admin.py       # Comandos admin
    │
    └── utils/
        ├── music_player.py      # Reproductor
        ├── queue_manager.py     # Cola
        ├── youtube_handler.py   # YouTube
        ├── spotify_handler.py   # Spotify
        └── song.py             # Modelo de datos
```

---

## Recursos de Ayuda

- 📖 [Documentación Discord.py](https://discordpy.readthedocs.io/)
- 🎵 [yt-dlp Docs](https://github.com/yt-dlp/yt-dlp)
- 💬 [Discord Developers](https://discord.gg/discord-developers)

---

**Tiempo estimado total: 15 minutos ⏱️**
**Costo: $0.00 💰**

¡Disfruta desarrollando tu bot de música! 🎉
