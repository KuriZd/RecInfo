"""
TF-IDF — Term Frequency · Inverse Document Frequency
Vectorización de documentos y cálculo manual + con sklearn.
"""

import math
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# ─── Corpus ──────────────────────────────────────────────────────────────────
CORPUS = [
    "la inteligencia artificial aprende de datos masivos",
    "los algoritmos de machine learning procesan información",
    "las redes neuronales imitan el cerebro humano",
    "el aprendizaje profundo mejora el reconocimiento de imágenes",
    "la minería de datos extrae patrones en grandes volúmenes",
    "los modelos de lenguaje generan texto coherente y útil",
    "la recuperación de información busca documentos relevantes",
    "los motores de búsqueda indexan millones de páginas web",
]

# ─── Cálculo MANUAL de TF-IDF ─────────────────────────────────────────────────

def tokenizar(texto: str) -> list[str]:
    return texto.lower().split()

def calcular_tf(tokens: list[str]) -> dict[str, float]:
    freq = Counter(tokens)
    total = len(tokens)
    return {palabra: count / total for palabra, count in freq.items()}

def calcular_idf(corpus_tokens: list[list[str]]) -> dict[str, float]:
    N = len(corpus_tokens)
    vocab = set(t for doc in corpus_tokens for t in doc)
    idf = {}
    for termino in vocab:
        docs_con_termino = sum(1 for doc in corpus_tokens if termino in doc)
        idf[termino] = math.log(N / docs_con_termino) + 1  # suavizado
    return idf

corpus_tokens = [tokenizar(doc) for doc in CORPUS]
idf_global = calcular_idf(corpus_tokens)

print("=" * 65)
print("1. TF-IDF MANUAL — Términos más relevantes por documento")
print("=" * 65)
for i, (doc, tokens) in enumerate(zip(CORPUS, corpus_tokens)):
    tf = calcular_tf(tokens)
    tfidf = {t: round(tf[t] * idf_global[t], 4) for t in tf}
    top3 = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"\n  Doc {i+1}: \"{doc[:45]}...\"" if len(doc) > 45 else f"\n  Doc {i+1}: \"{doc}\"")
    for term, score in top3:
        print(f"    {term:<30} TF-IDF: {score}")

# ─── TF-IDF con sklearn ────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("2. MATRIZ TF-IDF con sklearn")
print("=" * 65)

vectorizer = TfidfVectorizer(max_features=12)
X = vectorizer.fit_transform(CORPUS)
features = vectorizer.get_feature_names_out()

df = pd.DataFrame(
    X.toarray().round(3),
    columns=features,
    index=[f"Doc{i+1}" for i in range(len(CORPUS))]
)

print(df.to_string())

print("\n" + "=" * 65)
print("3. DOCUMENTO MÁS REPRESENTATIVO POR TÉRMINO")
print("=" * 65)
for feat in features:
    idx = df[feat].idxmax()
    score = df[feat].max()
    print(f"  {feat:<30} → {idx} (score: {score:.3f})")
