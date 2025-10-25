# 🔑 GUÍA DEFINITIVA: Cookies de YouTube para Servidores

## ⚠️ PROBLEMA ACTUAL

Tu error muestra:
```
ERROR: [youtube] Sign in to confirm you're not a bot
```

Esto significa que las cookies en tu servidor **NO son válidas** o **han expirado**.

---

## ✅ SOLUCIÓN GARANTIZADA EN 5 PASOS

### 📋 Paso 1: Instalar Extensión de Chrome

**Usa ESTA extensión (la más confiable):**

1. Abre Chrome
2. Ve a: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
3. Click en "Añadir a Chrome"

### 📋 Paso 2: Autenticarte en YouTube

1. Ve a https://www.youtube.com
2. **CIERRA SESIÓN** si ya estás logueado
3. **INICIA SESIÓN** de nuevo con tu cuenta
4. Asegúrate de ver tu perfil arriba a la derecha

### 📋 Paso 3: Exportar Cookies CORRECTAMENTE

1. Estando en youtube.com (cualquier página de YouTube)
2. Haz clic en el ícono de la extensión "Get cookies.txt locally"
3. Verás una lista de cookies
4. Haz clic en **"Export"** o **"Export As..."**
5. Se descargará un archivo llamado `youtube.com_cookies.txt` o similar

### 📋 Paso 4: Verificar el Archivo

Abre el archivo `cookies.txt` descargado con un editor de texto.

**DEBE verse así:**
```
# Netscape HTTP Cookie File
# http://www.netscape.com/newsref/std/cookie_spec.html
# This is a generated file!  Do not edit.

.youtube.com	TRUE	/	TRUE	1794820533	__Secure-1PAPISID	rwIq7tdyRymX2Q01/ACr_2ycM775bPi3gt
.youtube.com	TRUE	/	TRUE	1794820533	__Secure-1PSID	g.a0002Qgb7PBdeMftzIxhdfCDxwMM38u-3NMP0MbZRrEWxCRSQZYeOt8H-0jKHkr5NODYPK78sQACgYKAaMSARMSFQHGX2MilKCQMxOZrM0oguMy-1SNlhoVAUF8yKqJQga17s3r7etcOIaydza90076
.youtube.com	TRUE	/	FALSE	1794820533	SAPISID	UzIVEH6v45dSLmCU/AcP1VyAzynmcv5PuD
.youtube.com	TRUE	/	FALSE	1794820533	SID	g.a0002Qgb7PBdeMftzIxhdfCDxwMM38u-3NMP0MbZRrEWxCRSQZYehwQ2e46ngM29cywz7EQyGwACgYKAWQSARMSFQHGX2MiGwtSR_b2pkZ3Yvj53NL4zBoVAUF8yKoWwd5gs9COr9iVrzV3xiip0076
... (más cookies)
```

**✅ Verificaciones importantes:**
- [ ] Primera línea dice "# Netscape HTTP Cookie File"
- [ ] Hay cookies con nombres SAPISID, SID, SSID
- [ ] Cada línea tiene formato: dominio + campos separados por TABs
- [ ] NO hay espacios extra o caracteres raros

### 📋 Paso 5: Subir a Render

1. Ve a tu servicio en Render: https://dashboard.render.com
2. Ve a "Environment"
3. En "Secret Files":
   - Si ya existe `cookies.txt`, **ELIMÍNALO** primero
   - Click en "Add Secret File"
   - Filename: `cookies.txt`
   - Contents: **PEGA TODO EL CONTENIDO** del archivo que descargaste
4. Verifica que `YOUTUBE_COOKIES_FILE` esté configurado:
   - Variable: `YOUTUBE_COOKIES_FILE`
   - Value: `/etc/secrets/cookies.txt`
5. **Reinicia el servicio** (Manual Deploy o espera redeploy automático)

---

## 🔍 VERIFICACIÓN POST-DEPLOY

Después del deploy, revisa los logs. Deberías ver:

✅ **CORRECTO:**
```
📋 Cookies copiadas de /etc/secrets/cookies.txt a /tmp/youtube_cookies.txt
✅ Usando cookies desde archivo: /tmp/youtube_cookies.txt
✓ Archivo de cookies válido: 25 cookies de YouTube encontradas
✓ Cookies de autenticación encontradas: SAPISID, SSID, SID
```

❌ **INCORRECTO:**
```
⚠️ Archivo de cookies no tiene header de Netscape
⚠️ No se encontraron cookies de autenticación importantes
```

---

## 🐛 SI SIGUE SIN FUNCIONAR

### Problema: "Sign in to confirm you're not a bot" persiste

**Causa:** Las cookies exportadas no incluyen todas las necesarias.

**Solución:**
1. En YouTube, **navega a varios videos** (reproduce 2-3 videos)
2. Esto genera cookies adicionales necesarias
3. **EXPORTA COOKIES OTRA VEZ** con la extensión
4. Reemplaza el archivo en Render

### Problema: Cookies expiran rápidamente

**Solución:**
- Las cookies de YouTube duran ~30 días
- Cada 30 días aproximadamente deberás regenerarlas
- Considera automatizar esto o usar una cuenta dedicada para el bot

### Problema: "Archivo de cookies no tiene header de Netscape"

**Solución:**
- Asegúrate de usar la extensión "Get cookies.txt locally"
- NO uses "EditThisCookie" u otras extensiones (formato incorrecto)
- Exporta en formato "Netscape HTTP Cookie File"

---

## 🎯 EXTENSIÓN ALTERNATIVA (Si la primera no funciona)

Si "Get cookies.txt locally" no funciona:

1. **Instala:** https://chrome.google.com/webstore/detail/cookies-txt-one-click/hkjnneoinmcifckpjpdfjkdmafkfhmfb
2. Ve a youtube.com
3. Haz clic en la extensión
4. Click en "Export" → Se descargará cookies.txt
5. Sube a Render como en Paso 5

---

## 📞 CHECKLIST FINAL

Antes de declarar que no funciona, verifica que:

- [ ] Estoy autenticado en YouTube al momento de exportar
- [ ] El archivo tiene el header "# Netscape HTTP Cookie File"
- [ ] El archivo tiene cookies SAPISID, SID, SSID
- [ ] Subí el contenido COMPLETO del archivo a Render Secret Files
- [ ] La variable YOUTUBE_COOKIES_FILE = /etc/secrets/cookies.txt
- [ ] Reinicié el servicio en Render después de subir
- [ ] Los logs muestran "✅ Usando cookies desde archivo"
- [ ] Los logs muestran "✓ Cookies de autenticación encontradas"

Si TODOS están ✅ y sigue sin funcionar, puede ser restricción de YouTube a IPs de Render.

---

## 🔄 REGENERAR COOKIES (Cada 30 días)

YouTube cookies expiran. Cuando veas el error de nuevo:

1. Ve a youtube.com en Chrome
2. Verifica que sigues autenticado
3. Exporta cookies con la extensión
4. Reemplaza el Secret File en Render
5. Reinicia el servicio

**TIP:** Establece un recordatorio mensual para regenerar las cookies.