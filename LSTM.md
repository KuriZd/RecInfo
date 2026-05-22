# LSTM — Long Short-Term Memory en Procesamiento de Lenguaje Natural

**Zamudio Damián Oscar Kuricaveri — 22120729**  
**Recuperación de Información | ITM Morelia — 2026**

---

## 1. El problema del contexto en NLP

Los modelos como TF-IDF o Naive Bayes tratan cada palabra como independiente del resto. Esto pierde información fundamental: el significado de "banco" en "me senté en el banco del parque" es completamente diferente al de "deposité dinero en el banco". El contexto que rodea a una palabra determina su significado.

Las redes neuronales recurrentes (RNN) fueron diseñadas para procesar secuencias, manteniendo una memoria del pasado. Sin embargo, las RNN simples sufren del **problema del gradiente que desaparece**: en secuencias largas, la información del inicio de la secuencia se "olvida" antes de que el modelo pueda procesarla junto con el final.

---

## 2. Arquitectura LSTM

Las LSTM (Long Short-Term Memory), propuestas por Hochreiter y Schmidhuber en 1997, resuelven este problema mediante **compuertas** que controlan selectivamente qué información se recuerda y qué se olvida.

### Componentes principales

```
     ┌─────────────────────────────────────────────┐
     │              LSTM Cell                       │
     │                                              │
     │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐   │
     │  │Forget│  │Input │  │Gate  │  │Output│   │
     │  │Gate  │  │Gate  │  │(Cell)│  │Gate  │   │
     │  └──────┘  └──────┘  └──────┘  └──────┘   │
     │      ↑          ↑          ↑         ↑      │
     │  ───────────────────────────────────────    │
     │           x_t (entrada actual)              │
     │           h_{t-1} (estado oculto previo)    │
     └─────────────────────────────────────────────┘
```

### Las tres compuertas

| Compuerta | Función | Fórmula |
|---|---|---|
| **Forget gate** | Decide qué olvidar del estado anterior | `f_t = σ(W_f·[h_{t-1}, x_t] + b_f)` |
| **Input gate** | Decide qué nueva información almacenar | `i_t = σ(W_i·[h_{t-1}, x_t] + b_i)` |
| **Output gate** | Decide qué parte del estado devolver | `o_t = σ(W_o·[h_{t-1}, x_t] + b_o)` |

El **cell state** `C_t` fluye a través de toda la secuencia con modificaciones controladas, siendo el mecanismo de memoria a largo plazo.

---

## 3. LSTM para clasificación de texto

### Pipeline típico

```
Texto → Tokenización → Embeddings → LSTM → Dense → Softmax → Clase
```

### Ejemplo en Keras (arquitectura básica)

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

MAX_VOCAB = 10000
MAX_LEN = 100
EMBEDDING_DIM = 128

modelo = Sequential([
    Embedding(input_dim=MAX_VOCAB, output_dim=EMBEDDING_DIM,
              input_length=MAX_LEN),
    LSTM(units=64, return_sequences=False),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(3, activation='softmax')  # 3 clases: pos/neg/neutro
])

modelo.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

---

## 4. Embeddings: representación densa de palabras

Antes de ingresar texto a una LSTM, cada palabra se convierte en un vector denso de dimensión fija (embedding). Existen tres enfoques:

### 4.1 Embeddings aleatorios (desde cero)
El modelo aprende los embeddings durante el entrenamiento. Requiere mucho dato y computación.

### 4.2 Embeddings preentrenados
Vectores aprendidos sobre corpus masivos. Para español:
- **FastText (Facebook):** vectores de subpalabras, maneja palabras desconocidas.
- **Word2Vec en español (SBWCE):** entrenado sobre Wikipedia en español.
- **Spanish RoBERTa (PlanTL-GOB-ES):** modelo de lenguaje completo para tareas avanzadas.

### 4.3 Fine-tuning de BERT/RoBERTa
El enfoque más potente actualmente. Parte de un modelo preentrenado en millones de textos y se ajusta finamente sobre el corpus específico de la tarea.

---

## 5. Variantes de LSTM

| Variante | Descripción | Uso principal |
|---|---|---|
| **Bidirectional LSTM** | Procesa la secuencia en ambas direcciones | Clasificación, NER |
| **Stacked LSTM** | Múltiples capas LSTM apiladas | Tareas complejas |
| **LSTM + Attention** | Mecanismo de atención sobre las salidas | Traducción, resumen |
| **GRU** | Versión simplificada con menos parámetros | Corpus pequeños, velocidad |

---

## 6. LSTM vs. Transformers (BERT)

| Aspecto | LSTM | BERT/Transformer |
|---|:---:|:---:|
| Paralelización del entrenamiento | No | Sí |
| Manejo de dependencias largas | Limitado | Excelente |
| Requerimientos de datos | Moderados | Altos |
| Costo computacional | Medio | Alto |
| Rendimiento en benchmarks NLP (2026) | Bueno | Mejor |
| Interpretabilidad | Baja | Baja |

Las LSTM siguen siendo relevantes en dispositivos con recursos limitados, en tareas de tiempo real y en casos donde el corpus de entrenamiento es moderado. Para tareas académicas con corpus en español de tamaño medio, una LSTM bidireccional con embeddings FastText preentrenados ofrece un excelente balance.

---

## 7. Aplicaciones en recuperación de información

- **Análisis de sentimientos:** clasificar reseñas, comentarios o tweets.
- **Detección de spam:** identificar mensajes no deseados con contexto.
- **Extracción de entidades nombradas (NER):** identificar personas, lugares y organizaciones en texto.
- **Resumen automático:** generar versiones condensadas de documentos.
- **Traducción automática (seq2seq):** arquitectura encoder-decoder con LSTM.
- **Predicción de siguiente palabra:** base para sistemas de autocompletado.

---

## 8. Conclusión

Las LSTM representan un avance fundamental en el procesamiento de secuencias de texto porque resuelven el problema del olvido que limita a las RNN simples. Aunque los modelos Transformer han superado a las LSTM en la mayoría de benchmarks de NLP gracias a su capacidad de paralelización y atención global, las LSTM siguen siendo una opción válida y eficiente para muchas tareas de procesamiento de lenguaje natural, especialmente en contextos con recursos computacionales limitados o corpus de entrenamiento moderados.
