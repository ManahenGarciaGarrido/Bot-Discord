# 🚀 INSTALACION.md - Guía de Instalación Paso a Paso

## Tabla de Contenidos
1. [Requisitos Previos](#1-requisitos-previos)
2. [Configuración de Discord](#2-configuración-de-discord)
3. [Configuración de Spotify](#3-configuración-de-spotify)
4. [Instalación Local](#4-instalación-local)
5. [Configuración del Bot](#5-configuración-del-bot)
6. [Primera Ejecución](#6-primera-ejecución)
7. [Resolución de Problemas](#7-resolución-de-problemas)

---

## 1. Requisitos Previos

### 1.1 Software Necesario

#### Python 3.10 o superior

**Windows:**
1. Descargar desde [python.org](https://www.python.org/downloads/)
2. Durante instalación, marcar "Add Python to PATH"
3. Verificar instalación:
```bash
python --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3 --version
```

**macOS:**
```bash
brew install python@3.11
python3 --version
```

#### Git

**Windows:**
- Descargar desde [git-scm.com](https://git-scm.com/)

**Linux:**
```bash
sudo apt install git
```

**macOS:**
```bash
brew install git
```

#### FFmpeg

**Windows:**
1. Descargar desde [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extraer a `C:\ffmpeg`
3. Añadir `C:\ffmpeg\bin` al PATH del sistema
4. Verificar:
```bash
ffmpeg -version
```

**Linux:**
```bash
sudo apt install ffmpeg
ffmpeg -version
```

**macOS:**
```bash
brew install ffmpeg
ffmpeg -version
```

---

## 2. Configuración de Discord

### 2.1 Crear Aplicación en Discord Developer Portal

1. Ir a [Discord Developer Portal](https://discord.com/developers/applications)
2. Hacer clic en "New Application"
3. Darle un nombre (ej: "Mi Music Bot")
4. Hacer clic en "Create"

### 2.2 Crear Bot

1. En el menú lateral, hacer clic en "Bot"
2. Hacer clic en "Add Bot" → "Yes, do it!"
3. **Guardar el TOKEN** (lo necesitarás después)
   - Hacer clic en "Reset Token" → "Copy"
   - ⚠️ **NUNCA compartas este token**

### 2.3 Configurar Intents

En la misma página de Bot, activar los siguientes **Privileged Gateway Intents**:
- ✅ **Presence Intent** (opcional)
- ✅ **Server Members Intent** (opcional)
- ✅ **Message Content Intent** ⚠️ **OBLIGATORIO**

### 2.4 Crear Invitación del Bot

1. En el menú lateral, ir a "OAuth2" → "URL Generator"
2. En **SCOPES**, seleccionar:
   - ✅ `bot`
   - ✅ `applications.commands` (opcional, para slash commands futuros)
3. En **BOT PERMISSIONS**, seleccionar:
   - ✅ `Send Messages`
   - ✅ `Embed Links`
   - ✅ `Attach Files`
   - ✅ `Add Reactions`
   - ✅ `Use External Emojis`
   - ✅ `Read Message History`
   - ✅ `Connect` (voz)
   - ✅ `Speak` (voz)
   - ✅ `Use Voice Activity`
4. Copiar la **URL generada** al final de la página
5. Abrir la URL en el navegador e invitar el bot a tu servidor

---

## 3. Configuración de Spotify

### 3.1 Crear Aplicación en Spotify Developer Dashboard

1. Ir a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Hacer clic en "Create an App"
3. Rellenar:
   - **App name:** Mi Music Bot
   - **App description:** Bot de música para Discord
   - **Website:** (dejar en blanco)
   - **Redirect URI:** http://localhost (no se usa, pero requerido)
4. Aceptar términos y hacer clic en "Create"

### 3.2 Obtener Credenciales

1. En la página de tu app, encontrarás:
   - **Client ID** (visible)
   - **Client Secret** (hacer clic en "Show Client Secret")
2. **Guardar ambos** (los necesitarás después)

⚠️ **Nota:** La API de Spotify es gratuita con límite de 180 requests/minuto.

---

## 4. Instalación Local

### 4.1 Clonar el Repositorio

```bash
# Opción 1: Clonar desde GitHub (si ya existe)
git clone https://github.com/tu-usuario/discord-music-bot.git
cd discord-music-bot

# Opción 2: Crear estructura desde cero
mkdir discord-music-bot
cd discord-music-bot
```

### 4.2 Crear Estructura de Carpetas

Si estás creando desde cero:

```bash
# Linux/macOS
mkdir -p src/cogs src/utils src/config tests docs

# Windows (PowerShell)
New-Item -ItemType Directory -Path src\cogs, src\utils, src\config, tests, docs
```

### 4.3 Crear Entorno Virtual

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Tu terminal debería mostrar `(venv)` al inicio.

### 4.4 Instalar Dependencias

Crear archivo `requirements.txt`:

```txt
# Discord
discord.py[voice]>=2.3.0
PyNaCl>=1.5.0

# Audio Processing
yt-dlp>=2023.10.13

# Spotify
spotipy>=2.23.0

# Utilities
python-dotenv>=1.0.0
aiohttp>=3.9.0

# Database (opcional)
aiosqlite>=0.19.0

# Logging (opcional)
colorlog>=6.7.0
```

Instalar:

```bash
pip install -r requirements.txt
```

### 4.5 Verificar Instalación

```bash
python -c "import discord; import yt_dlp; import spotipy; print('✅ Todo instalado correctamente')"
```

---

## 5. Configuración del Bot

### 5.1 Crear Archivo de Entorno

Crear `.env` en la raíz del proyecto:

```bash
# Copiar ejemplo
cp .env.example .env

# O crear manualmente
touch .env
```

### 5.2 Rellenar Variables de Entorno

Editar `.env`:

```env
# Discord Bot
DISCORD_TOKEN=tu_token_de_discord_aqui

# Spotify API
SPOTIFY_CLIENT_ID=tu_spotify_client_id_aqui
SPOTIFY_CLIENT_SECRET=tu_spotify_client_secret_aqui

# Configuración del Bot
PREFIX=!
DEFAULT_VOLUME=50

# Opcionales
LOG_LEVEL=INFO
MAX_QUEUE_SIZE=100
```

⚠️ **IMPORTANTE:**
- Reemplazar `tu_token_de_discord_aqui` con tu token real
- Reemplazar las credenciales de Spotify con las reales
- NO subir este archivo a Git (debe estar en `.gitignore`)

### 5.3 Crear .gitignore

Crear `.gitignore`:

```gitignore
# Environment
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Bot specific
bot.log
*.db
*.sqlite3

# Downloads (por si acaso)
downloads/
*.mp3
*.m4a
*.webm
```

---

## 6. Primera Ejecución

### 6.1 Estructura Mínima de Archivos

Crear archivo básico `src/bot.py`:

```python
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Crear bot
bot = commands.Bot(
    command_prefix=os.getenv('PREFIX', '!'),
    intents=intents,
    help_command=None  # Desactivar help por defecto
)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    print(f'📊 Conectado a {len(bot.guilds)} servidores')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!help"
        )
    )

@bot.command(name='ping')
async def ping(ctx):
    """Comprobar latencia del bot"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latencia: {latency}ms')

if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print('❌ ERROR: DISCORD_TOKEN no encontrado en .env')
        exit(1)
    
    print('🚀 Iniciando bot...')
    bot.run(token)
```

### 6.2 Ejecutar el Bot

```bash
# Asegurarse de estar en el entorno virtual
python src/bot.py
```

Deberías ver:
```
🚀 Iniciando bot...
✅ Bot conectado como TuBot#1234
📊 Conectado a 1 servidores
```

### 6.3 Probar el Bot

En tu servidor de Discord:
```
!ping
```

El bot debería responder con:
```
🏓 Pong! Latencia: XXms
```

---

## 7. Resolución de Problemas

### 7.1 Error: "discord.py not found"

**Solución:**
```bash
pip install discord.py[voice]
```

### 7.2 Error: "Message content intent is not enabled"

**Causa:** No has activado el intent en Discord Developer Portal.

**Solución:**
1. Ir a Developer Portal → Tu App → Bot
2. Activar "Message Content Intent"
3. Guardar cambios
4. Reiniciar el bot

### 7.3 Error: "DISCORD_TOKEN is empty"

**Causa:** El archivo `.env` no está configurado correctamente.

**Solución:**
1. Verificar que `.env` existe en la raíz del proyecto
2. Verificar que contiene `DISCORD_TOKEN=...`
3. Asegurarse de que el token no tiene espacios antes/después

### 7.4 Error: "FFmpeg not found"

**Causa:** FFmpeg no está instalado o no está en el PATH.

**Solución Windows:**
1. Descargar FFmpeg
2. Extraer a `C:\ffmpeg`
3. Añadir `C:\ffmpeg\bin` al PATH del sistema
4. Reiniciar terminal
5. Verificar: `ffmpeg -version`

**Solución Linux:**
```bash
sudo apt install ffmpeg
```

### 7.5 Error: "Bot is not in a voice channel"

**Causa:** El bot no tiene permisos o tú no estás en un canal de voz.

**Solución:**
1. Unirte a un canal de voz
2. Verificar que el bot tiene permisos de "Connect" y "Speak"
3. Reintentar

### 7.6 Bot no responde a comandos

**Checklist:**
- ✅ El bot está online (luz verde en Discord)
- ✅ Estás usando el prefijo correcto (por defecto `!`)
- ✅ El bot tiene permiso de "Send Messages"
- ✅ El bot puede leer el canal (permisos de "Read Messages")

### 7.7 Error de importación de módulos

**Solución:**
```bash
# Reinstalar todas las dependencias
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

### 7.8 Error: "yt-dlp extraction failed"

**Causas posibles:**
1. Video privado o bloqueado geográficamente
2. Video eliminado
3. Problema temporal de YouTube

**Solución:**
```bash
# Actualizar yt-dlp a la última versión
pip install --upgrade yt-dlp
```

---

## 8. Siguientes Pasos

✅ **Bot instalado y funcionando**

Ahora puedes:
1. Leer [DESARROLLO.md](DESARROLLO.md) para añadir funcionalidades
2. Leer [DESPLIEGUE.md](DESPLIEGUE.md) para publicar el bot 24/7
3. Leer [COMANDOS.md](COMANDOS.md) para ver todos los comandos disponibles

---

## 9. Comandos Útiles

### Actualizar dependencias
```bash
pip install --upgrade -r requirements.txt
```

### Ver versión de Python
```bash
python --version
```

### Ver paquetes instalados
```bash
pip list
```

### Limpiar caché de Python
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
```

### Reiniciar bot (desarrollo)
```bash
# Linux/macOS
Ctrl+C
python src/bot.py

# Windows
Ctrl+C
python src/bot.py
```

---

## 10. Recursos Adicionales

- 📖 [Discord.py Documentation](https://discordpy.readthedocs.io/)
- 🎵 [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- 🎧 [Spotify API Docs](https://developer.spotify.com/documentation/web-api)
- 💬 [Discord Developers Discord](https://discord.gg/discord-developers)

---

**¡Felicidades! Tu bot de música está listo para desarrollo. 🎉**
