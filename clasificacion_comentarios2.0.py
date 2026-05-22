"""
Clasificación de comentarios v2.0
Mejoras respecto a v1: puntuación ponderada, detección de negaciones,
intensificadores, lectura desde CSV y exportación de resultados.
"""

import csv
import re
from pathlib import Path

PESOS_POS = {
    "excelente": 3, "increíble": 3, "espectacular": 3, "perfecto": 3,
    "maravilloso": 2, "fantástico": 2, "genial": 2, "encanta": 2,
    "bueno": 1, "bien": 1, "recomiendo": 1, "útil": 1, "rápido": 1,
    "fácil": 1, "satisfecho": 1, "confiable": 1, "eficiente": 1,
}

PESOS_NEG = {
    "pésimo": 3, "horrible": 3, "terrible": 3, "fraude": 3,
    "decepcionante": 2, "defectuoso": 2, "roto": 2, "odio": 2,
    "malo": 1, "falla": 1, "lento": 1, "caro": 1, "problema": 1,
    "error": 1, "basura": 1, "frustrado": 1, "nunca más": 2,
}

NEGACIONES = {"no", "nunca", "jamás", "tampoco", "sin", "ni"}
INTENSIFICADORES = {"muy", "súper", "demasiado", "bastante", "totalmente", "completamente"}


def analizar_sentimiento(texto: str) -> dict:
    texto_lower = texto.lower()
    tokens = re.findall(r'\b\w+\b', texto_lower)

    score_pos = 0
    score_neg = 0

    for i, token in enumerate(tokens):
        # Verificar si hay negación antes del término
        contexto = tokens[max(0, i-2):i]
        negado = any(n in contexto for n in NEGACIONES)
        intensificado = any(iv in contexto for iv in INTENSIFICADORES)
        mult = 1.5 if intensificado else 1.0

        if token in PESOS_POS:
            delta = PESOS_POS[token] * mult
            score_neg += delta if negado else 0
            score_pos += 0 if negado else delta
        elif token in PESOS_NEG:
            delta = PESOS_NEG[token] * mult
            score_pos += delta if negado else 0
            score_neg += 0 if negado else delta

    # Bigramas (frases de dos palabras)
    for i in range(len(tokens) - 1):
        bigrama = f"{tokens[i]} {tokens[i+1]}"
        if bigrama in PESOS_NEG:
            score_neg += PESOS_NEG[bigrama]

    total = score_pos + score_neg
    if total == 0:
        return {"sentimiento": "Neutro", "score": 0.0, "score_pos": 0, "score_neg": 0}

    ratio = (score_pos - score_neg) / max(total, 1)
    if ratio > 0.1:
        sentimiento = "Positivo"
    elif ratio < -0.1:
        sentimiento = "Negativo"
    else:
        sentimiento = "Neutro"

    return {
        "sentimiento": sentimiento,
        "score": round(ratio, 3),
        "score_pos": round(score_pos, 2),
        "score_neg": round(score_neg, 2),
    }


def procesar_archivo(ruta_csv: str) -> list[dict]:
    resultados = []
    with open(ruta_csv, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            texto = row.get("texto") or row.get("comentario") or ""
            analisis = analizar_sentimiento(texto)
            resultados.append({
                "id": row.get("id", ""),
                "texto": texto[:70],
                **analisis,
            })
    return resultados


def procesar_lista(comentarios: list[str]) -> list[dict]:
    resultados = []
    for i, texto in enumerate(comentarios, 1):
        analisis = analizar_sentimiento(texto)
        resultados.append({"id": i, "texto": texto[:70], **analisis})
    return resultados


# ─── Demo ─────────────────────────────────────────────────────────────────────
DEMO = [
    "El producto es muy bueno, llegó rápido y funciona perfectamente",
    "No me gustó nada, es demasiado malo para el precio que cuesta",
    "Está bien, nada especial pero cumple con lo básico",
    "Increíble calidad, completamente satisfecho con la compra",
    "Nunca más compro aquí, pésimo servicio al cliente y sin respuesta",
    "El envío tardó pero el producto llegó en buenas condiciones finalmente",
    "No es tan malo como dicen, a mí me funcionó sin problemas",
    "Totalmente defectuoso, se rompió al primer día de uso",
]

fuente = "100comentarios.csv" if Path("100comentarios.csv").exists() else None
if fuente:
    resultados = procesar_archivo(fuente)
    print(f"Procesando desde: {fuente}")
else:
    resultados = procesar_lista(DEMO)
    print("Procesando demo interno")

print("\n" + "=" * 70)
print(f"{'ID':>3}  {'Sentimiento':<12} {'Score':>7}  {'Texto'}")
print("─" * 70)
for r in resultados:
    emoji = "✅" if r["sentimiento"] == "Positivo" else ("❌" if r["sentimiento"] == "Negativo" else "⚪")
    print(f"  {r['id']:>2}  {emoji} {r['sentimiento']:<11} {r['score']:>7.3f}  {r['texto']}")

CSV_OUT = "sentimientos_resultados.csv"
with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "texto", "sentimiento", "score", "score_pos", "score_neg"])
    writer.writeheader()
    writer.writerows(resultados)

print(f"\n  Resultados guardados en: {CSV_OUT}")
