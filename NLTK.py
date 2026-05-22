"""
NLTK - Procesamiento de Lenguaje Natural en Español
Conceptos: tokenización, stopwords, stemming, frecuencia de palabras
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter

# Descargar recursos necesarios (solo la primera vez)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

# ─── Corpus de prueba ────────────────────────────────────────────────────────
texto = """
La inteligencia artificial está transformando la forma en que buscamos y recuperamos información.
Los motores de búsqueda modernos utilizan algoritmos avanzados para indexar millones de documentos.
El procesamiento de lenguaje natural permite analizar textos en español de manera automática.
Las redes neuronales aprenden patrones complejos a partir de grandes conjuntos de datos.
La minería de texto extrae conocimiento útil de documentos no estructurados.
"""

print("=" * 60)
print("1. TOKENIZACIÓN POR ORACIONES")
print("=" * 60)
oraciones = sent_tokenize(texto, language='spanish')
for i, oracion in enumerate(oraciones, 1):
    print(f"  Oración {i}: {oracion.strip()}")

print("\n" + "=" * 60)
print("2. TOKENIZACIÓN POR PALABRAS")
print("=" * 60)
tokens = word_tokenize(texto.lower(), language='spanish')
tokens_limpios = [t for t in tokens if t.isalpha()]
print(f"  Total tokens: {len(tokens_limpios)}")
print(f"  Primeros 15: {tokens_limpios[:15]}")

print("\n" + "=" * 60)
print("3. ELIMINACIÓN DE STOPWORDS")
print("=" * 60)
stop_es = set(stopwords.words('spanish'))
tokens_sin_stop = [t for t in tokens_limpios if t not in stop_es]
print(f"  Stopwords del español (muestra): {list(stop_es)[:10]}")
print(f"  Tokens antes: {len(tokens_limpios)} | Después: {len(tokens_sin_stop)}")
print(f"  Tokens filtrados: {tokens_sin_stop[:15]}")

print("\n" + "=" * 60)
print("4. STEMMING (Snowball en Español)")
print("=" * 60)
stemmer = SnowballStemmer('spanish')
tokens_stem = [stemmer.stem(t) for t in tokens_sin_stop]
ejemplos = list(zip(tokens_sin_stop[:10], tokens_stem[:10]))
print(f"  {'Palabra original':<25} {'Stem'}")
print(f"  {'-'*40}")
for original, stem in ejemplos:
    print(f"  {original:<25} {stem}")

print("\n" + "=" * 60)
print("5. FRECUENCIA DE TÉRMINOS")
print("=" * 60)
freq = Counter(tokens_sin_stop)
print(f"  Top 10 palabras más frecuentes:")
for palabra, count in freq.most_common(10):
    barra = "█" * count
    print(f"  {palabra:<20} {barra} ({count})")
