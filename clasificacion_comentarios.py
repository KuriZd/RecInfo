"""
Clasificación de comentarios — análisis de sentimiento con reglas
Clasifica comentarios en: Positivo, Negativo, Neutro
Exporta resultados a CSV.
"""

import csv
import re
from collections import Counter

# ─── Diccionarios de palabras clave ──────────────────────────────────────────
PALABRAS_POSITIVAS = {
    "excelente", "increíble", "genial", "fantástico", "maravilloso", "perfecto",
    "bueno", "bien", "buenísimo", "recomiendo", "amor", "feliz", "contento",
    "satisfecho", "útil", "rápido", "fácil", "cómodo", "hermoso", "encanta",
    "me gusta", "espectacular", "sorprendente", "eficiente", "confiable",
}

PALABRAS_NEGATIVAS = {
    "malo", "pésimo", "terrible", "horrible", "lento", "difícil", "caro",
    "decepcionante", "falla", "no funciona", "problema", "error", "roto",
    "defectuoso", "molesta", "odio", "basura", "fraude", "mala", "peor",
    "nunca más", "estafa", "devolución", "frustrado", "no sirve",
}

# ─── Corpus de comentarios simulados ─────────────────────────────────────────
COMENTARIOS = [
    "El producto llegó rápido y funciona perfectamente, muy recomendado",
    "Pésimo servicio, nunca llegó mi pedido y no me dan respuesta",
    "La calidad es buena considerando el precio que tiene",
    "Me encanta la aplicación, es muy fácil de usar y rápida",
    "Terrible experiencia, el producto vino roto y el soporte es malísimo",
    "El envío tardó pero el producto llegó en buenas condiciones",
    "No me convenció del todo, esperaba algo mejor por ese precio",
    "Increíble calidad, superó todas mis expectativas completamente",
    "El servicio al cliente es excelente, resolvieron mi problema de inmediato",
    "Fraude total, el producto no corresponde a lo que anunciaron",
    "Funciona bien pero podría ser más rápido en ciertos procesos",
    "Compré tres veces y siempre llegó perfecto, sin ningún problema",
    "Horrible, se rompió al segundo día de uso, muy decepcionante",
    "El diseño es hermoso y la calidad de los materiales es buena",
    "Mala experiencia, el soporte tardó semanas en contestar",
    "Producto útil y práctico, cumple con lo que promete en la descripción",
    "Lento y defectuoso, no lo volvería a comprar jamás nunca",
    "Satisfecho con la compra, recomiendo este vendedor sin dudarlo",
    "Me parece bien, aunque la guía de instalación podría ser más clara",
    "Excelente relación calidad precio, uno de los mejores que he comprado",
]


def limpiar(texto: str) -> str:
    return re.sub(r'[^\w\s]', ' ', texto.lower())


def clasificar(texto: str) -> tuple[str, float]:
    texto_limpio = limpiar(texto)
    tokens = set(texto_limpio.split())

    pos = sum(1 for p in PALABRAS_POSITIVAS if p in texto_limpio)
    neg = sum(1 for p in PALABRAS_NEGATIVAS if p in texto_limpio)

    if pos > neg:
        confianza = min(1.0, 0.5 + (pos - neg) * 0.15)
        return "Positivo", round(confianza, 2)
    elif neg > pos:
        confianza = min(1.0, 0.5 + (neg - pos) * 0.15)
        return "Negativo", round(confianza, 2)
    else:
        return "Neutro", 0.50


# ─── Clasificación y exportación ──────────────────────────────────────────────
resultados = []
for i, comentario in enumerate(COMENTARIOS, 1):
    sentimiento, confianza = clasificar(comentario)
    resultados.append({
        "id": i,
        "comentario": comentario,
        "sentimiento": sentimiento,
        "confianza": confianza,
    })

CSV_OUT = "sentimientos_resultados_100.csv"
with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "comentario", "sentimiento", "confianza"])
    writer.writeheader()
    writer.writerows(resultados)

print("=" * 65)
print("CLASIFICACIÓN DE COMENTARIOS — Resultados")
print("=" * 65)
for r in resultados:
    emoji = "✅" if r["sentimiento"] == "Positivo" else ("❌" if r["sentimiento"] == "Negativo" else "⚪")
    print(f"  {emoji} [{r['sentimiento']:<9} {r['confianza']:.2f}] {r['comentario'][:55]}")

dist = Counter(r["sentimiento"] for r in resultados)
print("\n" + "=" * 65)
print("DISTRIBUCIÓN")
print("=" * 65)
for sent, count in dist.most_common():
    print(f"  {sent:<12} {'█' * count} ({count})")

print(f"\n  Archivo exportado: {CSV_OUT}")
