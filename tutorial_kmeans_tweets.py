"""
Tutorial paso a paso: K-Means aplicado a tweets simulados en español.
Ideal para entender el flujo completo de clustering de texto.

Pasos:
  1. Corpus de tweets simulados
  2. Limpieza de texto
  3. Vectorización TF-IDF
  4. Entrenamiento K-Means
  5. Asignación y análisis de clusters
  6. Evaluación con Silhouette Score
"""

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ─── PASO 1: Corpus de tweets simulados ───────────────────────────────────────
print("PASO 1 — Corpus de tweets simulados")
print("─" * 55)

TWEETS = [
    # Política
    "@usuario La corrupción sigue igual de mal que siempre, no cambia nada",
    "El gobierno promete infraestructura pero no cumple, #MexicoPolitica",
    "Las elecciones se acercan y los candidatos solo hacen promesas vacías",
    "La transparencia gubernamental debe mejorar urgentemente #Rendición",
    "Nuevo escándalo de corrupción en dependencia federal, qué vergüenza",
    "El congreso aprueba reforma sin consultar a la ciudadanía #Democracia",
    # Entretenimiento
    "¡La nueva temporada de la serie está increíble! No puedo parar de verla",
    "El concierto de anoche fue lo mejor que he visto en años 🎶 #Música",
    "Esa película ganó el Oscar y es absolutamente merecido, obra maestra",
    "El nuevo álbum del artista rompió récords de streaming en México",
    "El festival de cine tiene películas increíbles este año #Cine2026",
    "La obra de teatro en el Palacio de Bellas Artes fue espectacular",
    # Tecnología
    "Probé el nuevo smartphone y la cámara es una locura, fotos increíbles",
    "La actualización de la app mejoró el rendimiento notablemente #Tech",
    "Lanzaron un modelo de IA que corre en el teléfono sin internet 🤯",
    "El coche eléctrico ya tiene autonomía para cruzar todo México",
    "Las gafas de realidad aumentada ya se venden en México #AR",
    "La nueva versión del sistema operativo es más rápida y segura",
    # Deportes
    "¡Golazo del Tri en el último minuto! Clasificamos al mundial 🇲🇽⚽",
    "Checo Pérez en el podio otra vez, orgullo mexicano en la F1 🏁",
    "El partido de hoy fue aburridísimo, sin goles y sin emociones",
    "La liga mexicana necesita más inversión para competir en Latinoamérica",
    "Gran actuación del boxeador tapatío, nuevo campeón del mundo 🥊",
    "Los Pumas ganan el clásico universitario con tres goles de diferencia",
]

for i, t in enumerate(TWEETS[:5], 1):
    print(f"  [{i}] {t}")
print(f"  ... ({len(TWEETS)} tweets en total)\n")

# ─── PASO 2: Limpieza de texto ─────────────────────────────────────────────────
print("PASO 2 — Limpieza de texto")
print("─" * 55)

STOPWORDS_ES = {
    "el", "la", "los", "las", "un", "una", "de", "en", "con", "a",
    "al", "del", "se", "que", "por", "para", "y", "o", "es", "su",
    "sus", "le", "lo", "les", "como", "más", "pero", "si", "no",
    "ya", "fue", "son", "ser", "tiene", "hay", "también", "sin",
}


def limpiar_tweet(texto: str) -> str:
    texto = re.sub(r'@\w+', '', texto)        # eliminar menciones
    texto = re.sub(r'#\w+', '', texto)         # eliminar hashtags
    texto = re.sub(r'https?://\S+', '', texto) # eliminar URLs
    texto = re.sub(r'[^\w\s]', ' ', texto)     # eliminar puntuación
    texto = texto.lower()
    tokens = [t for t in texto.split() if t not in STOPWORDS_ES and len(t) > 2]
    return " ".join(tokens)


tweets_limpios = [limpiar_tweet(t) for t in TWEETS]
print(f"  Original : {TWEETS[0]}")
print(f"  Limpio   : {tweets_limpios[0]}\n")

# ─── PASO 3: Vectorización TF-IDF ─────────────────────────────────────────────
print("PASO 3 — Vectorización TF-IDF")
print("─" * 55)

vectorizer = TfidfVectorizer(max_features=100, min_df=1)
X = vectorizer.fit_transform(tweets_limpios)
features = vectorizer.get_feature_names_out()
print(f"  Dimensión de la matriz: {X.shape}  ({X.shape[0]} tweets × {X.shape[1]} términos)\n")

# ─── PASO 4: Entrenamiento K-Means ────────────────────────────────────────────
print("PASO 4 — Entrenamiento K-Means (K=4)")
print("─" * 55)

K = 4
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10, max_iter=300)
kmeans.fit(X)
etiquetas = kmeans.labels_
print(f"  Iteraciones hasta convergencia: {kmeans.n_iter_}")
print(f"  Inercia final (suma de distancias²): {kmeans.inertia_:.2f}\n")

# ─── PASO 5: Análisis de clusters ─────────────────────────────────────────────
print("PASO 5 — Clusters y palabras representativas")
print("─" * 55)

centroids = kmeans.cluster_centers_
for cid in range(K):
    top_idx = centroids[cid].argsort()[::-1][:6]
    top_words = [features[i] for i in top_idx]
    docs = [TWEETS[i] for i, e in enumerate(etiquetas) if e == cid]
    print(f"\n  Cluster {cid} ({len(docs)} tweets)")
    print(f"  Palabras clave: {', '.join(top_words)}")
    for d in docs[:3]:
        print(f"    • {d[:70]}")

# ─── PASO 6: Evaluación ───────────────────────────────────────────────────────
print("\n" + "─" * 55)
print("PASO 6 — Evaluación con Silhouette Score")
print("─" * 55)

sil = silhouette_score(X, etiquetas)
print(f"  Silhouette Score (K={K}): {sil:.4f}")
print("""
  Interpretación:
    > 0.7  → Clusters muy bien separados
    0.5-0.7 → Clusters razonablemente buenos
    0.25-0.5 → Clusters débiles, puede haber solapamiento
    < 0.25 → Sin estructura clara
""")
