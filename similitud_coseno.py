"""
Similitud Coseno — sin eliminación de stopwords
Mide qué tan parecidos son dos documentos basándose en el ángulo
entre sus vectores TF-IDF en el espacio de términos.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

CORPUS = [
    "la inteligencia artificial transforma la industria tecnológica moderna",
    "los algoritmos de machine learning aprenden patrones de grandes datos",
    "las redes neuronales profundas mejoran el reconocimiento de imágenes",
    "la salud pública depende de políticas preventivas y educación ciudadana",
    "el ejercicio físico regular mejora la salud y el bienestar personal",
    "los deportes de equipo fomentan la cooperación y la disciplina personal",
    "la economía digital crea nuevas oportunidades de empleo y negocio",
    "las startups tecnológicas innovan con inteligencia artificial y datos",
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(CORPUS)

sim_matrix = cosine_similarity(X)

print("=" * 65)
print("MATRIZ DE SIMILITUD COSENO (sin stopwords removidos)")
print("=" * 65)

etiquetas = [f"D{i+1}" for i in range(len(CORPUS))]
header = f"{'':>5}" + "".join(f"{e:>7}" for e in etiquetas)
print(header)
print("─" * (5 + 7 * len(etiquetas)))

for i, fila in enumerate(sim_matrix):
    row = f"{etiquetas[i]:>5}"
    for j, val in enumerate(fila):
        row += f"{val:>7.3f}"
    print(row)

print("\n" + "=" * 65)
print("PARES MÁS SIMILARES (excluye diagonal)")
print("=" * 65)

pares = []
for i in range(len(CORPUS)):
    for j in range(i + 1, len(CORPUS)):
        pares.append((sim_matrix[i][j], i, j))

pares.sort(reverse=True)
for score, i, j in pares[:5]:
    print(f"\n  Similitud: {score:.4f}")
    print(f"  Doc {i+1}: {CORPUS[i]}")
    print(f"  Doc {j+1}: {CORPUS[j]}")

print("\n" + "=" * 65)
print("DOCUMENTO MÁS SIMILAR A: Doc 1")
print("=" * 65)
scores = sim_matrix[0].copy()
scores[0] = 0  # excluir sí mismo
idx_max = np.argmax(scores)
print(f"  Consulta : {CORPUS[0]}")
print(f"  Más similar (Doc {idx_max+1}, score={scores[idx_max]:.4f}): {CORPUS[idx_max]}")
