# Scripts de Utilidad

Este directorio contiene scripts de ayuda para configurar y mantener el bot.

## 🍪 export_cookies.py

Script para exportar cookies de YouTube desde tu navegador local.

### ¿Por qué necesito esto?

YouTube bloquea las peticiones del bot si no está autenticado. Este script extrae las cookies de tu navegador (donde ya estás autenticado en YouTube) y las guarda en un archivo que puedes subir a tu servidor.

### Uso

```bash
# Básico - usa Chrome por defecto
python scripts/export_cookies.py chrome

# Para otros navegadores
python scripts/export_cookies.py firefox
python scripts/export_cookies.py edge
python scripts/export_cookies.py brave
python scripts/export_cookies.py opera
```

### Requisitos

1. **Instalar dependencia:**
   ```bash
   pip install browser-cookie3
   ```

2. **Estar autenticado en YouTube:**
   - Abre tu navegador
   - Ve a https://youtube.com
   - Inicia sesión (si no lo has hecho)

3. **Ejecutar el script:**
   ```bash
   python scripts/export_cookies.py chrome
   ```

### Salida

El script genera un archivo `cookies.txt` en el directorio actual.

```
✅ Cookies exportadas exitosamente a: cookies.txt
📁 Ruta completa: /home/user/Bot-Discord/cookies.txt

📋 Próximos pasos:
   1. Sube el archivo cookies.txt a tu servidor
   2. En tu servidor, añade a .env:
      YOUTUBE_COOKIES_FILE=/app/cookies.txt
   3. Reinicia el bot
```

### Subir a tu servidor

**Para Railway:**
1. Ve a tu proyecto → Variables
2. Add Variable: `YOUTUBE_COOKIES_FILE=/app/cookies.txt`
3. Secret Files → Pega el contenido de cookies.txt

**Para Render:**
1. Ve a tu servicio → Environment
2. Secret Files → Filename: `cookies.txt`
3. Pega el contenido
4. Add Variable: `YOUTUBE_COOKIES_FILE=/etc/secrets/cookies.txt`

### Troubleshooting

**Error: "browser_cookie3 not found"**
```bash
pip install browser-cookie3
```

**Error al exportar cookies**
- Verifica que estés autenticado en YouTube en ese navegador
- Prueba con otro navegador
- Usa el método manual con una extensión (ver SOLUCION-COOKIES-YOUTUBE.md)

**El script no funciona**
- Consulta la guía completa: `SOLUCION-COOKIES-YOUTUBE.md`
- Usa el método alternativo con extensiones de navegador

### Seguridad

⚠️ **Las cookies son credenciales sensibles:**
- NO las compartas
- NO las subas a GitHub público
- cookies.txt ya está en .gitignore

### Más información

Ver guía completa en: [SOLUCION-COOKIES-YOUTUBE.md](../SOLUCION-COOKIES-YOUTUBE.md)
