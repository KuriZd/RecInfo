<p align="center">
  <strong>DEPARTAMENTO DE SISTEMAS Y COMPUTACIÓN</strong>
</p>

<p align="center">
  <img src="assets/itm.png" alt="ITM - Departamento de Sistemas y Computación" width="220" />
</p>

<br/>

<p align="center">
  <strong>APLICACIONES MÓVILES</strong>
</p>

<p align="center">
  <strong>TEMA</strong><br/>
  <strong>BÚSQUEDA DE INFORMACIÓN EN <u>FEEDS RSS</u></strong>
</p>

<br/>

<p align="center">
  <strong><u>PRESENTADO POR</u></strong>
</p>

<p align="center">
  <strong>ZAMUDIO DAMIÁN OSCAR KURICAVERI: 22120729</strong>
</p>

<br/>

<p align="center">
  <strong><u>ASESOR DE CONTENIDO</u></strong><br/>
  <strong>JESÚS EDUARDO ALCARAZ CHÁVEZ</strong>
</p>

<br/>

<p align="center">
  <strong>MORELIA MICHOACÁN</strong>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <strong>FEBRERO 2026</strong>
</p>

## Índice (Árbol de links)

- 📁 Contenido
  - 🔎 [Hacks de búsqueda avanzados](./docs/hacks_de_busqueda_avanzados.md)
  - 🌐 [APIs por ejes temáticos](./docs/API_RS.md)
  - 🕵️ [Investigación: narrativas de control digital](./docs/investigacion_control_digital.md)

- 📁 RSS Scraper
  - `main.py` — Orquestador principal: inicializa DB, lanza el scraper, exporta CSV y permite búsqueda FTS
  - `scraper.py` — Descarga y parsea feeds RSS con `feedparser`; retorna lista de items normalizados
  - `db.py` — Esquema SQLite (feeds / items / runs), upsert y búsqueda FTS5 con triggers de sincronización
  - `ScrapingT1.py` — Versión inicial del scraper (DB plana, sin tabla de runs ni FTS)
  - `rss_items.csv` — Exportación CSV del último scraping
  - **Feeds configurados:** BBC World · CNN Top · TechCrunch · CNBC Business · ESPN News

- 📁 Análisis de Noticias
  - `EDA.py` — Búsqueda dual (NewsAPI + GNews) sobre "El Mencho"; calcula nivel de riesgo por clickbait, mayúsculas y fuente verificada; exporta `analisis_mencho_2026.json`

- 📁 Visión por Computadora
  - `PixelCount.py` — Cuenta píxeles verdes (HSV) en `assets/frutas.png` y muestra porcentaje
  - `P2Count.py` — Analiza porcentaje de rojo, verde y azul en un lote de imágenes (HSV)

- 📁 Expediente X (Esteganografía y color)
  - `Expediente X/Mision1.py` — Extracción LSB en escala de grises (`evidencia_1.png`)
  - `Expediente X/Mision2.py` — Recuperación de mensaje por rango de matiz HSV (`evidencia_2.png`)
  - `Expediente X/Mision3.py` — Reto híbrido: máscara HSV amarillo pardo + LSB canal V (`evidencia_3.png`)
  - 📄 [Reporte de misiones](./Expediente%20X/reporte_mision.md)

- 📁 Reducción de Dimensión
  - 📄 [Tabla de palabras principales por documento](./Reduccion_dimension.md)

## Proyectos Finales

| Proyecto | Repositorio |
|---|---|
| SIMANW | [github.com/KuriZd/SIMANW](https://github.com/KuriZd/SIMANW) |

