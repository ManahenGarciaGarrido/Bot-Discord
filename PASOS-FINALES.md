# 🚀 PASOS FINALES PARA USAR TU BOT

## ✅ TODO ESTÁ IMPLEMENTADO

El bot está **100% completo** con TODAS las funcionalidades descritas en la documentación + las nuevas funcionalidades inteligentes de IA.

---

## 📦 ¿Qué incluye el bot?

### **Funcionalidades Core (40+ comandos):**
✅ Reproducción desde YouTube y Spotify
✅ Sistema de cola avanzado (loop, shuffle, jump, move)
✅ Control completo (pause, resume, skip, stop, volume)
✅ Sistema de favoritos con SQLite
✅ Comandos administrativos y estadísticas

### **Funcionalidades IA (NUEVAS):**
✅ **Radio Inteligente** - Reproducción continua personalizada
✅ **Sistema Like/Dislike** - El bot aprende tus gustos
✅ **Motor de Recomendaciones** - Sugerencias basadas en IA
✅ **Auto-Shuffle para Playlists** - Nunca el mismo orden
✅ **Búsqueda Inteligente** - `!findplaylist rock`, `!play hits 2010`
✅ **Preferencias Musicales** - Ve qué aprendió el bot de ti

---

## 🎯 OPCIÓN 1: Ejecutar Localmente (10 minutos)

### 1. Instalar Requisitos

**Windows:**
1. Descargar Python 3.10+ de https://python.org/downloads
2. Descargar FFmpeg de https://ffmpeg.org/download.html
3. Añadir FFmpeg al PATH del sistema

**Linux:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv ffmpeg git
```

**Mac:**
```bash
brew install python ffmpeg git
```

### 2. Obtener Credenciales (5 minutos)

#### **Discord:**
1. Ir a https://discord.com/developers/applications
2. "New Application" → Nombre: "Mi Music Bot"
3. Ir a "Bot" → "Reset Token" → **COPIAR TOKEN**
4. Activar "Message Content Intent" ✅
5. OAuth2 → URL Generator → Scopes: `bot` → Permisos: `Send Messages`, `Connect`, `Speak`
6. Invitar bot a tu servidor con la URL generada

#### **Spotify (Opcional pero recomendado):**
1. Ir a https://developer.spotify.com/dashboard
2. "Create an App" → Nombre: "Music Bot"
3. **COPIAR** Client ID y Client Secret

### 3. Configurar el Bot

```bash
# Clonar repositorio
git clone https://github.com/ManahenGarciaGarrido/Bot-Discord.git
cd Bot-Discord

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env
```

Editar `.env` y añadir tus credenciales:
```env
DISCORD_TOKEN=tu_token_de_discord_aqui
SPOTIFY_CLIENT_ID=tu_client_id_aqui
SPOTIFY_CLIENT_SECRET=tu_client_secret_aqui
PREFIX=!
DEFAULT_VOLUME=50
```

### 4. Ejecutar el Bot

```bash
python -m src.bot
```

Deberías ver:
```
🚀 Iniciando Discord Music Bot...
✅ Bot conectado como TuBot#1234
📊 Servidores: 1
✨ Bot listo para recibir comandos
```

### 5. Probar en Discord

```
!help           # Ver todos los comandos
!ping           # Verificar latencia
!join           # Unirse a tu canal de voz
!play despacito # Probar reproducción
!radio          # Probar radio inteligente
!like           # Dale like para entrenar al bot
```

---

## ☁️ OPCIÓN 2: Desplegar en Railway (100% GRATIS, 10 minutos)

### 1. Preparar GitHub

El repositorio ya está en GitHub: `ManahenGarciaGarrido/Bot-Discord`

### 2. Deploy en Railway

1. Ir a https://railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Conectar tu cuenta de GitHub
4. Seleccionar `Bot-Discord`
5. Railway detectará automáticamente la configuración

### 3. Configurar Variables de Entorno

En Railway, ir a "Variables" y añadir:
```
DISCORD_TOKEN=tu_token_de_discord
SPOTIFY_CLIENT_ID=tu_spotify_client_id
SPOTIFY_CLIENT_SECRET=tu_spotify_client_secret
PREFIX=!
DEFAULT_VOLUME=50
```

### 4. Deploy Automático

Railway desplegará automáticamente. En 2-3 minutos:
✅ Bot online
✅ Funcionando 24/7
✅ Logs visibles en Railway

### 5. Mantener Activo 24/7

1. Ir a https://uptimerobot.com
2. "Add New Monitor"
3. Type: HTTP(s)
4. URL: Tu URL de Railway + `/health`
5. Interval: 5 minutos
6. Crear monitor

¡Listo! Bot activo 24/7 gratis.

---

## ☁️ OPCIÓN 3: Desplegar en Render (100% GRATIS)

### 1. Preparar

El repositorio ya tiene `render.yaml` configurado.

### 2. Deploy

1. Ir a https://render.com
2. "New +" → "Web Service"
3. Conectar GitHub → Seleccionar `Bot-Discord`
4. Render detectará configuración automáticamente

### 3. Variables de Entorno

Añadir en Render:
```
DISCORD_TOKEN=tu_token
SPOTIFY_CLIENT_ID=tu_id
SPOTIFY_CLIENT_SECRET=tu_secret
PREFIX=!
```

### 4. Deploy

Hacer clic en "Create Web Service". En 3-5 minutos el bot estará online.

### 5. UptimeRobot

Igual que Railway - usar UptimeRobot para mantenerlo activo.

---

## 📚 Documentación Completa

Todo está documentado en los archivos .md:

- **NUEVAS-FUNCIONALIDADES.md** - Todas las funciones de IA explicadas
- **README.md** - Visión general del proyecto
- **COMANDOS.md** - Lista completa de comandos (40+)
- **INSTALACION.md** - Instalación paso a paso detallada
- **DESPLIEGUE.md** - Guías completas de deployment
- **ARQUITECTURA.md** - Diseño técnico del sistema
- **DESARROLLO.md** - Código completo comentado
- **INICIO-RAPIDO.md** - Guía de 15 minutos

---

## 🎵 Comandos Rápidos para Probar

### Básicos:
```
!help            # Ver ayuda
!play despacito  # Reproducir por búsqueda
!np              # Ver canción actual
!queue           # Ver cola
!skip            # Saltar canción
```

### Playlists:
```
!play https://open.spotify.com/playlist/xxxxx  # Spotify
!play https://youtube.com/playlist?list=xxxxx  # YouTube
!shuffle         # Mezclar cola
!loop queue      # Repetir cola
```

### Radio Inteligente (NUEVO):
```
!radio           # Radio personalizada
!radio rock      # Radio de rock
!like            # Me gusta esta canción
!dislike         # No me gusta
!recommend       # Ver recomendaciones
!mypreferences   # Ver tus gustos
```

### Búsqueda de Playlists (NUEVO):
```
!findplaylist rock
!findplaylist hits 2010
!findplaylist chill vibes
!findplaylist workout music
```

### Favoritos:
```
!favorite        # Añadir a favoritos
!favorites       # Ver favoritos
!playfav 1       # Reproducir favorito
```

---

## 🔥 Características Destacadas

### 1. **Radio que Aprende de Ti**
```
!radio                    # Primera vez: música variada
[Dale like a 5 canciones de pop]
[Dale dislike a 2 de reggaeton]
!radio                    # Segunda vez: solo pop, cero reggaeton
```

### 2. **Playlists Siempre Diferentes**
```
!play spotify_playlist    # Primera vez: orden A
!play spotify_playlist    # Segunda vez: orden B (auto-mezclada)
```

### 3. **Búsqueda Contextual**
```
!findplaylist rock        # Encuentra playlists de rock en YouTube
!findplaylist sad songs   # Encuentra música triste
!findplaylist gym         # Música para entrenar
```

### 4. **Sistema Inteligente**
```
Usuario: !radio
Bot: [Reproduce reggaeton]
Usuario: !dislike
Bot: [Auto-skip + recuerda que no te gusta reggaeton]
Bot: [Próximas veces evita reggaeton automáticamente]
```

---

## 📊 Bases de Datos

El bot crea automáticamente:
- `favorites.db` - Canciones favoritas
- `preferences.db` - Preferencias musicales y sistema de IA

Ambas son SQLite, no requieren configuración.

---

## ⚠️ Solución de Problemas Comunes

### Bot no responde a comandos:
1. Verificar que "Message Content Intent" está activado en Discord Developer Portal
2. Verificar el prefijo (por defecto `!`)
3. Revisar logs del bot

### No reproduce música:
1. Verificar que FFmpeg está instalado: `ffmpeg -version`
2. Verificar que el bot tiene permisos de "Connect" y "Speak"
3. Verificar que estás en un canal de voz

### Spotify no funciona:
1. Verificar Client ID y Client Secret en `.env`
2. El bot funcionará sin Spotify, solo con YouTube

### Bot se desconecta (deployment):
1. Verificar que UptimeRobot está configurado correctamente
2. Verificar que el health check endpoint funciona: `https://tu-url/health`

---

## 🎯 Próximos Pasos Recomendados

1. **Ejecutar localmente** primero para probar
2. **Dale like/dislike** a varias canciones para entrenar al bot
3. **Prueba !radio** para ver las recomendaciones personalizadas
4. **Despliega en Railway/Render** cuando esté todo probado
5. **Configura UptimeRobot** para mantenerlo activo 24/7

---

## 💡 Tips Pro

### Para entrenar rápido al bot:
```bash
!radio
# Dale like a 10-15 canciones que te gusten
# Dale dislike a 5-10 que no
!mypreferences  # Ver qué aprendió
!radio          # Ahora será mucho más personalizado
```

### Para fiestas:
```bash
!findplaylist party music 2023
!shuffle
!loop queue
!volume 80
```

### Para trabajar/estudiar:
```bash
!radio chill vibes
!loop queue
!volume 30
```

---

## 🎉 ¡YA ESTÁ TODO LISTO!

**Solo necesitas:**
1. Copiar tus tokens en `.env`
2. Ejecutar `python -m src.bot`
3. Usar `!help` en Discord

**El bot hará el resto:**
- Aprenderá de tus gustos
- Recomendará música similar
- Evitará lo que no te gusta
- Se convertirá en tu DJ personal

---

## 📞 Soporte

- **Documentación completa:** Todos los archivos .md
- **Logs del bot:** Archivo `bot.log`
- **GitHub Issues:** Para reportar bugs

---

**¡Disfruta de tu bot de música con IA! 🎵**

Ahora tienes el **bot de música más avanzado** con sistema de recomendaciones inteligente, radio personalizada, y aprendizaje automático de gustos musicales.

**Costo total: $0.00** ✨
