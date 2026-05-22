# Actividad 1.5 — Sesgos Algorítmicos en los Motores de Búsqueda

**Alumno:** Zamudio Damián Oscar Kuricaveri — 22120729  
**Materia:** Recuperación de Información  
**Asesor:** Jesús Eduardo Alcaraz Chávez  
**Fecha:** Marzo 2026

---

## Objetivo

Investigar y documentar los principales tipos de sesgo que introducen los algoritmos de los motores de búsqueda, comprender sus causas estructurales y reflexionar sobre las implicaciones éticas para la sociedad de la información.

---

## 1. ¿Qué es el sesgo algorítmico en búsqueda?

Un motor de búsqueda no recupera información de forma neutral: sus algoritmos aplican criterios de ranking que reflejan decisiones de diseño, objetivos comerciales y los patrones estadísticos presentes en los datos de entrenamiento. Cuando estos criterios favorecen sistemáticamente ciertos tipos de contenido, fuentes o perspectivas sobre otros, se produce un sesgo algorítmico.

Lo que aparece en la primera página de resultados no es necesariamente lo más verdadero ni lo más relevante: es lo que el algoritmo considera más probable que sea seleccionado por el usuario promedio que realizó esa consulta.

---

## 2. Tipos de sesgo identificados

### 2.1 Sesgo de popularidad

Los algoritmos de PageRank y sus derivados asignan mayor autoridad a páginas con más backlinks entrantes. Esto privilegia a fuentes con más recursos para generar o comprar enlaces, no necesariamente a las más precisas o actualizadas.

**Impacto:** Fuentes pequeñas, especializadas o de habla no inglesa quedan sistemáticamente relegadas en el ranking.

---

### 2.2 Sesgo de personalización

Los motores de búsqueda adaptan los resultados según el historial, la ubicación y el perfil inferido de cada usuario. Esto crea lo que Eli Pariser denominó la "burbuja de filtro": el usuario recibe información que confirma sus creencias previas, limitando la exposición a perspectivas alternativas.

**Experimento realizado:** Al buscar "reforma energética México" desde dos cuentas con perfiles distintos (una con historial de medios de izquierda y otra con medios de derecha), los primeros cinco resultados fueron completamente diferentes en ambos casos.

---

### 2.3 Sesgo de idioma y geografía

La mayor parte del índice web en inglés es notablemente más grande que en español. Un evento de relevancia regional en México puede recibir cobertura académica en repositorios locales que Google no indexa o pondera con menor peso que publicaciones anglófonas sobre el mismo tema.

**Impacto:** Investigadores en América Latina pueden subestimar el conocimiento producido en su contexto geográfico por su menor visibilidad en los buscadores principales.

---

### 2.4 Sesgo de selección temporal

Los algoritmos tienden a privilegiar contenido reciente, interpretando la fecha de publicación como señal de relevancia. Esto puede hacer que artículos clásicos o fundamentales queden sepultados por contenido nuevo pero superficial.

---

### 2.5 Sesgo de género y representación

Estudios sobre imágenes de búsqueda han documentado que términos profesionales como "CEO", "doctor" o "ingeniero" devuelven predominantemente imágenes de personas masculinas, reproduciendo estereotipos presentes en los datos de entrenamiento.

---

## 3. Comparación de resultados entre motores de búsqueda

Se realizó la siguiente búsqueda en tres motores diferentes, sin sesión iniciada y con VPN neutral:

**Consulta:** `"vigilancia digital" derechos humanos México`

| Motor | Tipo de fuente predominante | Perspectiva observada |
|---|---|---|
| Google | Medios digitales populares, opinión | Balanceada, comercialmente orientada |
| DuckDuckGo | ONG, medios alternativos | Mayor diversidad de perspectivas |
| Bing | Noticias de agencias internacionales | Énfasis en cobertura anglosajona |

**Observación:** DuckDuckGo mostró más resultados de organizaciones de derechos digitales como Electronic Frontier Foundation y Article 19, fuentes que no aparecieron en la primera página de Google para la misma consulta.

---

## 4. Estrategias para mitigar el sesgo en la búsqueda académica

| Estrategia | Descripción |
|---|---|
| Usar múltiples motores | Comparar resultados de Google Scholar, Semantic Scholar, BASE |
| Búsqueda en repositorios locales | Revisar RENATI (México), CLACSO, Latindex |
| Desactivar personalización | Usar modo incógnito o sesión sin cuenta |
| Operadores avanzados | `site:`, `filetype:`, `after:` para mayor control |
| Búsqueda inversa | Partir de un artículo conocido y rastrear sus citas |
| Cambiar idioma de búsqueda | Realizar la misma consulta en inglés y comparar |

---

## 5. Reflexión ética

El sesgo algorítmico en los motores de búsqueda tiene consecuencias que van más allá de la incomodidad académica. En contextos de salud pública, los algoritmos que privilegian información antivacunas por su mayor engagement han contribuido a crisis sanitarias documentadas. En procesos electorales, la personalización de resultados puede influir en la formación de opinión política sin que el usuario lo perciba conscientemente.

La alfabetización algorítmica, es decir, la capacidad de entender cómo funciona y qué limita un motor de búsqueda, es hoy una competencia ciudadana fundamental tan importante como la lectura crítica de medios tradicionales.

---

## 6. Conclusión

Los motores de búsqueda son intermediarios de la información, no ventanas neutrales al conocimiento. Sus algoritmos están diseñados para maximizar el engagement del usuario dentro de un modelo de negocio basado en publicidad, no para garantizar la recuperación más precisa o diversa. Reconocer este hecho y desarrollar estrategias de búsqueda que compensen activamente los sesgos identificados es una habilidad esencial para cualquier investigador o profesional de la información en el siglo XXI.
