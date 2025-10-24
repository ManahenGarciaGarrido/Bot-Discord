# 🚀 DESPLIEGUE.md - Guía de Despliegue Gratuito

## Tabla de Contenidos
1. [Opciones de Hosting Gratuito](#1-opciones-de-hosting-gratuito)
2. [Railway.app (Recomendado)](#2-railwayapp-recomendado)
3. [Render.com](#3-rendercom)
4. [Replit](#4-replit)
5. [Oracle Cloud Free Tier](#5-oracle-cloud-free-tier)
6. [Mantener el Bot Activo 24/7](#6-mantener-el-bot-activo-247)
7. [Monitoreo y Logs](#7-monitoreo-y-logs)

---

## 1. Opciones de Hosting Gratuito

### Comparación de Plataformas

| Plataforma | RAM | CPU | Horas/mes | Sleep | Dificultad | Recomendado |
|------------|-----|-----|-----------|-------|------------|-------------|
| **Railway** | 512MB | 0.5 vCPU | 500 | Sí (5min) | ⭐⭐ Fácil | ✅ Sí |
| **Render** | 512MB | 0.5 vCPU | 750 | Sí (15min) | ⭐⭐ Fácil | ✅ Sí |
| **Replit** | 1GB | Shared | Ilimitado | Sí | ⭐ Muy fácil | ⚠️ Requiere workaround |
| **Oracle Cloud** | 1GB+ | 1+ vCPU | Ilimitado | No | ⭐⭐⭐⭐ Difícil | Solo avanzados |

### Recomendación por Uso

- **Uso casual (<500hrs/mes):** Railway
- **Uso intensivo (>500hrs/mes):** Render + UptimeRobot
- **Principiantes absolutos:** Replit
- **Usuarios avanzados:** Oracle Cloud

---

## 2. Railway.app (Recomendado)

### Ventajas
✅ Setup extremadamente fácil
✅ Integración directa con GitHub
✅ Variables de entorno sencillas
✅ Logs en tiempo real
✅ 500 horas gratis/mes

### Desventajas
❌ Sleep después de 5 minutos de inactividad (en plan gratuito)
❌ Solo 500 horas/mes

### 2.1 Preparación

#### Crear `Procfile`

En la raíz del proyecto:

```
web: python src/bot.py
```

#### Crear `railway.json`

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python src/bot.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### Actualizar `requirements.txt`

Asegurarse de que incluye:

```txt
discord.py[voice]>=2.3.0
PyNaCl>=1.5.0
yt-dlp>=2023.10.13
spotipy>=2.23.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
```

### 2.2 Deployment

#### Paso 1: Crear cuenta en Railway

1. Ir a [railway.app](https://railway.app)
2. Hacer clic en "Start a New Project"
3. Iniciar sesión con GitHub

#### Paso 2: Conectar Repositorio

1. Hacer clic en "Deploy from GitHub repo"
2. Seleccionar tu repositorio del bot
3. Railway detectará automáticamente Python

#### Paso 3: Configurar Variables de Entorno

1. Ir a la pestaña "Variables"
2. Añadir:
   ```
   DISCORD_TOKEN = tu_token_aqui
   SPOTIFY_CLIENT_ID = tu_client_id
   SPOTIFY_CLIENT_SECRET = tu_client_secret
   PREFIX = !
   ```

#### Paso 4: Deploy

1. Railway desplegará automáticamente
2. Ver logs en la pestaña "Deployments"
3. El bot debería estar online en 2-3 minutos

### 2.3 Configurar Dominio (Opcional)

1. Ir a "Settings"
2. En "Public Networking" → "Generate Domain"
3. Esto es útil para webhooks o monitoreo

### 2.4 Mantener Activo

Railway pone el bot en sleep después de 5 minutos sin requests HTTP. 

**Solución 1: Health Check Endpoint**

Añadir a `src/bot.py`:

```python
from aiohttp import web
import asyncio

async def health_check(request):
    return web.Response(text="Bot is alive!")

async def start_health_server():
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

# En main()
async def main():
    bot = MusicBot()
    
    # Iniciar servidor de health check
    asyncio.create_task(start_health_server())
    
    await bot.start(os.getenv('DISCORD_TOKEN'))
```

Luego usar UptimeRobot (ver sección 6).

---

## 3. Render.com

### Ventajas
✅ 750 horas gratis/mes (más que Railway)
✅ No requiere tarjeta de crédito
✅ Deploy automático desde GitHub
✅ SSL gratuito

### Desventajas
❌ Sleep después de 15 minutos (más tolerante que Railway)
❌ Solo 750 horas/mes

### 3.1 Preparación

#### Crear `render.yaml`

```yaml
services:
  - type: web
    name: discord-music-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/bot.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DISCORD_TOKEN
        sync: false
      - key: SPOTIFY_CLIENT_ID
        sync: false
      - key: SPOTIFY_CLIENT_SECRET
        sync: false
```

### 3.2 Deployment

#### Paso 1: Crear cuenta

1. Ir a [render.com](https://render.com)
2. Hacer clic en "Get Started"
3. Iniciar sesión con GitHub

#### Paso 2: Nuevo Web Service

1. Dashboard → "New +"
2. Seleccionar "Web Service"
3. Conectar repositorio de GitHub

#### Paso 3: Configurar

```
Name: discord-music-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python src/bot.py
Plan: Free
```

#### Paso 4: Variables de Entorno

En "Environment":

```
DISCORD_TOKEN = tu_token
SPOTIFY_CLIENT_ID = tu_client_id
SPOTIFY_CLIENT_SECRET = tu_secret
PREFIX = !
```

#### Paso 5: Deploy

1. Hacer clic en "Create Web Service"
2. Render desplegará automáticamente
3. Ver logs en tiempo real

### 3.3 Mantener Activo

Render tiene un sleep más tolerante (15 minutos), pero aún así necesita:

1. Añadir health check endpoint (ver código en sección Railway)
2. Usar UptimeRobot para hacer ping cada 5 minutos

---

## 4. Replit

### Ventajas
✅ Extremadamente fácil para principiantes
✅ IDE en el navegador
✅ No requiere GitHub
✅ Comunidad activa

### Desventajas
❌ Sleep después de inactividad
❌ Recursos compartidos (puede ser lento)
❌ Menos profesional

### 4.1 Deployment

#### Paso 1: Crear Repl

1. Ir a [replit.com](https://replit.com)
2. Hacer clic en "+ Create"
3. Seleccionar "Python"
4. Nombrar: "discord-music-bot"

#### Paso 2: Subir Código

1. Usar el explorador de archivos para subir/crear archivos
2. O importar desde GitHub: "Import from GitHub"

#### Paso 3: Configurar Secrets

1. Hacer clic en el icono de candado (Secrets)
2. Añadir:
   ```
   DISCORD_TOKEN = tu_token
   SPOTIFY_CLIENT_ID = tu_id
   SPOTIFY_CLIENT_SECRET = tu_secret
   ```

#### Paso 4: Instalar Dependencias

En el Shell:

```bash
pip install -r requirements.txt
```

#### Paso 5: Run

1. Hacer clic en "Run"
2. El bot se iniciará

### 4.2 Mantener Activo

**Método 1: UptimeRobot**

1. Crear web server en bot:

```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# En main()
keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
```

2. Obtener URL de Replit
3. Configurar en UptimeRobot

**Método 2: Replit Always On (Requiere Hacker Plan - $7/mes)**

---

## 5. Oracle Cloud Free Tier

### Ventajas
✅ SIEMPRE gratuito (no trial)
✅ Recursos generosos (1GB RAM, 1 vCPU)
✅ Sin límite de horas
✅ No duerme
✅ IP pública estática

### Desventajas
❌ Configuración compleja
❌ Requiere conocimientos de Linux
❌ Requiere tarjeta de crédito (no se cobra)

### 5.1 Requisitos

- Cuenta de Oracle Cloud (requiere tarjeta)
- Conocimientos básicos de Linux
- SSH client

### 5.2 Setup Rápido

#### Paso 1: Crear VM

1. Ir a [cloud.oracle.com](https://cloud.oracle.com)
2. Console → Compute → Instances
3. Create Instance:
   - Name: discord-bot
   - Image: Ubuntu 22.04
   - Shape: VM.Standard.A1.Flex (ARM - GRATUITO)
   - RAM: 1GB
   - Storage: 50GB
4. Descargar SSH key
5. Create

#### Paso 2: Conectar via SSH

```bash
ssh -i /path/to/key ubuntu@your_vm_ip
```

#### Paso 3: Instalar Dependencias

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Instalar FFmpeg
sudo apt install ffmpeg -y

# Instalar Git
sudo apt install git -y
```

#### Paso 4: Clonar Repositorio

```bash
cd ~
git clone https://github.com/tu-usuario/discord-music-bot.git
cd discord-music-bot
```

#### Paso 5: Setup Python

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Paso 6: Configurar .env

```bash
nano .env
```

Pegar:
```env
DISCORD_TOKEN=tu_token
SPOTIFY_CLIENT_ID=tu_id
SPOTIFY_CLIENT_SECRET=tu_secret
PREFIX=!
```

Guardar: `Ctrl+X`, `Y`, `Enter`

#### Paso 7: Crear Servicio Systemd

```bash
sudo nano /etc/systemd/system/discord-bot.service
```

Contenido:

```ini
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-music-bot
Environment="PATH=/home/ubuntu/discord-music-bot/venv/bin"
ExecStart=/home/ubuntu/discord-music-bot/venv/bin/python src/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Paso 8: Iniciar Servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-bot
sudo systemctl start discord-bot

# Ver status
sudo systemctl status discord-bot

# Ver logs
sudo journalctl -u discord-bot -f
```

### 5.3 Actualizar Bot

```bash
cd ~/discord-music-bot
git pull
sudo systemctl restart discord-bot
```

---

## 6. Mantener el Bot Activo 24/7

### UptimeRobot (Recomendado)

**Qué es:** Servicio gratuito que hace ping a tu bot para mantenerlo activo.

#### Setup

1. Ir a [uptimerobot.com](https://uptimerobot.com)
2. Crear cuenta gratuita
3. Add New Monitor:
   - Monitor Type: HTTP(s)
   - Friendly Name: Discord Bot
   - URL: Tu URL de health endpoint
   - Monitoring Interval: 5 minutos
4. Create Monitor

#### Configurar Health Endpoint

```python
# src/bot.py
from aiohttp import web
import asyncio

async def health_check(request):
    return web.Response(text="OK")

async def run_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Puerto 8080 para Railway/Render
    port = int(os.getenv('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f'✅ Web server running on port {port}')

# En main()
async def main():
    bot = MusicBot()
    
    # Iniciar web server en background
    asyncio.create_task(run_web_server())
    
    # Iniciar bot
    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 7. Monitoreo y Logs

### 7.1 Ver Logs en Railway

```
Dashboard → Tu proyecto → Deployments → Ver logs en tiempo real
```

### 7.2 Ver Logs en Render

```
Dashboard → Tu servicio → Logs
```

### 7.3 Ver Logs en Oracle Cloud

```bash
# SSH a la VM
sudo journalctl -u discord-bot -f

# Ver últimas 100 líneas
sudo journalctl -u discord-bot -n 100
```

### 7.4 Configurar Alertas

#### Discord Webhook para Errores

```python
import aiohttp

async def send_error_webhook(error_message):
    webhook_url = os.getenv('ERROR_WEBHOOK_URL')
    if not webhook_url:
        return
    
    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json={
            'content': f'🚨 **Error en el bot:**\n```{error_message}```'
        })

# En on_error
async def on_error(self, event, *args, **kwargs):
    logger.error(f'Error en {event}', exc_info=True)
    await send_error_webhook(f'{event}: {args}')
```

---

## 8. Costos Estimados

### Plan Completamente Gratuito

| Servicio | Costo/mes | Notas |
|----------|-----------|-------|
| Railway | $0 | 500 horas |
| Render | $0 | 750 horas |
| Replit | $0 | Con workarounds |
| Oracle Cloud | $0 | Siempre gratuito |
| UptimeRobot | $0 | 50 monitores |
| **TOTAL** | **$0.00** | ✅ 100% gratis |

### Plan Recomendado (Opcional)

| Servicio | Costo/mes | Beneficio |
|----------|-----------|-----------|
| Replit Hacker | $7 | Always On |
| Railway Pro | $5 | Sin sleep |
| Render Pro | $7 | Sin sleep |

**Recomendación:** Usar Oracle Cloud para 100% gratis 24/7.

---

## 9. Checklist Final

### Pre-Deployment
- [ ] Código probado localmente
- [ ] `.env` configurado
- [ ] `.gitignore` incluye `.env`
- [ ] `requirements.txt` actualizado
- [ ] Health check endpoint añadido

### Post-Deployment
- [ ] Bot online en Discord
- [ ] Comandos funcionando
- [ ] Reproducción de música funciona
- [ ] UptimeRobot configurado
- [ ] Logs monitoreados

### Mantenimiento
- [ ] Actualizar yt-dlp regularmente
- [ ] Revisar logs semanalmente
- [ ] Backup de base de datos (si aplica)
- [ ] Actualizar dependencias mensualmente

---

## 10. Resolución de Problemas

### Bot se desconecta frecuentemente

**Causa:** Sleep de la plataforma gratuita.

**Solución:**
1. Verificar UptimeRobot está activo
2. Verificar health endpoint responde
3. Considerar Oracle Cloud

### Out of Memory

**Causa:** Demasiadas canciones en cola.

**Solución:**
```python
MAX_QUEUE_SIZE = 50  # Reducir límite
```

### Bot lento en Replit

**Causa:** Recursos compartidos.

**Solución:** Migrar a Railway/Render/Oracle.

---

**¡Tu bot está ahora desplegado 24/7 completamente gratis! 🎉**

**Siguiente:** Ver [COMANDOS.md](COMANDOS.md) para lista completa de comandos
