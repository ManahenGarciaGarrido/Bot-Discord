# 🔧 SOLUCIÓN: Error de Cookies de YouTube

## ❌ Problema

YouTube está bloqueando las requests del bot con este error:
```
ERROR: Sign in to confirm you're not a bot.
Use --cookies-from-browser or --cookies for the authentication.
```

## ✅ Solución Implementada

El bot ahora usa **automáticamente las cookies de tu navegador** donde estás autenticado en YouTube.

---

## 🚀 Configuración Rápida (2 minutos)

### **Opción 1: Usar Navegador Automáticamente (RECOMENDADO)**

El bot intentará usar cookies de Chrome por defecto. Si usas otro navegador, configúralo:

**En tu archivo `.env`, añade:**
```env
COOKIES_BROWSER=chrome    # Para Chrome
# O cualquiera de estos:
# COOKIES_BROWSER=firefox
# COOKIES_BROWSER=edge
# COOKIES_BROWSER=brave
# COOKIES_BROWSER=safari
# COOKIES_BROWSER=opera
```

**Requisitos:**
1. Tener el navegador instalado
2. Estar autenticado en YouTube en ese navegador
3. Reiniciar el bot

### **Opción 2: Archivo de Cookies Manual** (Avanzado)

Si prefieres usar un archivo de cookies:

1. Exporta cookies de YouTube usando una extensión del navegador
2. Guarda el archivo como `cookies.txt`
3. En `.env`:
   ```env
   YOUTUBE_COOKIES_FILE=/ruta/completa/a/cookies.txt
   ```

---

## 📝 Pasos Detallados

### **Para Chrome (Recomendado):**

1. **Verificar que estás autenticado en YouTube:**
   - Abre Chrome
   - Ve a https://youtube.com
   - Verifica que estás logueado (deberías ver tu perfil)

2. **Configurar el bot:**
   ```env
   # En .env
   COOKIES_BROWSER=chrome
   ```

3. **Reiniciar el bot:**
   ```bash
   # Detener el bot (Ctrl+C)
   python -m src.bot
   ```

4. **Verificar en logs:**
   Deberías ver:
   ```
   ✅ Configured to use cookies from chrome
   ```

### **Para Firefox:**

1. Autenticado en YouTube en Firefox
2. En `.env`:
   ```env
   COOKIES_BROWSER=firefox
   ```
3. Reiniciar bot

### **Para Edge:**

1. Autenticado en YouTube en Edge
2. En `.env`:
   ```env
   COOKIES_BROWSER=edge
   ```
3. Reiniciar bot

---

## 🔍 Verificación

Después de configurar, el bot mostrará en los logs:

```
✅ Configured to use cookies from chrome
```

O:
```
⚠️  No cookies configured - YouTube may block requests
💡 Set COOKIES_BROWSER environment variable (chrome/firefox/edge)
```

---

## 🐛 Troubleshooting

### Problema: "Could not setup cookies from chrome"

**Solución 1:** Verifica que Chrome está instalado
```bash
# Windows: Buscar en Archivos de Programa
# Linux: which google-chrome
# Mac: open -a "Google Chrome"
```

**Solución 2:** Usa otro navegador
```env
COOKIES_BROWSER=firefox  # O edge, brave, etc.
```

**Solución 3:** Instala la versión más reciente de yt-dlp
```bash
pip install --upgrade yt-dlp
```

### Problema: "No cookies configured"

El bot intentará automáticamente varios navegadores. Si todos fallan:

1. **Instala y configura Chrome/Firefox**
2. **Asegúrate de estar autenticado en YouTube**
3. **Reinicia el bot**

### Problema: Sigue sin funcionar

**Opción manual con archivo de cookies:**

1. **Instala extensión del navegador:**
   - Chrome: "Get cookies.txt" (buscar en Chrome Web Store)
   - Firefox: "cookies.txt" extension

2. **Exporta cookies de YouTube:**
   - Ve a youtube.com
   - Usa la extensión para exportar
   - Guarda como `cookies.txt`

3. **Configura en .env:**
   ```env
   YOUTUBE_COOKIES_FILE=/ruta/completa/a/cookies.txt
   ```

4. **Reinicia el bot**

---

## 📊 Prioridad de Configuración

El bot intenta en este orden:

1. ✅ **YOUTUBE_COOKIES_FILE** (si está configurado)
2. ✅ **COOKIES_BROWSER** (navegador especificado)
3. ✅ **Auto-detección** (prueba chrome, firefox, edge, brave, opera, safari)
4. ⚠️ **Sin cookies** (puede fallar)

---

## 💡 Recomendaciones

### Para Desarrollo Local:
```env
COOKIES_BROWSER=chrome
```
- Más fácil
- No requiere archivos adicionales
- Se actualiza automáticamente

### Para Deployment (Railway/Render):
```env
YOUTUBE_COOKIES_FILE=/app/cookies.txt
```
- Más confiable en servidores
- Requiere subir archivo cookies.txt
- No depende de navegador instalado

---

## 🔐 Seguridad

**Las cookies son sensibles - NO las compartas:**
- ❌ No subas `cookies.txt` a GitHub
- ❌ No compartas tu archivo de cookies
- ✅ Usa `.gitignore` para excluir cookies.txt
- ✅ Usa variables de entorno en deployment

El `.gitignore` ya incluye:
```gitignore
cookies.txt
*.txt
```

---

## 🚀 Deployment en Railway/Render

### Método 1: Cookies del Navegador (NO funciona en servidores)

Los servidores no tienen navegadores instalados. Necesitas usar archivo de cookies.

### Método 2: Archivo de Cookies (RECOMENDADO)

1. **Exporta cookies localmente:**
   - Usa extensión del navegador
   - Guarda como `cookies.txt`

2. **Sube a tu repositorio:**
   ```bash
   # IMPORTANTE: Asegúrate que cookies.txt está en .gitignore
   # Solo súbelo de forma privada o usa secrets
   ```

3. **O mejor - usa secrets del servicio:**

   **Railway:**
   - Variables → Añadir variable multilinea
   - Nombre: `YOUTUBE_COOKIES_CONTENT`
   - Valor: [pega contenido de cookies.txt]

   **Render:**
   - Environment → Secret Files
   - File: `cookies.txt`
   - Content: [pega contenido]

4. **Configura en .env:**
   ```env
   YOUTUBE_COOKIES_FILE=/app/cookies.txt
   ```

---

## ✅ Solución Aplicada al Código

He actualizado automáticamente:
- ✅ `src/utils/youtube_handler.py` - Usa cookies automáticamente
- ✅ `src/config/settings.py` - Variables de entorno para cookies
- ✅ `.env.example` - Ejemplo de configuración

**Cambios:**
```python
# Ahora el bot automáticamente:
1. Busca YOUTUBE_COOKIES_FILE (archivo)
2. Si no, usa COOKIES_BROWSER (chrome por defecto)
3. Si no, intenta chrome, firefox, edge, brave, safari, opera
4. Si nada funciona, advierte pero intenta continuar
```

---

## 🎯 Resumen Ejecutivo

**Para solucionar AHORA:**

1. Añade a tu `.env`:
   ```env
   COOKIES_BROWSER=chrome
   ```

2. Asegúrate de estar autenticado en YouTube en Chrome

3. Reinicia el bot:
   ```bash
   python -m src.bot
   ```

4. Verifica logs:
   ```
   ✅ Configured to use cookies from chrome
   ```

5. ¡Listo! Ahora funcionará.

---

## 📞 Soporte

Si sigue sin funcionar:
1. Verifica que estás autenticado en YouTube en tu navegador
2. Prueba con otro navegador (Firefox, Edge)
3. Actualiza yt-dlp: `pip install --upgrade yt-dlp`
4. Usa método manual con cookies.txt

**El bot ahora manejará esto automáticamente en la mayoría de casos.**
