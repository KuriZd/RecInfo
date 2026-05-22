"""
Similitud Coseno con preprocesamiento completo usando NLTK
Pipeline: tokenización → stopwords → stemming → TF-IDF → coseno
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

CORPUS = [
    "La inteligencia artificial transforma la industria tecnológica moderna.",
    "Los algoritmos de machine learning aprenden patrones de grandes datos.",
    "Las redes neuronales profundas mejoran el reconocimiento de imágenes.",
    "La salud pública depende de políticas preventivas y educación ciudadana.",
    "El ejercicio físico regular mejora la salud y el bienestar personal.",
    "Los deportes de equipo fomentan la cooperación y la disciplina personal.",
    "La economía digital crea nuevas oportunidades de empleo y negocio.",
    "Las startups tecnológicas innovan con inteligencia artificial y datos.",
]

stop_es = set(stopwords.words('spanish'))
stemmer = SnowballStemmer('spanish')


def pipeline_nltk(texto: str) -> str:
    tokens = word_tokenize(texto.lower(), language='spanish')
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stop_es]
    tokens = [stemmer.stem(t) for t in tokens]
    return " ".join(tokens)


corpus_procesado = [pipeline_nltk(doc) for doc in CORPUS]

print("=" * 65)
print("PIPELINE NLTK — Transformación de documentos")
print("=" * 65)
for i, (original, procesado) in enumerate(zip(CORPUS, corpus_procesado)):
    print(f"\n  Doc {i+1}:")
    print(f"    Original : {original[:60]}")
    print(f"    Procesado: {procesado}")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus_procesado)
sim_matrix = cosine_similarity(X)

print("\n" + "=" * 65)
print("MATRIZ DE SIMILITUD COSENO (con NLTK preprocessing)")
print("=" * 65)
etiquetas = [f"D{i+1}" for i in range(len(CORPUS))]
header = f"{'':>5}" + "".join(f"{e:>7}" for e in etiquetas)
print(header)
print("─" * (5 + 7 * len(etiquetas)))
for i, fila in enumerate(sim_matrix):
    row = f"{etiquetas[i]:>5}"
    for val in fila:
        row += f"{val:>7.3f}"
    print(row)

print("\n" + "=" * 65)
print("TOP 3 PARES MÁS SIMILARES")
print("=" * 65)
pares = []
for i in range(len(CORPUS)):
    for j in range(i + 1, len(CORPUS)):
        pares.append((sim_matrix[i][j], i, j))
pares.sort(reverse=True)
for score, i, j in pares[:3]:
    print(f"\n  Score: {score:.4f}")
    print(f"  Doc {i+1}: {CORPUS[i]}")
    print(f"  Doc {j+1}: {CORPUS[j]}")

print("\n" + "=" * 65)
print("BÚSQUEDA POR CONSULTA")
print("=" * 65)
consulta = "redes neuronales e inteligencia artificial en imágenes"
consulta_proc = pipeline_nltk(consulta)
vec_consulta = vectorizer.transform([consulta_proc])
scores = cosine_similarity(vec_consulta, X).flatten()
ranking = np.argsort(scores)[::-1]

print(f"  Consulta: \"{consulta}\"")
print(f"  Procesada: \"{consulta_proc}\"")
print()
for rank, idx in enumerate(ranking, 1):
    print(f"  {rank}. [score={scores[idx]:.4f}] {CORPUS[idx]}")
