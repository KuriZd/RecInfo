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

- 📁 Actividades de Investigación
  - 📄 [Actividad 1.1 — Estrategias de búsqueda de información](./Actividad1.1.md)
  - 📄 [Actividad 1.2 — Evaluación de credibilidad de fuentes](./Actividad1.2.md)
  - 📄 [Actividad 1.3 — Feeds RSS y vigilancia tecnológica](./Actividad1.3.md)
  - 📄 [Actividad 1.4 — Metadatos, indexación y organización](./Actividad1.4.md)
  - 📄 [Actividad 1.5 — Sesgos algorítmicos en buscadores](./Actividad1.5.md)
  - 📄 [Actividades 2 — Salud mental y tecnología en jóvenes (multi-fuente)](./Actividades2.md)
  - 📄 [Actividades 3 — Análisis crítico de medios y algoritmos](./Actividades3.md)

- 📁 NLP — Procesamiento de Lenguaje Natural
  - `NLTK.py` — Tokenización, stopwords, stemming y frecuencia de términos en español
  - `NLTK_Activity.py` — Análisis comparativo de corpus con y sin preprocesamiento NLTK
  - `TF-IDF.py` — Vectorización manual y con sklearn, matriz TF-IDF y documento más representativo por término
  - `similitud_coseno.py` — Similitud coseno básica sin filtrado de stopwords
  - `similitud_coseno_stop.py` — Similitud coseno con eliminación de stopwords (comparación de impacto)
  - `similitud_coseno_nltk.py` — Pipeline completo NLTK → TF-IDF → coseno con búsqueda por consulta

- 📁 K-Means Clustering
  - `K_means_cluster.py` — K-Means sobre noticias simuladas con análisis de centroides y Silhouette Score
  - `tutorial_kmeans_tweets.py` — Tutorial paso a paso aplicado a tweets simulados (6 pasos documentados)
  - 📄 [Reporte K-Means](./Reporte_kmeans.md)

- 📁 Clasificación y Sentimientos
  - `clasificacion_comentarios.py` — Clasificador de sentimiento basado en léxico, exporta CSV
  - `clasificacion_comentarios2.0.py` — V2: puntuación ponderada, negaciones e intensificadores
  - `extraccion_comentarios.py` — Lee CSV, detecta sentimiento y sarcasmo, exporta reporte

- 📁 Datasets
  - `100comentarios.csv` — 100 comentarios simulados etiquetados (Positivo/Negativo/Neutro)
  - `dataset_redes_sociales_200.csv` — 200 publicaciones de redes sociales con usuario, plataforma y likes
  - `clasificacion_sarcasmo_200.csv` — 200 textos con etiqueta binaria de sarcasmo
  - `sentimientos_resultados.csv` — Resultados de clasificación con score de confianza
  - `sentimientos_resultados_100.csv` — Resultados de 100 comentarios clasificados

- 📁 Notebooks
  - `covid-19.ipynb` — EDA de datos COVID-19 simulados: curva epidémica, distribución por edad y estado
  - `diabetes.ipynb` — EDA + clasificador logístico para diagnóstico de diabetes con datos simulados

- 📁 Documentos Teóricos
  - 📄 [Algoritmos Supervisados](./Algoritmos_supervisados.md) — Naive Bayes, SVM, Regresión Logística, Random Forest
  - 📄 [LSTM — Redes de Memoria a Largo Plazo](./LSTM.md)
  - 📄 [Ventana de Overton](./Overton.md) — Marco analítico aplicado a narrativas digitales
  - 📄 [Programas de Gobierno y Digitalización](./Programas_Gob.md)
  - 📄 [Conceptos de Recuperación de Información](./Informacion_Recu.txt)

- 📁 Textos base
  - `textos/doc1.txt` — IA y recuperación de información (texto de referencia para NLP)
  - `textos/doc2.txt` — Minería de texto y análisis de sentimientos en redes sociales

## Proyectos Finales

| Proyecto | Repositorio |
|---|---|
| SIMANW | [github.com/KuriZd/SIMANW](https://github.com/KuriZd/SIMANW) |
| XFiles | [github.com/KuriZd/X-Files](https://github.com/KuriZd/X-Files) |

