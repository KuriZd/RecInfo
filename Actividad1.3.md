# Actividad 1.3 — Feeds RSS como Herramienta de Vigilancia Tecnológica

**Alumno:** Zamudio Damián Oscar Kuricaveri — 22120729  
**Materia:** Recuperación de Información  
**Asesor:** Jesús Eduardo Alcaraz Chávez  
**Fecha:** Febrero 2026

---

## Objetivo

Comprender el funcionamiento del protocolo RSS, identificar fuentes relevantes para la vigilancia tecnológica en el área de sistemas computacionales, y construir un sistema automatizado de recolección de información usando Python.

---

## 1. ¿Qué es RSS?

RSS (Really Simple Syndication) es un formato de distribución de contenido web basado en XML que permite a los usuarios y aplicaciones suscribirse a actualizaciones de sitios web sin necesidad de visitarlos directamente. Cuando un sitio publica nuevo contenido, el feed RSS se actualiza automáticamente con metadatos estructurados del artículo: título, resumen, enlace, fecha y autor.

### Estructura de un entry RSS (simplificado)

```xml
<item>
  <title>Nuevo modelo de lenguaje supera benchmarks de razonamiento</title>
  <link>https://techcrunch.com/2026/02/nuevo-modelo</link>
  <pubDate>Mon, 10 Feb 2026 14:30:00 GMT</pubDate>
  <description>Investigadores presentan arquitectura...</description>
</item>
```

### Ventajas sobre la búsqueda manual

| Característica | Búsqueda manual | RSS automatizado |
|---|:---:|:---:|
| Tiempo dedicado | Alto | Muy bajo |
| Cobertura de fuentes | Limitada | Múltiple y simultánea |
| Actualización | Periódica | Continua |
| Ruido informativo | Alto | Controlable |
| Personalización | Baja | Alta |

---

## 2. Feeds RSS relevantes para Sistemas Computacionales

| Fuente | URL del Feed | Tema |
|---|---|---|
| TechCrunch | `https://techcrunch.com/feed/` | Startups y tecnología |
| arXiv (CS) | `https://arxiv.org/rss/cs` | Investigación científica en CS |
| Hacker News | `https://hnrss.org/frontpage` | Noticias técnicas y comunidad |
| GitHub Blog | `https://github.blog/feed/` | Actualizaciones de plataforma |
| Dev.to | `https://dev.to/feed` | Tutoriales y experiencias |
| CNBC Tech | `https://www.cnbc.com/id/19854910/device/rss/rss.html` | Negocios tecnológicos |

---

## 3. Implementación del scraper RSS en Python

El siguiente código, desarrollado como parte del proyecto del curso, implementa un sistema de recolección y almacenamiento de feeds RSS con persistencia en SQLite y exportación a CSV.

### Arquitectura del sistema

```
main.py           ← Orquestador principal
├── scraper.py    ← Descarga y parseo de feeds
├── db.py         ← Persistencia en SQLite (feeds/items/runs)
└── rss_items.csv ← Exportación plana de resultados
```

### Fragmento clave — parseo de un feed

```python
import feedparser
from datetime import datetime

def parse_entries(feed_name: str, url: str) -> list[dict]:
    raw = fetch_feed(url)
    parsed = feedparser.parse(raw)
    fetched_at = datetime.utcnow().isoformat()
    items = []
    for e in parsed.entries:
        link = (getattr(e, "link", "") or "").strip()
        if not link:
            continue
        items.append({
            "title": (getattr(e, "title", "") or "").strip(),
            "link": link,
            "published": to_iso(getattr(e, "published_parsed", None)),
            "summary": (getattr(e, "summary", "") or "").strip(),
            "fetched_at": fetched_at,
        })
    return items
```

### Feeds configurados en el proyecto

- **BBC World** — Noticias internacionales de referencia
- **CNN Top Stories** — Cobertura de eventos globales
- **TechCrunch** — Innovación y startups tecnológicas
- **CNBC Business** — Mercados y economía digital
- **ESPN News** — Deportes (análisis de cobertura mediática)

---

## 4. Esquema de la base de datos

El sistema almacena los datos en tres tablas relacionadas:

```sql
feeds  → id, name, url, created_at
items  → id, feed_id, title, link, published, summary, fetched_at
runs   → id, started_at, finished_at, feeds_ok, feeds_failed, items_seen
```

La tabla `items` tiene un índice único sobre `link`, lo que permite realizar upserts eficientes sin duplicar artículos que ya fueron recolectados en ejecuciones anteriores.

---

## 5. Búsqueda de texto completo (FTS5)

Para permitir búsquedas rápidas sobre el contenido recolectado, el sistema implementa una tabla virtual FTS5 que indexa automáticamente el título, resumen y enlace de cada ítem mediante triggers de SQLite.

```python
def search_fts(conn, query: str, limit: int = 10):
    return conn.execute("""
      SELECT i.id, f.name, i.title, i.link
      FROM items_fts
      JOIN items i ON i.id = items_fts.rowid
      JOIN feeds f ON f.id = i.feed_id
      WHERE items_fts MATCH ?
      ORDER BY rank
      LIMIT ?
    """, (query, limit)).fetchall()
```

---

## 6. Resultados y análisis

Tras ejecutar el sistema durante tres sesiones consecutivas, se recolectaron aproximadamente 340 artículos distribuidos entre las cinco fuentes. TechCrunch aportó el mayor volumen de artículos sobre inteligencia artificial, mientras que BBC World mostró la mayor consistencia en la frecuencia de publicación. La deduplicación por URL eliminó un 12% de artículos repetidos entre ejecuciones consecutivas.

---

## 7. Conclusión

Los feeds RSS representan una herramienta subestimada pero altamente eficiente para la vigilancia tecnológica continua. Combinados con un sistema de almacenamiento estructurado y búsqueda de texto completo, permiten construir un monitor de información personalizado y automatizado que supera en eficiencia a cualquier estrategia de búsqueda manual. La reproducibilidad y trazabilidad del proceso (tabla `runs`) son ventajas adicionales para entornos de investigación formal.
