# 📖 COMANDOS.md - Lista Completa de Comandos

## Tabla de Contenidos
1. [Comandos de Música](#1-comandos-de-música)
2. [Comandos de Cola](#2-comandos-de-cola)
3. [Comandos de Playlists](#3-comandos-de-playlists)
4. [Comandos de Información](#4-comandos-de-información)
5. [Comandos Administrativos](#5-comandos-administrativos)
6. [Ejemplos de Uso](#6-ejemplos-de-uso)

**Prefijo por defecto:** `!`

---

## 1. Comandos de Música

### `!play` (aliases: `!p`)
Reproducir música desde YouTube, Spotify o búsqueda.

**Uso:**
```
!play <URL de YouTube>
!play <URL de Spotify>
!play <nombre de canción>
```

**Ejemplos:**
```
!play https://www.youtube.com/watch?v=dQw4w9WgXcQ
!play https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp
!play despacito
!p never gonna give you up
```

**Comportamiento:**
- Si no hay nada reproduciéndose, comienza inmediatamente
- Si hay música, añade a la cola
- Para búsquedas, muestra 5 resultados para seleccionar

**Permisos requeridos:** Ninguno (usuario debe estar en canal de voz)

---

### `!pause`
Pausar la reproducción actual.

**Uso:**
```
!pause
```

**Comportamiento:**
- Pausa la canción actual
- Mantiene la posición en la canción
- No afecta la cola

---

### `!resume` (aliases: `!unpause`)
Reanudar reproducción pausada.

**Uso:**
```
!resume
```

**Comportamiento:**
- Continúa desde donde se pausó
- Solo funciona si hay música pausada

---

### `!skip` (aliases: `!s`, `!next`)
Saltar a la siguiente canción.

**Uso:**
```
!skip
```

**Comportamiento:**
- Detiene la canción actual
- Reproduce la siguiente en la cola
- Si no hay más canciones, detiene la reproducción

---

### `!stop`
Detener reproducción y limpiar cola.

**Uso:**
```
!stop
```

**Comportamiento:**
- Detiene la música actual
- Limpia toda la cola
- El bot permanece en el canal de voz

---

### `!volume` (aliases: `!vol`, `!v`)
Ajustar el volumen de reproducción.

**Uso:**
```
!volume <0-100>
```

**Ejemplos:**
```
!volume 50
!vol 80
!v 25
```

**Comportamiento:**
- Cambia el volumen instantáneamente
- Se mantiene para las siguientes canciones
- Por defecto: 50%

---

### `!seek`
Saltar a un tiempo específico en la canción.

**Uso:**
```
!seek <MM:SS>
!seek <segundos>
```

**Ejemplos:**
```
!seek 1:30
!seek 90
```

**Comportamiento:**
- Salta al tiempo especificado
- Solo funciona mientras hay reproducción
- No disponible con streams en vivo

---

### `!loop` (aliases: `!repeat`)
Configurar modo de repetición.

**Uso:**
```
!loop [off|song|queue]
```

**Ejemplos:**
```
!loop song    # Repetir canción actual
!loop queue   # Repetir toda la cola
!loop off     # Desactivar repetición
!loop         # Alternar entre modos
```

**Comportamiento:**
- `song`: Repite la canción actual infinitamente
- `queue`: Cuando termina la cola, vuelve a empezar
- `off`: Reproducción normal

---

### `!shuffle`
Mezclar el orden de la cola.

**Uso:**
```
!shuffle
```

**Comportamiento:**
- Reorganiza aleatoriamente la cola
- No afecta la canción actual
- Útil para playlists largas

---

## 2. Comandos de Cola

### `!queue` (aliases: `!q`)
Mostrar cola de reproducción.

**Uso:**
```
!queue
!q
```

**Ejemplo de salida:**
```
🎵 Cola de Reproducción

▶️ Reproduciendo:
1. Never Gonna Give You Up - Rick Astley [3:33]

📝 En Cola:
2. Despacito - Luis Fonsi [3:48]
3. Shape of You - Ed Sheeran [3:54]
4. Bohemian Rhapsody - Queen [5:55]

Duración total: 17:10
```

**Comportamiento:**
- Paginación automática (10 canciones por página)
- Muestra duración total estimada
- Navegación con reacciones para cola larga

---

### `!remove` (aliases: `!rm`)
Eliminar canción de la cola.

**Uso:**
```
!remove <número>
```

**Ejemplos:**
```
!remove 3
!rm 5
```

**Comportamiento:**
- Elimina la canción en la posición especificada
- Los números se pueden ver con `!queue`
- No se puede eliminar la canción actual

---

### `!clear`
Limpiar toda la cola.

**Uso:**
```
!clear
```

**Comportamiento:**
- Elimina todas las canciones de la cola
- No afecta la canción actual
- Útil para empezar de cero

---

### `!jump`
Saltar a una canción específica en la cola.

**Uso:**
```
!jump <número>
```

**Ejemplos:**
```
!jump 5
```

**Comportamiento:**
- Salta a la canción especificada
- Las canciones previas se eliminan de la cola
- Similar a skip múltiple

---

### `!move`
Mover canción a otra posición.

**Uso:**
```
!move <posición_actual> <nueva_posición>
```

**Ejemplos:**
```
!move 5 2    # Mover canción 5 a posición 2
```

**Comportamiento:**
- Reorganiza la cola
- Útil para priorizar canciones

---

## 3. Comandos de Playlists

### `!favorite` (aliases: `!fav`, `!♥`)
Añadir canción actual a favoritos.

**Uso:**
```
!favorite
!fav
```

**Comportamiento:**
- Guarda la canción en tus favoritos personales
- Máximo 50 favoritos por usuario
- Vinculado a tu cuenta de Discord

---

### `!favorites` (aliases: `!favs`, `!flist`)
Ver lista de favoritos.

**Uso:**
```
!favorites
!favs
```

**Ejemplo de salida:**
```
❤️ Tus Favoritos

1. Never Gonna Give You Up - Rick Astley
2. Despacito - Luis Fonsi
3. Bohemian Rhapsody - Queen

Total: 3 canciones
Usa !playfav <número> para reproducir
```

---

### `!playfavorite` (aliases: `!playfav`, `!pf`)
Reproducir desde favoritos.

**Uso:**
```
!playfavorite <número>
!playfav <número>
!pf 1
```

**Ejemplos:**
```
!playfav 1
!pf 3
```

**Comportamiento:**
- Reproduce la canción especificada de tus favoritos
- Los números se ven con `!favorites`

---

### `!removefavorite` (aliases: `!rmfav`)
Eliminar de favoritos.

**Uso:**
```
!removefavorite <número>
!rmfav <número>
```

**Ejemplos:**
```
!removefavorite 2
!rmfav 5
```

---

### `!playallfavs`
Reproducir todos los favoritos.

**Uso:**
```
!playallfavs
```

**Comportamiento:**
- Añade todos tus favoritos a la cola
- En orden
- Útil para sesiones personalizadas

---

## 4. Comandos de Información

### `!nowplaying` (aliases: `!np`, `!current`)
Ver información de canción actual.

**Uso:**
```
!nowplaying
!np
```

**Ejemplo de salida:**
```
🎵 Reproduciendo Ahora

Never Gonna Give You Up
Rick Astley

⏱️ [━━━━━━━●────] 2:15 / 3:33
🔊 Volumen: 50%
🔁 Loop: Off
👤 Solicitado por: @Usuario

[Enlace] [Thumbnail]
```

---

### `!help` (aliases: `!h`, `!commands`)
Mostrar lista de comandos.

**Uso:**
```
!help
!help <comando>
```

**Ejemplos:**
```
!help
!help play
```

**Comportamiento:**
- Sin argumentos: Muestra todos los comandos
- Con comando específico: Muestra ayuda detallada

---

### `!ping`
Ver latencia del bot.

**Uso:**
```
!ping
```

**Ejemplo de salida:**
```
🏓 Pong! Latencia: 42ms
```

---

### `!stats` (aliases: `!statistics`)
Ver estadísticas del bot.

**Uso:**
```
!stats
```

**Ejemplo de salida:**
```
📊 Estadísticas del Bot

🎵 Canciones reproducidas: 1,234
⏱️ Tiempo total: 45h 23m
💿 Servidores activos: 15
👥 Usuarios totales: 1,532

🔝 Top 5 Canciones:
1. Never Gonna Give You Up (42x)
2. Despacito (38x)
3. Shape of You (35x)
...
```

---

## 5. Comandos Administrativos

### `!join` (aliases: `!j`, `!connect`)
Forzar al bot a unirse a tu canal.

**Uso:**
```
!join
!j
```

**Comportamiento:**
- El bot se une a tu canal de voz actual
- Útil si el bot está en otro canal

---

### `!leave` (aliases: `!disconnect`, `!dc`)
Forzar al bot a desconectarse.

**Uso:**
```
!leave
!dc
```

**Comportamiento:**
- El bot sale del canal de voz
- Limpia la cola automáticamente

---

### `!prefix`
Cambiar prefijo del bot (solo administradores).

**Uso:**
```
!prefix <nuevo_prefijo>
```

**Ejemplos:**
```
!prefix ?
!prefix music!
```

**Permisos requeridos:** Administrador del servidor

---

### `!reset`
Resetear configuración del servidor (solo administradores).

**Uso:**
```
!reset
```

**Comportamiento:**
- Restaura configuración por defecto
- Limpia cola
- Desconecta el bot

**Permisos requeridos:** Administrador del servidor

---

## 6. Ejemplos de Uso

### Escenario 1: Reproducción Básica

```
Usuario: !join
Bot: ✅ Conectado a General Voice

Usuario: !play bohemian rhapsody
Bot: [Muestra 5 resultados]
Usuario: [Reacciona con 1️⃣]
Bot: ▶️ Reproduciendo: Bohemian Rhapsody - Queen

Usuario: !volume 75
Bot: 🔊 Volumen ajustado a 75%
```

### Escenario 2: Crear Cola desde Playlist

```
Usuario: !play https://open.spotify.com/playlist/xxxxx
Bot: 🔄 Procesando playlist... 
Bot: ✅ 25 canciones añadidas a la cola
Bot: ▶️ Reproduciendo: Canción 1...

Usuario: !queue
Bot: [Muestra cola de 25 canciones]

Usuario: !shuffle
Bot: 🔀 Cola mezclada aleatoriamente

Usuario: !loop queue
Bot: 🔁 Modo repetición: Cola completa
```

### Escenario 3: Gestión de Favoritos

```
Usuario: !play never gonna give you up
Bot: ▶️ Reproduciendo: Never Gonna Give You Up

Usuario: !favorite
Bot: ❤️ Añadido a favoritos

Usuario: !favorites
Bot: [Muestra lista de favoritos]

Usuario: !playfav 1
Bot: ▶️ Reproduciendo desde favoritos...
```

### Escenario 4: Control Avanzado

```
Usuario: !play https://youtube.com/playlist?list=xxxxx
Bot: ✅ 50 canciones añadidas a la cola

Usuario: !skip
Bot: ⏭️ Canción saltada

Usuario: !jump 10
Bot: ⏩ Saltando a canción #10

Usuario: !remove 15
Bot: 🗑️ Canción #15 eliminada de la cola

Usuario: !move 20 5
Bot: ↕️ Canción movida de posición 20 a 5
```

---

## 7. Tips y Trucos

### 🎵 Reproducción Eficiente

1. **URLs directas son más rápidas** que búsquedas
2. **Playlists de YouTube** son más rápidas que de Spotify
3. **Evita videos muy largos** (>1 hora) en servidores activos

### 📝 Gestión de Cola

1. Usa `!shuffle` antes de `!loop queue` para variedad
2. `!jump` es más rápido que múltiples `!skip`
3. `!clear` + nueva playlist es mejor que eliminar uno a uno

### ❤️ Favoritos

1. Guarda tus canciones más reproducidas
2. Úsalos como "quick access"
3. Comparte tus favoritos con `!playallfavs`

### 🔧 Solución de Problemas

**Bot no responde:**
```
!ping    # Verificar conexión
```

**Canción no se reproduce:**
```
!skip    # Saltar a siguiente
!stop    # Reset completo
!play <url>    # Reintentar
```

**Bot en canal equivocado:**
```
!leave
!join
```

---

## 8. Atajos de Teclado (Discord)

- **Ctrl + K:** Búsqueda rápida de canales
- **Ctrl + I:** Abrir inbox
- **Ctrl + /** Mostrar atajos

---

## 9. Aliases Completos

| Comando | Aliases |
|---------|---------|
| `play` | `p` |
| `skip` | `s`, `next` |
| `volume` | `vol`, `v` |
| `pause` | - |
| `resume` | `unpause` |
| `stop` | - |
| `queue` | `q` |
| `nowplaying` | `np`, `current` |
| `loop` | `repeat` |
| `shuffle` | - |
| `join` | `j`, `connect` |
| `leave` | `disconnect`, `dc` |
| `favorite` | `fav`, `♥` |
| `favorites` | `favs`, `flist` |
| `playfavorite` | `playfav`, `pf` |
| `help` | `h`, `commands` |

---

## 10. Permisos del Bot

Para funcionamiento completo, el bot requiere:

### Permisos de Texto:
- ✅ Ver Canales
- ✅ Enviar Mensajes
- ✅ Insertar Enlaces
- ✅ Adjuntar Archivos
- ✅ Añadir Reacciones
- ✅ Usar Emojis Externos
- ✅ Leer Historial de Mensajes

### Permisos de Voz:
- ✅ Conectar
- ✅ Hablar
- ✅ Usar Actividad de Voz

---

## 11. Límites y Restricciones

| Límite | Valor |
|--------|-------|
| Cola máxima | 100 canciones |
| Duración máxima por canción | 2 horas |
| Favoritos por usuario | 50 canciones |
| Comandos por usuario | 1 cada 5 segundos |
| Búsquedas simultáneas | 1 por servidor |

---

## 12. Soporte

### Comandos no funcionan:
1. Verificar prefijo con `@BotName help`
2. Verificar permisos del bot
3. Reintentar en 30 segundos (cooldown)

### Problemas de reproducción:
1. Verificar que el bot tiene permisos de voz
2. Verificar que la URL es válida
3. Actualizar yt-dlp (admin del bot)

### Reportar Bugs:
- GitHub Issues
- Discord del bot (si disponible)
- Contactar al administrador del servidor

---

**¡Disfruta de tu música! 🎵**

Para más información, consulta los demás archivos .md del proyecto.
