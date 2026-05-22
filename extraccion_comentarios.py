"""
Extracción y clasificación de comentarios desde CSV
Lee un dataset, aplica análisis de sentimiento y sarcasmo,
y exporta un reporte consolidado.
"""

import csv
import re
from pathlib import Path
from collections import Counter

# ─── Clasificador de sentimiento ─────────────────────────────────────────────
POS = {"bueno", "excelente", "genial", "rápido", "fácil", "encanta", "perfecto",
       "recomiendo", "satisfecho", "útil", "increíble", "maravilloso", "feliz"}
NEG = {"malo", "pésimo", "horrible", "lento", "caro", "roto", "fraude",
       "basura", "terrible", "decepcionante", "falla", "problema", "nunca"}
SARCASMO = ["claro que sí", "obvio que", "como no", "qué sorpresa",
            "vaya que", "brillante idea", "muy original", "genio total"]


def sentimiento(texto: str) -> str:
    t = texto.lower()
    p = sum(1 for w in POS if w in t)
    n = sum(1 for w in NEG if w in t)
    if p > n:
        return "Positivo"
    elif n > p:
        return "Negativo"
    return "Neutro"


def detectar_sarcasmo(texto: str) -> int:
    t = texto.lower()
    return 1 if any(s in t for s in SARCASMO) else 0


def limpiar(texto: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', texto.lower())).strip()


def extraer_estadisticas(filas: list[dict]) -> dict:
    sentimientos = Counter(r["sentimiento"] for r in filas)
    sarcasmos = sum(r["sarcasmo"] for r in filas)
    avg_len = sum(len(r["texto"]) for r in filas) / max(len(filas), 1)
    return {
        "total": len(filas),
        "positivos": sentimientos.get("Positivo", 0),
        "negativos": sentimientos.get("Negativo", 0),
        "neutros": sentimientos.get("Neutro", 0),
        "sarcasmos": sarcasmos,
        "longitud_promedio": round(avg_len, 1),
    }


# ─── Leer CSV o usar corpus interno ──────────────────────────────────────────
FUENTES = ["100comentarios.csv", "dataset_redes_sociales_200.csv"]
datos_cargados = []

for ruta in FUENTES:
    if Path(ruta).exists():
        with open(ruta, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                texto = row.get("texto") or row.get("comentario") or ""
                if texto.strip():
                    datos_cargados.append({"id": row.get("id", ""), "texto": texto})
        print(f"  Cargado: {ruta} ({len(datos_cargados)} registros)")
        break

if not datos_cargados:
    print("  Usando corpus interno de demostración")
    DEMO_TEXTOS = [
        "Me encanta este producto, es excelente y muy fácil de usar",
        "Claro que sí, genio total el que diseñó esto, qué sorpresa que no funcione",
        "Pésimo servicio, nunca respondieron mis mensajes de soporte",
        "Bien, cumple con lo básico para el precio que tiene",
        "Increíble calidad, completamente recomendado para cualquier persona",
        "Como no, otra actualización que rompe todo lo que funcionaba bien",
        "El envío llegó a tiempo y el producto está en perfectas condiciones",
        "Horrible experiencia, el producto llegó roto y sin embalaje",
        "Vaya que sí, muy original el diseño copiado de otra marca",
        "Satisfecho con la compra, supera mis expectativas en todo",
    ]
    datos_cargados = [{"id": i+1, "texto": t} for i, t in enumerate(DEMO_TEXTOS)]

# ─── Procesamiento ───────────────────────────────────────────────────────────
resultados = []
for fila in datos_cargados:
    texto = fila["texto"]
    resultados.append({
        "id": fila["id"],
        "texto": texto,
        "texto_limpio": limpiar(texto),
        "sentimiento": sentimiento(texto),
        "sarcasmo": detectar_sarcasmo(texto),
        "longitud": len(texto),
    })

# ─── Reporte ──────────────────────────────────────────────────────────────────
stats = extraer_estadisticas(resultados)
print("\n" + "=" * 65)
print("REPORTE DE EXTRACCIÓN Y CLASIFICACIÓN")
print("=" * 65)
print(f"  Total registros:      {stats['total']}")
print(f"  Positivos:            {stats['positivos']}")
print(f"  Negativos:            {stats['negativos']}")
print(f"  Neutros:              {stats['neutros']}")
print(f"  Sarcasmo detectado:   {stats['sarcasmos']}")
print(f"  Longitud promedio:    {stats['longitud_promedio']} chars")

print("\n─" + "─" * 64)
print(f"{'ID':>4}  {'Sent':<10} {'Sarc'}  Texto")
print("─" * 65)
for r in resultados[:15]:
    s_emoji = "✅" if r["sentimiento"] == "Positivo" else ("❌" if r["sentimiento"] == "Negativo" else "⚪")
    sarc = "🎭" if r["sarcasmo"] else "  "
    print(f"  {str(r['id']):>3}  {s_emoji} {r['sentimiento']:<9} {sarc}  {r['texto'][:50]}")

CSV_OUT = "clasificacion_sarcasmo_200.csv"
with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "texto", "sentimiento", "sarcasmo", "longitud"])
    writer.writeheader()
    for r in resultados:
        writer.writerow({k: r[k] for k in ["id", "texto", "sentimiento", "sarcasmo", "longitud"]})

print(f"\n  Exportado: {CSV_OUT}")
