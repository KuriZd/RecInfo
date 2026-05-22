# Actividad 1.4 — Metadatos, Indexación y Organización de Información Digital

**Alumno:** Zamudio Damián Oscar Kuricaveri — 22120729  
**Materia:** Recuperación de Información  
**Asesor:** Jesús Eduardo Alcaraz Chávez  
**Fecha:** Marzo 2026

---

## Objetivo

Comprender el rol de los metadatos en los sistemas de recuperación de información, analizar los principales estándares de metadatos y explorar cómo la correcta organización de la información impacta en la eficiencia de búsqueda y recuperación.

---

## 1. ¿Qué son los metadatos?

Los metadatos son datos que describen otros datos. En el contexto de recuperación de información, los metadatos proporcionan contexto estructurado sobre un recurso digital: quién lo creó, cuándo, sobre qué tema, en qué formato y bajo qué condiciones de acceso.

La diferencia fundamental entre un documento con metadatos correctos y uno sin ellos es análoga a la diferencia entre un libro catalogado en una biblioteca y uno abandonado en el suelo: ambos contienen la misma información, pero solo el primero puede ser recuperado eficientemente.

---

## 2. Estándares principales de metadatos

### Dublin Core

Es el estándar más extendido para describir recursos digitales en general. Define 15 elementos básicos:

| Elemento | Descripción | Ejemplo |
|---|---|---|
| `dc:title` | Nombre del recurso | "Análisis de sentimientos en Twitter" |
| `dc:creator` | Responsable del contenido | "Zamudio Damián, O.K." |
| `dc:subject` | Tema o palabras clave | "NLP, sentimiento, Twitter" |
| `dc:description` | Resumen del contenido | "Estudio comparativo de..." |
| `dc:date` | Fecha de creación | "2026-02-15" |
| `dc:type` | Tipo de recurso | "Text", "Dataset", "Software" |
| `dc:format` | Formato del archivo | "application/pdf" |
| `dc:identifier` | Identificador único | DOI, ISBN, URL |
| `dc:language` | Idioma | "es" (español) |
| `dc:rights` | Derechos de uso | "CC BY 4.0" |

### Schema.org

Vocabulario semántico utilizado por Google, Bing y otros motores de búsqueda para entender el contenido de páginas web. Permite marcar artículos, eventos, productos y personas con significado estructurado.

### EXIF / XMP

Metadatos embebidos en archivos de imagen y video. Almacenan información técnica como resolución, modelo de cámara, coordenadas GPS y ajustes de exposición.

---

## 3. Metadatos en el proyecto RSS

En el sistema de recuperación de información desarrollado para el curso, cada artículo recolectado almacena los siguientes metadatos:

```
feed_id     → Fuente del artículo (referencia a tabla feeds)
title       → Título del artículo
link        → URL única del recurso (identificador)
published   → Fecha de publicación en formato ISO 8601
summary     → Resumen o descripción del contenido
fetched_at  → Marca temporal de la recolección
```

Este esquema de metadatos permite:
- Recuperar artículos por rango de fechas (`published`)
- Filtrar por fuente (`feed_id`)
- Buscar por contenido textual (`title`, `summary` vía FTS5)
- Ordenar por relevancia temporal o frecuencia

---

## 4. Indexación invertida

El índice invertido es la estructura de datos central en todo motor de búsqueda moderno. En lugar de recorrer todos los documentos por cada consulta, el índice mapea cada término del vocabulario a la lista de documentos donde aparece.

### Ejemplo simplificado

**Corpus:**
- Doc1: "inteligencia artificial en educación"
- Doc2: "educación digital y tecnología"
- Doc3: "tecnología aplicada a inteligencia artificial"

**Índice invertido resultante:**

| Término | Documentos |
|---|---|
| `inteligencia` | Doc1, Doc3 |
| `artificial` | Doc1, Doc3 |
| `educación` | Doc1, Doc2 |
| `digital` | Doc2 |
| `tecnología` | Doc2, Doc3 |

**Consulta:** "inteligencia artificial"  
**Resultado:** Doc1 ∩ Doc3 = {Doc1, Doc3}

SQLite FTS5 implementa internamente un índice invertido con soporte para operadores booleanos, búsqueda por prefijo y ranking por BM25.

---

## 5. Impacto de los metadatos en el ranking de recuperación

Los motores de búsqueda modernos consideran los metadatos como señales de relevancia. Un documento con `<title>` descriptivo, metadatos `description` precisos y texto estructurado con encabezados semánticos (`<h1>`, `<h2>`) obtiene mejor posición que uno con metadatos vacíos o engañosos.

En el contexto académico, el uso correcto de metadatos Dublin Core en repositorios institucionales mejora la visibilidad de tesis y artículos en agregadores como BASE (Bielefeld Academic Search Engine) y Google Scholar.

---

## 6. Organización jerárquica vs. facetada

### Organización jerárquica (clasificación decimal)

Asigna cada documento a una categoría en un árbol de temas. Ejemplo: la clasificación Dewey ubica "inteligencia artificial" en 006.3 (Inteligencia artificial).

**Ventaja:** Clara, intuitiva.  
**Desventaja:** Un documento sobre "IA aplicada a la salud" pertenece a dos categorías simultáneamente.

### Organización facetada

Permite asignar múltiples atributos independientes (facetas) a un recurso. Ejemplo: un artículo puede clasificarse simultáneamente por *tema* (IA), *año* (2025), *tipo* (artículo), *idioma* (español) y *metodología* (experimental).

**Ventaja:** Más flexible y expresiva para consultas multi-criterio.  
**Uso práctico:** Amazon, eBay y la mayoría de repositorios académicos modernos.

---

## 7. Conclusión

Los metadatos son la infraestructura invisible de todo sistema de recuperación de información eficiente. Sin una descripción adecuada de los recursos digitales, la búsqueda se convierte en una exploración ciega de volúmenes enormes de datos. La adopción de estándares como Dublin Core y la implementación de índices invertidos como FTS5 son los pilares técnicos que hacen posible la recuperación precisa y escalable de información en cualquier colección digital.
