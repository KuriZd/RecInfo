"""
NLTK Activity - Análisis comparativo de dos documentos en español
Actividad: procesar un mini corpus, comparar distribución de términos
y visualizar diferencias entre documentos con y sin preprocesamiento.
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

# ─── Mini corpus ─────────────────────────────────────────────────────────────
CORPUS = {
    "Tecnología": """
        La inteligencia artificial y el aprendizaje automático están revolucionando
        la industria tecnológica. Los algoritmos de machine learning procesan grandes
        volúmenes de datos para extraer patrones relevantes. La automatización
        inteligente mejora la productividad en empresas de tecnología y manufactura.
        Los modelos de lenguaje grande generan texto coherente y útil para los usuarios.
    """,
    "Salud": """
        La salud pública requiere políticas preventivas basadas en evidencia científica.
        Las enfermedades crónicas como la diabetes y la hipertensión afectan a millones
        de personas en México. La nutrición adecuada y el ejercicio regular son pilares
        fundamentales del bienestar. Los sistemas de salud deben garantizar acceso
        equitativo a tratamientos y medicamentos esenciales para la población.
    """,
    "Educación": """
        La educación digital transforma los métodos de enseñanza y aprendizaje en todos
        los niveles. Las plataformas en línea facilitan el acceso a contenidos educativos
        de calidad sin importar la ubicación geográfica. Los estudiantes desarrollan
        habilidades digitales esenciales para el mercado laboral moderno. La formación
        continua y el aprendizaje autodirigido son competencias clave del siglo veintiuno.
    """,
}

stop_es = set(stopwords.words('spanish'))
stemmer = SnowballStemmer('spanish')


def preprocesar(texto: str, usar_stopwords: bool = True, usar_stem: bool = False) -> list[str]:
    tokens = word_tokenize(texto.lower(), language='spanish')
    tokens = [t for t in tokens if t.isalpha()]
    if usar_stopwords:
        tokens = [t for t in tokens if t not in stop_es]
    if usar_stem:
        tokens = [stemmer.stem(t) for t in tokens]
    return tokens


def imprimir_top(nombre: str, tokens: list[str], n: int = 8):
    freq = Counter(tokens)
    print(f"\n  [{nombre}] Top {n} términos:")
    for palabra, cnt in freq.most_common(n):
        print(f"    {palabra:<20} {'█' * cnt} ({cnt})")


print("=" * 65)
print("ANÁLISIS DE CORPUS — CON Y SIN PREPROCESAMIENTO")
print("=" * 65)

for doc, texto in CORPUS.items():
    print(f"\n{'─'*65}")
    print(f"  DOCUMENTO: {doc}")

    raw = preprocesar(texto, usar_stopwords=False)
    limpio = preprocesar(texto, usar_stopwords=True)
    stem = preprocesar(texto, usar_stopwords=True, usar_stem=True)

    print(f"  Tokens sin filtrar:       {len(raw)}")
    print(f"  Tokens sin stopwords:     {len(limpio)}")
    print(f"  Tokens con stemming:      {len(stem)}")
    imprimir_top("Sin stopwords", limpio, n=6)
    imprimir_top("Con stemming", stem, n=6)

print("\n" + "=" * 65)
print("VOCABULARIO COMPARTIDO ENTRE DOCUMENTOS")
print("=" * 65)
vocabs = {doc: set(preprocesar(txt)) for doc, txt in CORPUS.items()}
docs = list(vocabs.keys())
for i in range(len(docs)):
    for j in range(i + 1, len(docs)):
        comun = vocabs[docs[i]] & vocabs[docs[j]]
        print(f"  {docs[i]} ∩ {docs[j]}: {sorted(comun)}")
