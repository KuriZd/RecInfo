"""
K-Means Clustering sobre corpus de textos cortos (noticias simuladas)
Pipeline: limpieza → TF-IDF → K-Means → análisis de clusters
"""

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import Counter

CORPUS = [
    # Tecnología / IA
    "La inteligencia artificial mejora los diagnósticos médicos con algoritmos",
    "Los modelos de lenguaje como GPT generan texto natural y coherente",
    "El machine learning detecta fraudes bancarios en tiempo real",
    "Las redes neuronales procesan imágenes médicas con alta precisión",
    "La automatización con IA reduce costos operativos en manufactura",
    "Los chips de IA aceleran el entrenamiento de modelos profundos",
    # Salud
    "La diabetes tipo dos afecta a millones de personas en México",
    "Las vacunas contra el COVID protegen a poblaciones vulnerables",
    "El sedentarismo y la mala alimentación causan enfermedades crónicas",
    "Los hospitales públicos enfrentan escasez de medicamentos esenciales",
    "La salud mental es una prioridad en la agenda de bienestar juvenil",
    "La hipertensión arterial incrementa el riesgo cardiovascular en adultos",
    # Deportes
    "El América gana el clásico capitalino ante Cruz Azul en el Azteca",
    "Checo Pérez termina en el podio del Gran Premio de México",
    "La selección mexicana clasifica al mundial tras superar a Honduras",
    "El boxeador tapatío conquista el campeonato mundial superwélter",
    "El Guadalajara vence al Monterrey en la final del torneo apertura",
    "Los Juegos Olímpicos de Los Ángeles 2028 ya tienen sede confirmada",
    # Economía
    "La inflación en México sube al cuatro punto dos por ciento en marzo",
    "El peso mexicano se deprecia frente al dólar por tensiones globales",
    "Las exportaciones automotrices crecen gracias al T-MEC",
    "La inversión extranjera directa aumenta en el sector manufacturero",
    "Los salarios mínimos suben un veinte por ciento según decreto oficial",
    "El banco central sube la tasa de interés para contener la inflación",
]

K = 4
STOPWORDS_ES = [
    "el", "la", "los", "las", "un", "una", "de", "en", "con", "a", "al",
    "del", "se", "que", "por", "para", "y", "o", "es", "su", "sus",
    "le", "lo", "les", "como", "más", "pero", "si", "no", "ya",
    "este", "esta", "estos", "son", "fue", "ser", "tiene", "hay",
]

TEMAS = {0: "Tecnología/IA", 1: "Salud", 2: "Deportes", 3: "Economía"}


def limpiar(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúüñ\s]', ' ', texto)
    tokens = texto.split()
    tokens = [t for t in tokens if t not in STOPWORDS_ES and len(t) > 2]
    return " ".join(tokens)


corpus_limpio = [limpiar(doc) for doc in CORPUS]

vectorizer = TfidfVectorizer(max_features=200, min_df=1)
X = vectorizer.fit_transform(corpus_limpio)

kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
etiquetas = kmeans.fit_predict(X)

sil_score = silhouette_score(X, etiquetas)

print("=" * 65)
print(f"K-MEANS CLUSTERING  (K={K})")
print("=" * 65)
print(f"\n  Silhouette Score: {sil_score:.4f}  (rango: -1 a 1, mayor=mejor)")

features = vectorizer.get_feature_names_out()
centroids = kmeans.cluster_centers_

print("\n" + "=" * 65)
print("PALABRAS CLAVE POR CLUSTER")
print("=" * 65)
for cluster_id in range(K):
    top_idx = centroids[cluster_id].argsort()[::-1][:8]
    top_words = [features[i] for i in top_idx]
    print(f"\n  Cluster {cluster_id}: {', '.join(top_words)}")

print("\n" + "=" * 65)
print("DOCUMENTOS POR CLUSTER")
print("=" * 65)
for cluster_id in range(K):
    miembros = [CORPUS[i] for i, e in enumerate(etiquetas) if e == cluster_id]
    print(f"\n  ── Cluster {cluster_id} ({len(miembros)} documentos) ──")
    for doc in miembros:
        print(f"    • {doc}")

print("\n" + "=" * 65)
print("DISTRIBUCIÓN DE DOCUMENTOS")
print("=" * 65)
dist = Counter(etiquetas)
for cid, count in sorted(dist.items()):
    barra = "█" * count
    print(f"  Cluster {cid}: {barra} ({count} docs)")
