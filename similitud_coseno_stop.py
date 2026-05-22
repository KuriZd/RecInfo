"""
Similitud Coseno CON eliminación de stopwords
Compara resultados vs. similitud_coseno.py para mostrar el impacto
de las stopwords en la representación vectorial.
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

STOPWORDS_ES = [
    "de", "la", "el", "los", "las", "un", "una", "unos", "unas",
    "y", "en", "con", "a", "se", "que", "por", "para", "del",
    "al", "es", "su", "sus", "le", "lo", "les", "como", "más",
    "pero", "o", "si", "no", "ya", "este", "esta", "estos", "estas",
    "fue", "son", "ser", "tiene", "hay", "también",
]


def calcular_sim(corpus, stopwords=None):
    vec = TfidfVectorizer(stop_words=stopwords)
    X = vec.fit_transform(corpus)
    return cosine_similarity(X), vec.get_feature_names_out()


sim_con, vocab_con = calcular_sim(CORPUS, stopwords=STOPWORDS_ES)
sim_sin, vocab_sin = calcular_sim(CORPUS, stopwords=None)

print("=" * 65)
print("COMPARACIÓN: CON vs. SIN stopwords")
print("=" * 65)
print(f"\n  Vocabulario SIN stopwords: {len(vocab_sin)} términos")
print(f"  Vocabulario CON stopwords: {len(vocab_con)} términos")
print(f"  Reducción: {len(vocab_sin) - len(vocab_con)} términos eliminados\n")

print("─" * 65)
print(f"{'Par':<12} {'Sin stop':>10} {'Con stop':>10} {'Diferencia':>12}")
print("─" * 65)

etiquetas = [f"D{i+1}" for i in range(len(CORPUS))]
for i in range(len(CORPUS)):
    for j in range(i + 1, len(CORPUS)):
        s_sin = sim_sin[i][j]
        s_con = sim_con[i][j]
        diff = s_con - s_sin
        par = f"{etiquetas[i]}-{etiquetas[j]}"
        marker = " ▲" if diff > 0.05 else (" ▼" if diff < -0.05 else "  ")
        print(f"  {par:<10} {s_sin:>10.4f} {s_con:>10.4f} {diff:>+11.4f}{marker}")

print("\n" + "=" * 65)
print("INTERPRETACIÓN")
print("=" * 65)
print("""
  • Cuando se eliminan stopwords, los vectores TF-IDF capturan mejor
    el contenido semántico real de cada documento.

  • Pares que comparten stopwords frecuentes (de, la, el...) pueden
    mostrar similitud artificial cuando NO se filtran.

  • La reducción del vocabulario hace que el modelo sea más eficiente
    y los clusters resultantes sean más coherentes temáticamente.
""")
