# 🚀 NUEVAS FUNCIONALIDADES - Bot de Música con IA

## 🎯 Características Nuevas Implementadas

### 1. 🎵 **Sistema de Radio Inteligente**

El bot ahora puede reproducir música continua personalizada basada en tus gustos musicales.

#### Comando: `!radio`

```bash
!radio                    # Radio personalizada basada en tus gustos
!radio rock              # Radio de rock
!radio chill vibes       # Radio de música relajante
!radio hits 2010         # Radio de hits del 2010
!radio workout music     # Radio para hacer ejercicio
```

**¿Cómo funciona?**
- El bot analiza las canciones que te gustaron (likes)
- Evita automáticamente artistas/géneros que no te gustan (dislikes)
- Genera una cola de 20+ canciones personalizadas
- Aprende continuamente de tus preferencias

---

### 2. 👍👎 **Sistema de Likes y Dislikes**

Ahora puedes decirle al bot qué canciones te gustan y cuáles no.

#### Comandos:

**`!like` / `👍`**
- Dale "me gusta" a la canción actual
- El bot recordará que te gusta esta canción y el artista
- Influye en las recomendaciones futuras

**`!dislike` / `👎`**
- Dale "no me gusta" a la canción actual
- El bot evitará este artista en el futuro
- Si estás en modo Radio, saltará la canción automáticamente

**Ejemplo:**
```
Usuario: !play despacito
Bot: [reproduciendo Despacito]
Usuario: !like
Bot: 👍 Te gustó! El bot recordará que te gusta Luis Fonsi.

Usuario: !play never gonna give you up
Bot: [reproduciendo Never Gonna Give You Up]
Usuario: !dislike
Bot: 👎 El bot evitará reproducir canciones de Rick Astley.
```

---

### 3. 🧠 **Motor de Recomendaciones Inteligente**

El bot aprende de tus gustos y hace recomendaciones personalizadas.

#### Comando: `!recommend`

```bash
!recommend           # 5 recomendaciones personalizadas
!recommend 10        # 10 recomendaciones personalizadas
```

**¿Cómo aprende el bot?**

1. **Analiza tus likes**: Ve qué artistas y canciones te gustan
2. **Busca similares**: Encuentra canciones parecidas en YouTube
3. **Evita dislikes**: No recomienda artistas que rechazaste
4. **Patrones de skip**: Si siempre saltas reggaeton, aprende a evitarlo
5. **Exploración**: Ocasionalmente sugiere música nueva relacionada

---

### 4. 🎲 **Auto-Shuffle para Playlists**

Cuando añades una playlist, se mezcla automáticamente.

#### Comando: `!autoshuffle`

```bash
!autoshuffle         # Ver estado actual
!autoshuffle on      # Activar auto-shuffle
!autoshuffle off     # Desactivar auto-shuffle
```

**Comportamiento:**
- Por defecto: **ACTIVADO**
- Cuando añades una playlist de YouTube o Spotify, se mezcla automáticamente
- Las playlists nunca se reproducen en el mismo orden
- Puedes desactivarlo si prefieres el orden original

**Ejemplo:**
```
Usuario: !play https://open.spotify.com/playlist/xxxxx
Bot: ✅ 25 canciones añadidas a la cola (mezcladas aleatoriamente).

Usuario: !autoshuffle off
Bot: ✅ Auto-Shuffle Desactivado

Usuario: !play https://youtube.com/playlist?list=xxxxx
Bot: ✅ 30 canciones añadidas a la cola.
```

---

### 5. 📝 **Búsqueda Inteligente de Playlists**

Encuentra y reproduce playlists por género o tema.

#### Comando: `!findplaylist` / `!searchplaylist`

```bash
!findplaylist rock
!findplaylist hits 2010
!findplaylist chill vibes
!findplaylist workout music
!findplaylist sad songs
!findplaylist party music
!findplaylist spanish music
```

**¿Cómo funciona?**
1. Busca playlists en YouTube relacionadas con tu query
2. Muestra 3 opciones con reacciones (1️⃣ 2️⃣ 3️⃣)
3. Seleccionas la que quieres
4. Se añade toda la playlist a la cola (y se mezcla si auto-shuffle está activo)

---

### 6. 📊 **Ver tus Preferencias Musicales**

#### Comando: `!mypreferences` / `!mytaste`

```bash
!mypreferences
```

**Muestra:**
- Número de canciones con like
- Top 5 artistas favoritos
- Artistas que evitas
- Top canciones que te gustaron

**Ejemplo de salida:**
```
🎵 Preferencias Musicales de Usuario

👍 Canciones que te gustan: 15

⭐ Artistas Favoritos:
• The Weeknd
• Dua Lipa
• Calvin Harris
• Daft Punk
• Avicii

👎 Artistas Evitados:
• Justin Bieber
• Bad Bunny

🔝 Top Canciones:
• Blinding Lights - The Weeknd
• Levitating - Dua Lipa
• One More Time - Daft Punk
```

---

## 🎯 Casos de Uso Prácticos

### Caso 1: Descubrir Música Nueva

```
Usuario: !radio
Bot: 🎵 Generando cola personalizada...
Bot: ✅ Radio iniciada! 20 canciones en cola

[El bot reproduce canciones similares a las que te gustaron]

Usuario: !like        # En las que te gustan
Usuario: !dislike     # En las que no
```

### Caso 2: Fiesta Temática

```
Usuario: !findplaylist party music 2023
Bot: [Muestra 3 playlists]
Usuario: [Reacciona con 1️⃣]
Bot: ✅ 50 canciones añadidas (mezcladas aleatoriamente)

Usuario: !shuffle     # Mezclar aún más si quieres
Usuario: !loop queue  # Repetir toda la noche
```

### Caso 3: Sesión de Trabajo/Estudio

```
Usuario: !radio chill vibes
Bot: ✅ Radio de chill vibes iniciada

Usuario: !loop queue       # Para que no se acabe
Usuario: !volume 30        # Volumen bajo
```

### Caso 4: Entrenar tus Gustos

```
Usuario: !radio
[Reproduce varias canciones]

Usuario: !like    # En pop
Usuario: !like    # En electrónica
Usuario: !dislike # En reggaeton
Usuario: !dislike # En country

[El bot aprende: "Le gusta pop y electrónica, no reggaeton ni country"]

Usuario: !radio
[Ahora solo reproduce pop y electrónica]
```

---

## 📊 Base de Datos de Preferencias

El bot guarda automáticamente:
- ✅ Canciones con like/dislike
- ✅ Artistas favoritos (con puntuación)
- ✅ Artistas rechazados
- ✅ Historial de reproducción
- ✅ Patrones de skip

**Todo es por usuario y por servidor** - Tus gustos en un servidor no afectan a otros.

---

## 🚀 Lista Completa de Nuevos Comandos

### Radio y Recomendaciones

| Comando | Aliases | Descripción |
|---------|---------|-------------|
| `!radio [género]` | `autoplay`, `smartplay` | Iniciar radio inteligente |
| `!radiooff` | `stopradio` | Desactivar radio |
| `!like` | `👍`, `love` | Me gusta la canción actual |
| `!dislike` | `👎`, `hate` | No me gusta la canción actual |
| `!recommend [#]` | `reco`, `suggestions` | Obtener recomendaciones |
| `!mypreferences` | `myprefs`, `mytaste` | Ver tus preferencias |
| `!findplaylist <query>` | `searchplaylist`, `playlist` | Buscar playlists |

### Configuración

| Comando | Descripción |
|---------|-------------|
| `!autoshuffle [on/off]` | Activar/desactivar auto-shuffle |

---

## 🎨 Flujo de Usuario Mejorado

### Antes:
```
Usuario: !play canción
Usuario: !skip
Usuario: !play otra canción
Usuario: !skip
Usuario: !play otra más
```

### Ahora:
```
Usuario: !radio rock
[Bot reproduce 20 canciones de rock automáticamente]

Usuario: !like    # En las buenas
Usuario: !dislike # En las malas

[Bot aprende y mejora las próximas recomendaciones]
```

---

## 💡 Tips y Trucos

### 1. Entrena tu Radio
- Usa `!like` y `!dislike` en al menos 10 canciones
- Después usa `!radio` para música ultra-personalizada

### 2. Explora Géneros
- `!findplaylist <género>` es perfecto para descubrir nuevos estilos
- Prueba: rock, jazz, electronic, latin, k-pop, anime, lofi, etc.

### 3. Modo Fiesta
- `!radio party music` + `!loop queue` = fiesta infinita
- `!autoshuffle on` para máxima variedad

### 4. Ver Progreso
- `!mypreferences` te muestra cómo está aprendiendo el bot
- Cuantos más likes/dislikes, mejor las recomendaciones

---

## 🔧 Configuración Recomendada

```bash
# Para máxima inteligencia del bot:
!autoshuffle on        # Playlists siempre mezcladas

# Para sesiones de radio:
!radio                 # Iniciar con tus gustos
!loop queue           # Repetir cuando termine
!volume 60            # Volumen cómodo

# Dar feedback:
!like    # En canciones que te gusten
!dislike # En canciones que no
```

---

## 📈 Estadísticas del Sistema

El bot trackea:
- **Canciones reproducidas** por usuario
- **Skip rate** por artista (% de veces que saltas ese artista)
- **Géneros preferidos** inferidos de títulos
- **Patrones temporales** (qué escuchas cuándo)

Todo esto se usa para mejorar las recomendaciones.

---

## 🎯 Diferencias Clave vs Bot Normal

| Característica | Bot Normal | Este Bot |
|----------------|------------|----------|
| Reproducción | Manual | ✅ Automática con Radio |
| Personalización | ❌ Ninguna | ✅ Aprende tus gustos |
| Playlists | Orden fijo | ✅ Auto-mezcladas |
| Recomendaciones | ❌ No | ✅ Inteligentes |
| Feedback | ❌ No | ✅ Like/Dislike |
| Búsqueda | Solo por título | ✅ Por género/tema |

---

## 🎵 ¡Disfruta de tu Bot Musical Inteligente!

El bot ahora es mucho más que un simple reproductor - es tu **DJ personal** que aprende y se adapta a tus gustos musicales.

**¿Tienes ideas para más funcionalidades?** ¡El bot está diseñado para seguir mejorando!
