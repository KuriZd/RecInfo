# Algoritmos Supervisados en Recuperación de Información y NLP

**Zamudio Damián Oscar Kuricaveri — 22120729**  
**Recuperación de Información | ITM Morelia — 2026**

---

## 1. Aprendizaje supervisado: concepto central

En el aprendizaje supervisado, el modelo aprende a partir de un conjunto de datos de entrenamiento donde cada ejemplo incluye:
- **Entrada (X):** las características del dato (e.g., vector TF-IDF de un texto).
- **Salida esperada (y):** la etiqueta o valor correcto (e.g., "Positivo", "Negativo").

El objetivo es aprender una función `f(X) → y` que generalice bien sobre datos nuevos no vistos durante el entrenamiento. La calidad del modelo se mide comparando sus predicciones contra las etiquetas reales en un conjunto de prueba separado.

---

## 2. Naive Bayes

### Fundamento teórico

Naive Bayes aplica el teorema de Bayes asumiendo independencia condicional entre características. Para clasificación de texto:

```
P(clase | documento) ∝ P(clase) × ∏ P(término_i | clase)
```

A pesar de la suposición "naïve" (que raramente se cumple en texto real), el clasificador es sorprendentemente efectivo en muchas tareas NLP por su eficiencia computacional y robustez ante corpus pequeños.

### Variantes principales

- **Multinomial NB:** ideal para texto con conteos de palabras (TF).
- **Bernoulli NB:** adecuado para representaciones binarias (presencia/ausencia de término).
- **Gaussian NB:** para características continuas (no recomendado para texto).

### Aplicación en análisis de sentimientos

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(corpus_entrenamiento)
modelo = MultinomialNB()
modelo.fit(X_train, etiquetas)
```

### Ventajas y limitaciones

| Ventajas | Limitaciones |
|---|---|
| Muy rápido de entrenar | Asume independencia entre palabras |
| Funciona bien con corpus pequeños | No captura contexto ni orden de palabras |
| Interpretable | Sensible al desbalance de clases |

---

## 3. Regresión Logística

### Fundamento teórico

A pesar del nombre, es un clasificador binario (y multiclase con softmax) que aprende una frontera de decisión lineal en el espacio de características. Utiliza la función sigmoide para producir probabilidades:

```
P(y=1 | X) = 1 / (1 + e^(-w·X))
```

La función de pérdida es la entropía cruzada (cross-entropy), optimizada con gradiente descendente.

### Fortalezas en NLP

- Produce probabilidades bien calibradas.
- Permite inspeccionar los pesos aprendidos para interpretar qué términos son más predictivos de cada clase.
- Regularización L1 produce modelos dispersos (selección implícita de características).

---

## 4. Máquinas de Soporte Vectorial (SVM)

### Fundamento teórico

SVM busca el hiperplano con máximo margen de separación entre clases. Los vectores de soporte son los ejemplos más cercanos al hiperplano y son los únicos que determinan la frontera de decisión.

El kernel RBF (Radial Basis Function) permite separar clases no linealmente separables al proyectar los datos a un espacio de mayor dimensionalidad implícitamente.

### Aplicación en clasificación de texto

SVM lineal (LinearSVC) es frecuentemente el baseline más fuerte para clasificación de texto con TF-IDF, superando a redes neuronales en corpus pequeños o medianos.

---

## 5. Árboles de Decisión y Random Forest

### Árbol de Decisión

Genera una secuencia de preguntas binarias sobre las características del dato hasta asignar una clase. El criterio de división más común es la **impureza de Gini** o la **ganancia de información** (entropía).

### Random Forest

Ensemble de múltiples árboles de decisión entrenados sobre subconjuntos aleatorios del corpus y las características. La predicción final es la votación mayoritaria. Reduce el sobreajuste característico de los árboles individuales.

**Ventaja para NLP:** Maneja bien características de alta dimensionalidad (vocabularios grandes) sin requerir normalización.

---

## 6. Comparación de algoritmos para clasificación de texto

| Algoritmo | Velocidad entrenamiento | Interpretabilidad | Rendimiento tipico F1 | Corpus ideal |
|---|:---:|:---:|:---:|---|
| Naive Bayes | Muy alta | Alta | 0.75-0.85 | Pequeño, categorías claras |
| Regresión Logística | Alta | Media | 0.80-0.88 | Mediano, binario/multiclase |
| SVM Lineal | Media | Baja | 0.82-0.90 | Mediano-grande |
| Random Forest | Baja | Media | 0.78-0.87 | Mediano, características mixtas |
| Red Neuronal (LSTM) | Muy baja | Muy baja | 0.85-0.93 | Grande, contexto importante |

---

## 7. Evaluación de clasificadores

### Métricas fundamentales

**Matriz de confusión:**
```
                Predicho +    Predicho -
Real +      │  TP (Verdadero Pos) │  FN (Falso Neg)  │
Real -      │  FP (Falso Pos)     │  TN (Verdadero Neg)│
```

**Precisión:** TP / (TP + FP) — de lo que predigo positivo, ¿cuánto lo es realmente?  
**Recall:** TP / (TP + FN) — de lo que realmente es positivo, ¿cuánto detecto?  
**F1-Score:** 2 × (Precisión × Recall) / (Precisión + Recall) — media armónica de ambas.

### Validación cruzada (Cross-Validation)

Para corpus pequeños, la validación cruzada k-fold permite obtener una estimación más robusta del rendimiento real del modelo:

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(modelo, X, y, cv=5, scoring='f1_weighted')
print(f"F1 promedio: {scores.mean():.3f} ± {scores.std():.3f}")
```

---

## 8. Aplicaciones en recuperación de información

| Tarea | Algoritmo recomendado | Descripción |
|---|---|---|
| Clasificación de spam | Naive Bayes | Rápido y preciso para vocabulario simple |
| Análisis de sentimientos | Regresión Logística | Buena calibración de probabilidades |
| Categorización de noticias | SVM Lineal | Excelente en alta dimensionalidad |
| Detección de fake news | Random Forest | Maneja características mixtas (texto+metadatos) |
| Clasificación de idioma | Naive Bayes Multinomial | Eficiente con n-gramas de caracteres |

---

## 9. Conclusión

Los algoritmos supervisados son herramientas esenciales del arsenal de recuperación de información moderno. La elección del algoritmo correcto depende del tamaño del corpus, la disponibilidad de datos etiquetados, el balance entre interpretabilidad y rendimiento, y los recursos computacionales disponibles. Para la mayoría de tareas académicas con corpus de tamaño moderado y en español, la combinación de TF-IDF con SVM lineal o Regresión Logística ofrece resultados robustos sin requerir infraestructura de deep learning.
