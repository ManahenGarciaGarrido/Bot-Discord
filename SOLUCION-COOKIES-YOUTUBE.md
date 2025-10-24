# 🔧 SOLUCIÓN: Error de Cookies de YouTube

## ❌ Problema

YouTube está bloqueando las requests del bot con este error:
```
ERROR: could not find chrome cookies database in "/root/.config/google-chrome"
ERROR: Sign in to confirm you're not a bot.
```

**Causa del error:**
El bot está corriendo en un servidor (Railway, Render, VPS, etc.) que **NO tiene navegadores instalados**. No puede leer las cookies de Chrome/Edge/Firefox porque esos navegadores no existen en el servidor.

---

## 🎯 Solución Correcta Según tu Caso

### 📍 **¿Dónde corre tu bot?**

#### **A) Bot en SERVIDOR (Railway, Render, Docker, VPS)**
**→ Usa: Archivo de cookies (cookies.txt)**

Los servidores no tienen navegadores instalados. La única solución es usar un archivo de cookies exportado.

#### **B) Bot en TU PC LOCAL**
**→ Usa: Cookies del navegador**

Si el bot corre en tu computadora personal, puede leer las cookies directamente de tu navegador.

---

## 🚀 Solución Recomendada: Archivo de Cookies

**Esta es la solución universal que funciona en cualquier servidor.**

### Paso 1: Exportar Cookies (en tu PC local)

Tenemos un script automático que hace todo por ti:

```bash
# En tu PC local (NO en el servidor)
python scripts/export_cookies.py chrome
```

**Navegadores soportados:**
- `chrome` - Google Chrome
- `firefox` - Mozilla Firefox
- `edge` - Microsoft Edge
- `brave` - Brave Browser
- `opera` - Opera

**Requisitos previos:**
1. Instalar la dependencia:
   ```bash
   pip install browser-cookie3
   ```

2. Estar autenticado en YouTube en ese navegador

El script generará un archivo `cookies.txt` en el directorio actual.

### Paso 2: Subir el archivo a tu servidor

**Opción A: Usando Secret Files (RECOMENDADO - más seguro)**

**Para Railway:**
1. Ve a tu proyecto en Railway
2. Variables → Add Variable
3. Key: `YOUTUBE_COOKIES_FILE`
4. Value: `/app/cookies.txt`
5. Luego ve a "Secret Files" y pega el contenido de cookies.txt

**Para Render:**
1. Ve a tu servicio en Render
2. Environment → Secret Files
3. Filename: `cookies.txt`
4. Contents: [pega el contenido completo de tu archivo cookies.txt]
5. Add Variable:
   - Key: `YOUTUBE_COOKIES_FILE`
   - Value: `/etc/secrets/cookies.txt`

**Opción B: Subir al repositorio (solo si es privado)**
```bash
# En tu PC local
# 1. Copia el archivo al proyecto
cp cookies.txt /ruta/a/Bot-Discord/

# 2. Añade a .env (o configura en tu plataforma)
echo "YOUTUBE_COOKIES_FILE=/app/cookies.txt" >> .env

# 3. Sube al repositorio (SOLO si es privado)
git add cookies.txt
git commit -m "Add YouTube cookies"
git push
```

**⚠️ IMPORTANTE:** Las cookies son sensibles. Si tu repositorio es **público**, usa Secret Files de tu plataforma.

### Paso 3: Configurar en tu .env

Añade esta línea a tu archivo `.env`:

```env
YOUTUBE_COOKIES_FILE=/app/cookies.txt
```

**Nota:** La ruta cambia según tu plataforma:
- Railway: `/app/cookies.txt`
- Render (con Secret Files): `/etc/secrets/cookies.txt`
- Docker: `/app/cookies.txt`
- VPS: La ruta donde subas el archivo

### Paso 4: Reiniciar el bot

Después de configurar, reinicia tu bot. En los logs deberías ver:

```
✅ Usando cookies desde archivo: /app/cookies.txt
```

---

## 💻 Alternativa: Usar Cookies del Navegador (Solo PC Local)

**⚠️ ADVERTENCIA:** Esta opción **NO funciona en servidores**. Solo úsala si el bot corre en tu PC.

### Paso 1: Configurar .env

```env
COOKIES_BROWSER=chrome
```

### Paso 2: Verificar requisitos

1. Tener Chrome instalado localmente
2. Estar autenticado en YouTube en Chrome
3. El bot debe correr en la misma PC

### Paso 3: Reiniciar bot

```bash
python -m src.bot
```

Deberías ver:
```
⚙️  Configurado para usar cookies de chrome
```

---

## 🐛 Troubleshooting

### ❌ Error: "could not find chrome cookies database"

**Causa:** Estás usando `COOKIES_BROWSER=edge` pero el bot está en un servidor sin navegadores.

**Solución:** Elimina `COOKIES_BROWSER` del .env y usa `YOUTUBE_COOKIES_FILE` con un archivo exportado.

```env
# ❌ NO hagas esto en servidores:
COOKIES_BROWSER=edge

# ✅ HAZ esto en servidores:
YOUTUBE_COOKIES_FILE=/app/cookies.txt
```

---

### ❌ Error: "NO HAY COOKIES CONFIGURADAS"

El bot mostrará un mensaje de error largo explicando qué hacer.

**Solución rápida:**
1. Ejecuta en tu PC: `python scripts/export_cookies.py chrome`
2. Sube el `cookies.txt` generado a tu servidor
3. Configura `YOUTUBE_COOKIES_FILE=/app/cookies.txt`
4. Reinicia el bot

---

### ❌ Error al exportar cookies: "browser_cookie3 not found"

**Solución:**
```bash
pip install browser-cookie3
```

---

### ❌ Script de exportación falla

**Método alternativo manual:**

1. **Instala una extensión del navegador:**

   **Para Chrome/Edge/Brave:**
   - Busca "Get cookies.txt" en Chrome Web Store
   - O usa "EditThisCookie"

   **Para Firefox:**
   - Busca "cookies.txt" en Firefox Add-ons

2. **Exporta las cookies:**
   - Ve a https://youtube.com
   - Asegúrate de estar autenticado
   - Haz clic en la extensión
   - Exporta en formato "Netscape" o "cookies.txt"
   - Guarda el archivo

3. **Sube el archivo a tu servidor** (ver Paso 2 arriba)

---

## 📊 Orden de Prioridad del Bot

El bot intenta en este orden:

1. ✅ **YOUTUBE_COOKIES_FILE** - Archivo de cookies (RECOMENDADO para servidores)
2. ✅ **COOKIES_BROWSER** - Cookies del navegador (solo PC local)
3. ❌ **Sin cookies** - Mostrará error y guía de solución

---

## 💡 Recomendaciones por Caso de Uso

### 🖥️ Para Desarrollo Local (bot en tu PC):

```env
# Opción 1: Archivo (más confiable)
YOUTUBE_COOKIES_FILE=cookies.txt

# Opción 2: Navegador (más fácil)
COOKIES_BROWSER=chrome
```

**Pros de archivo:**
- ✅ Más confiable
- ✅ No depende del navegador
- ✅ Funciona incluso si cierras el navegador

**Pros de navegador:**
- ✅ Más fácil de configurar
- ✅ No requiere archivos adicionales
- ✅ Se actualiza si re-autentícas en YouTube

### 🌐 Para Servidores (Railway/Render/Docker/VPS):

```env
YOUTUBE_COOKIES_FILE=/app/cookies.txt
```

**Única opción válida para servidores:**
- ✅ No depende de navegadores instalados
- ✅ Portátil entre servidores
- ✅ Funciona en contenedores Docker
- ❌ Requiere exportar manualmente

---

## 🔐 Seguridad

**⚠️ Las cookies son credenciales sensibles:**

### ❌ NO hagas esto:
- Subir cookies.txt a GitHub público
- Compartir tu archivo de cookies
- Commitear cookies sin .gitignore

### ✅ SÍ haz esto:
- Usar Secret Files de tu plataforma (Railway/Render)
- Añadir cookies.txt a .gitignore
- Regenerar cookies si las expones accidentalmente

**El .gitignore ya incluye:**
```gitignore
cookies.txt
*.cookies
```

---

## 📋 Checklist Rápido

**Si tu bot está en un SERVIDOR:**

- [ ] Ejecuté `python scripts/export_cookies.py chrome` en mi PC
- [ ] Tengo el archivo `cookies.txt` generado
- [ ] Subí el archivo a Secret Files de mi plataforma
- [ ] Configuré `YOUTUBE_COOKIES_FILE=/app/cookies.txt` en .env
- [ ] Reinicié el bot
- [ ] Vi "✅ Usando cookies desde archivo" en los logs

**Si mi bot está en MI PC:**

- [ ] Estoy autenticado en YouTube en mi navegador
- [ ] Configuré `COOKIES_BROWSER=chrome` (o mi navegador) en .env
- [ ] Reinicié el bot
- [ ] Vi "⚙️ Configurado para usar cookies de chrome" en los logs

---

## 🎯 Resumen TL;DR

**Tu error:**
```
ERROR: could not find chrome cookies database
```

**Tu problema:**
- Configuraste `COOKIES_BROWSER=edge`
- Pero el bot está en un servidor sin navegadores instalados
- Los servidores NO tienen Chrome/Edge/Firefox

**Solución en 3 pasos:**

1. **En tu PC local:**
   ```bash
   python scripts/export_cookies.py chrome
   # o usa el navegador donde estés autenticado en YouTube
   ```

2. **Sube cookies.txt a tu servidor** (Railway/Render/etc.)

3. **Configura en .env:**
   ```env
   # Elimina esto:
   # COOKIES_BROWSER=edge

   # Añade esto:
   YOUTUBE_COOKIES_FILE=/app/cookies.txt
   ```

4. **Reinicia** y listo ✅

---

## 📞 Ayuda Adicional

Si después de seguir esta guía sigues teniendo problemas:

1. Verifica los logs del bot - te dirán exactamente qué falta
2. Asegúrate de estar autenticado en YouTube cuando exportes cookies
3. Verifica que la ruta del archivo sea correcta en tu plataforma
4. Prueba actualizar yt-dlp: `pip install --upgrade yt-dlp`

**El bot te guiará con mensajes de error claros si algo falta.**
