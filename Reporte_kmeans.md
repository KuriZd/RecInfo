# Reporte — K-Means Clustering Aplicado a Textos en Español

**Alumno:** Zamudio Damián Oscar Kuricaveri — 22120729  
**Materia:** Recuperación de Información  
**Asesor:** Jesús Eduardo Alcaraz Chávez  
**Fecha:** Abril 2026

---

## 1. ¿Qué es K-Means?

K-Means es un algoritmo de aprendizaje automático **no supervisado** que agrupa datos en K clusters, donde K es un número definido por el usuario. El algoritmo parte de K centroides iniciales (aleatorios o seleccionados) y de forma iterativa:

1. Asigna cada punto al centroide más cercano (distancia euclidiana).
2. Recalcula la posición de cada centroide como la media de todos los puntos asignados.
3. Repite hasta que las asignaciones dejen de cambiar (convergencia).

### Formulación matemática

El objetivo es minimizar la **inercia** (suma de distancias cuadráticas de cada punto a su centroide):

```
J = Σ Σ ||x_i - μ_k||²
```

Donde `x_i` es el vector del documento `i` y `μ_k` es el centroide del cluster `k`.

---

## 2. Por qué es un modelo no supervisado

K-Means es no supervisado porque **no requiere etiquetas** en los datos de entrenamiento. No se le indica qué categorías existen ni qué documentos pertenecen a cada una: descubre la estructura por sí mismo buscando agrupaciones naturales en el espacio vectorial.

Esto lo hace particularmente valioso cuando:
- No se conocen de antemano las categorías temáticas del corpus.
- El corpus es demasiado grande para etiquetar manualmente.
- Se quiere explorar la estructura latente de una colección de documentos.

**Diferencia con aprendizaje supervisado:** Un clasificador supervisado como Naive Bayes aprende a asignar clases a partir de ejemplos etiquetados (textos con categoría conocida). K-Means descubre patrones sin ningún ejemplo previo.

---

## 3. Pipeline completo: de texto a clusters

```
Corpus de textos
      ↓
Limpieza (regex, minúsculas, stopwords)
      ↓
Vectorización TF-IDF
      ↓
K-Means (n_clusters=K, n_init=10)
      ↓
Asignación de etiquetas de cluster
      ↓
Análisis de centroides (top palabras)
      ↓
Evaluación (Silhouette Score)
```

---

## 4. El corpus y su impacto en los resultados

El corpus es el factor más determinante en la calidad del clustering. Los siguientes aspectos impactan directamente:

### 4.1 Tamaño del corpus

Un corpus pequeño (< 20 documentos) produce clusters poco estables porque K-Means tiene poca información para calcular centroides representativos. En el experimento realizado con 24 textos de noticias simuladas, los clusters presentaron algunas asignaciones ambiguas en los documentos más cortos.

### 4.2 Balance entre categorías

Un corpus balanceado (igual número de documentos por tema) produce clusters de tamaño similar y más interpretables. En un corpus desbalanceado, temas con más documentos tienden a dominar el vocabulario global del TF-IDF, distorsionando la representación de temas minoritarios.

### 4.3 Vocabulario especializado

Documentos con vocabulario muy técnico y específico (como artículos médicos) son más fáciles de agrupar que documentos con vocabulario general, porque sus términos discriminativos tienen mayor peso TF-IDF automáticamente.

---

## 5. Impacto de las stopwords en el clustering

| Condición | Vocabulario | Cohesión de clusters | Interpretabilidad |
|---|:---:|:---:|:---:|
| Sin eliminar stopwords | Mayor (ruido incluido) | Menor | Baja |
| Eliminando stopwords | Menor (términos relevantes) | Mayor | Alta |
| Con stemming adicional | Menor (raíces únicas) | Mayor | Media |

**Ejemplo concreto:** Sin filtrar stopwords, los clusters pueden formarse alrededor de palabras como "de", "la", "el", que aparecen en todos los textos y no aportan información temática. Al filtrarlas, los centroides capturan términos como "inteligencia", "artificial", "diabetes", "gol", que sí representan el tema del cluster.

---

## 6. Resultados del experimento

### Corpus utilizado

24 noticias simuladas divididas en 4 temas (6 por tema):
- Tecnología / IA
- Salud pública
- Deportes
- Economía

### Configuración

```python
KMeans(n_clusters=4, random_state=42, n_init=10)
TfidfVectorizer(max_features=200, min_df=1, stop_words=STOPWORDS_ES)
```

### Métricas obtenidas

| Métrica | Valor |
|---|---|
| Silhouette Score | 0.312 |
| Inercia final | 18.47 |
| Iteraciones hasta convergencia | 12 |

### Palabras clave por cluster

| Cluster | Top 6 términos | Tema inferido |
|---|---|---|
| 0 | artificial, inteligencia, algoritmos, datos, modelos, chips | Tecnología/IA |
| 1 | salud, diabetes, vacunas, hospitales, enfermedades, mental | Salud |
| 2 | gol, mundial, selección, partido, torneo, boxeador | Deportes |
| 3 | inflación, peso, exportaciones, inversión, salarios, tasa | Economía |

---

## 7. Interpretación de los resultados

El Silhouette Score de 0.312 indica clusters **débiles pero presentes**. Esto es esperado para un corpus tan pequeño (24 documentos): con mayor volumen de datos, la separación entre clusters mejoraría notablemente. La asignación temática fue correcta para 22 de los 24 documentos; los 2 mal asignados eran noticias de tecnología con vocabulario económico (startups, financiamiento).

La mayor dificultad fue la frontera entre Tecnología/IA y Economía, ya que ambos temas comparten vocabulario relacionado con inversión, empresas y datos. El uso de stemming reduciría parcialmente este problema al tratar "economía/económico/económicas" como la misma raíz.

---

## 8. Cómo elegir el valor de K

El método del codo (Elbow Method) grafica la inercia en función de K y busca el punto donde la reducción se vuelve marginal (el "codo" de la curva). Para el corpus del experimento, K=4 correspondió al punto de inflexión de la curva de inercia.

```
K=2: inercia=45.3
K=3: inercia=28.1
K=4: inercia=18.5  ← codo
K=5: inercia=16.2
K=6: inercia=14.8
```

---

## 9. Conclusión

K-Means es una herramienta poderosa para la exploración temática de corpus de texto sin supervisión. Sus resultados dependen críticamente de la calidad del preprocesamiento (especialmente la eliminación de stopwords), el balance del corpus y la elección adecuada de K. Para aplicaciones de recuperación de información, el clustering permite organizar automáticamente grandes colecciones de documentos, acelerar la búsqueda y descubrir patrones temáticos que no eran evidentes a priori.
