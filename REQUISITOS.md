# 📋 REQUISITOS.md - Requisitos Técnicos Detallados

## 1. Requisitos Funcionales

### 1.1 Reproducción de Música

#### RF-001: Reproducción desde YouTube
- **Prioridad:** Alta
- **Descripción:** El bot debe poder reproducir audio desde enlaces de YouTube
- **Criterios de aceptación:**
  - Aceptar enlaces de videos individuales de YouTube
  - Aceptar enlaces de playlists de YouTube
  - Extraer y reproducir el audio sin descargar el video completo
  - Soportar videos de hasta 2 horas de duración
- **Dependencias:** yt-dlp, FFmpeg

#### RF-002: Reproducción desde Spotify
- **Prioridad:** Alta
- **Descripción:** El bot debe convertir enlaces de Spotify a YouTube y reproducir
- **Criterios de aceptación:**
  - Aceptar enlaces de tracks de Spotify
  - Aceptar enlaces de álbumes de Spotify
  - Aceptar enlaces de playlists de Spotify
  - Buscar equivalente en YouTube basándose en metadatos
  - Tasa de éxito de coincidencia >90%
- **Dependencias:** spotipy, Spotify API

#### RF-003: Sistema de Búsqueda
- **Prioridad:** Media
- **Descripción:** Permitir búsqueda de canciones por nombre
- **Criterios de aceptación:**
  - Buscar por nombre de canción y artista
  - Mostrar top 5 resultados con reacciones para seleccionar
  - Timeout de selección de 30 segundos
  - Añadir resultado seleccionado a la cola
- **Dependencias:** yt-dlp

### 1.2 Gestión de Cola

#### RF-004: Cola de Reproducción
- **Prioridad:** Alta
- **Descripción:** Sistema FIFO para gestión de múltiples canciones
- **Criterios de aceptación:**
  - Añadir canciones al final de la cola
  - Reproducir automáticamente siguiente canción
  - Mostrar cola actual con numeración
  - Eliminar canciones específicas de la cola
  - Limpiar cola completa
- **Capacidad máxima:** 100 canciones por servidor

#### RF-005: Manipulación de Cola
- **Prioridad:** Media
- **Descripción:** Operaciones avanzadas sobre la cola
- **Criterios de aceptación:**
  - Mezclar orden de la cola (shuffle)
  - Mover canciones de posición
  - Saltar a canción específica
  - Repetir canción actual o toda la cola
- **Dependencias:** RF-004

### 1.3 Controles de Reproducción

#### RF-006: Controles Básicos
- **Prioridad:** Alta
- **Descripción:** Comandos esenciales de control
- **Lista de controles:**
  - `play <url/query>` - Reproducir o añadir a cola
  - `pause` - Pausar reproducción
  - `resume` - Reanudar reproducción
  - `skip` - Saltar canción actual
  - `stop` - Detener y limpiar cola
  - `volume <0-100>` - Ajustar volumen

#### RF-007: Controles Avanzados
- **Prioridad:** Media
- **Descripción:** Funcionalidades adicionales de control
- **Lista de controles:**
  - `loop [song/queue/off]` - Modo de repetición
  - `shuffle` - Mezclar cola
  - `seek <timestamp>` - Saltar a tiempo específico
  - `previous` - Volver a canción anterior
  - `jump <número>` - Saltar a canción específica

### 1.4 Información y Visualización

#### RF-008: Now Playing
- **Prioridad:** Media
- **Descripción:** Mostrar información de canción actual
- **Criterios de aceptación:**
  - Título de la canción
  - Nombre del artista/canal
  - Duración total
  - Tiempo transcurrido con barra de progreso
  - Thumbnail de la canción
  - Usuario que solicitó la canción
- **Formato:** Embed de Discord enriquecido

#### RF-009: Visualización de Cola
- **Prioridad:** Media
- **Descripción:** Mostrar lista de canciones en espera
- **Criterios de aceptación:**
  - Paginación (10 canciones por página)
  - Tiempo total estimado
  - Navegación con reacciones
  - Indicador de canción actual

### 1.5 Funcionalidades Adicionales

#### RF-010: Sistema de Favoritos
- **Prioridad:** Baja
- **Descripción:** Guardar canciones favoritas por usuario
- **Criterios de aceptación:**
  - Añadir canción actual a favoritos
  - Listar favoritos personales
  - Reproducir desde favoritos
  - Eliminar de favoritos
  - Límite de 50 favoritos por usuario

#### RF-011: Estadísticas
- **Prioridad:** Baja
- **Descripción:** Tracking de uso del bot
- **Métricas:**
  - Total de canciones reproducidas
  - Tiempo total de reproducción
  - Top 10 canciones más reproducidas
  - Usuarios más activos
  - Horarios de mayor uso

## 2. Requisitos No Funcionales

### 2.1 Rendimiento

#### RNF-001: Tiempo de Respuesta
- Respuesta a comandos: <2 segundos
- Inicio de reproducción: <5 segundos
- Carga de playlist completa: <10 segundos

#### RNF-002: Capacidad
- Soportar hasta 50 servidores simultáneos
- Máximo 1 reproducción por servidor a la vez
- Cola máxima de 100 canciones por servidor

### 2.2 Disponibilidad

#### RNF-003: Uptime
- Disponibilidad objetivo: 95%+
- Reconexión automática en caso de desconexión
- Recuperación automática de errores

#### RNF-004: Escalabilidad
- Arquitectura preparada para sharding (futuro)
- Uso eficiente de memoria (<512MB RAM)
- CPU usage <50% en operación normal

### 2.3 Seguridad

#### RNF-005: Autenticación
- Token de Discord almacenado de forma segura
- No exponer credenciales en logs
- Variables de entorno para datos sensibles

#### RNF-006: Permisos
- Verificar permisos de canal de voz antes de unirse
- Verificar permisos de envío de mensajes
- Manejo seguro de comandos administrativos

### 2.4 Usabilidad

#### RNF-007: Interfaz de Usuario
- Comandos intuitivos y descriptivos
- Mensajes de error claros y accionables
- Embeds visuales atractivos
- Soporte de prefijo personalizable

#### RNF-008: Documentación
- Comando `help` con lista completa
- Ejemplos de uso para cada comando
- README completo en repositorio

### 2.5 Mantenibilidad

#### RNF-009: Código
- Código modular usando Cogs
- Comentarios en funciones complejas
- Manejo de excepciones completo
- Logs estructurados

#### RNF-010: Deployment
- Configuración mediante variables de entorno
- Proceso de deployment automatizado
- Rollback sencillo en caso de errores

## 3. Requisitos Técnicos del Sistema

### 3.1 Software

#### Python
- Versión: 3.10 o superior
- Recomendado: 3.11

#### Bibliotecas Python Principales
```
discord.py>=2.3.0
yt-dlp>=2023.10.13
PyNaCl>=1.5.0
spotipy>=2.23.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
```

#### FFmpeg
- Versión: 4.4 o superior
- Requerido para procesamiento de audio

### 3.2 Hardware (Mínimo)

#### Para Desarrollo Local
- CPU: 2 cores
- RAM: 2GB
- Almacenamiento: 1GB
- Conexión: 5 Mbps upload

#### Para Producción (Hosting Gratuito)
- CPU: 0.5 vCPU (Railway/Render)
- RAM: 512MB
- Almacenamiento: 1GB
- Ancho de banda: Ilimitado

### 3.3 APIs y Servicios Externos

#### Discord API
- Application registrada en Discord Developer Portal
- Bot Token generado
- Intents necesarios:
  - Guild Voice States
  - Guild Messages
  - Message Content (para comandos)

#### Spotify API
- Application registrada en Spotify Developer Dashboard
- Client ID obtenido
- Client Secret obtenido
- Límites: 180 requests/minuto (tier gratuito)

#### YouTube (via yt-dlp)
- Sin API key necesaria
- Sin límites de requests
- Nota: Puede requerir rotación de IP en algunos casos

## 4. Restricciones y Limitaciones

### 4.1 Restricciones Técnicas
- No descarga completa de archivos (streaming only)
- Un canal de voz por servidor simultáneamente
- Dependencia de servicios de terceros (YouTube, Spotify)
- Posibles bloqueos de IP por YouTube

### 4.2 Restricciones Legales
- Uso personal y educativo únicamente
- No redistribución comercial
- Cumplimiento con ToS de Discord
- Respeto a copyright de contenido reproducido

### 4.3 Limitaciones de Hosting Gratuito
- Railway: 500 horas/mes, sleep después de 5min inactividad
- Render: 750 horas/mes, sleep después de 15min inactividad
- Replit: Requiere UptimeRobot para mantener activo
- Oracle: Sin limitaciones pero requiere configuración avanzada

## 5. Casos de Uso

### Caso de Uso 1: Reproducir canción desde YouTube
**Actor:** Usuario de Discord
**Precondición:** Bot en el servidor y usuario en canal de voz
**Flujo principal:**
1. Usuario escribe `!play https://youtube.com/watch?v=xxxxx`
2. Bot se une al canal de voz del usuario
3. Bot extrae información del video
4. Bot comienza reproducción
5. Bot muestra mensaje "Now Playing"
**Postcondición:** Música reproduciéndose en canal de voz

### Caso de Uso 2: Crear cola desde playlist de Spotify
**Actor:** Usuario de Discord
**Precondición:** Bot en el servidor
**Flujo principal:**
1. Usuario escribe `!play https://open.spotify.com/playlist/xxxxx`
2. Bot extrae metadatos de la playlist
3. Bot busca cada canción en YouTube
4. Bot añade todas las canciones a la cola
5. Bot comienza reproducción de la primera
**Postcondición:** Playlist completa en cola y reproduciéndose

### Caso de Uso 3: Búsqueda de canción
**Actor:** Usuario de Discord
**Precondición:** Bot en el servidor
**Flujo principal:**
1. Usuario escribe `!play despacito`
2. Bot busca en YouTube
3. Bot muestra top 5 resultados con reacciones (1️⃣-5️⃣)
4. Usuario reacciona con número deseado
5. Bot añade canción seleccionada a cola
**Postcondición:** Canción añadida a cola

## 6. Métricas de Éxito

- ✅ Tasa de éxito de reproducción >95%
- ✅ Tiempo de respuesta promedio <3 segundos
- ✅ Uptime >95%
- ✅ 0 crashes por errores conocidos
- ✅ Uso de memoria <512MB
- ✅ Soporte de 50+ servidores simultáneos

## 7. Dependencias Externas

| Servicio | Propósito | Gratuito | Límites |
|----------|-----------|----------|---------|
| Discord API | Plataforma del bot | Sí | Rate limit: 50 req/s |
| Spotify API | Metadatos de música | Sí | 180 req/min |
| YouTube (yt-dlp) | Streaming de audio | Sí | Soft limits |
| Railway/Render | Hosting | Sí | 500-750 hrs/mes |
| FFmpeg | Procesamiento audio | Sí | N/A |
