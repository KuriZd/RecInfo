# Reporte: Web Semántica y Datos Enlazados

---

## Misión 0 — ¿Qué es la Web Semántica?

La web actual está diseñada para que los humanos la lean. Un navegador muestra texto, imágenes y tablas, pero una computadora solo ve HTML sin significado. La **Web Semántica** propone agregar una capa de significado estructurado para que las máquinas puedan *entender* la información, no solo mostrarla.

El mecanismo clave son los **datos enlazados** (*Linked Data*): cada entidad del mundo (una persona, un lugar, un concepto) recibe un URI único, y las relaciones entre entidades se expresan como tripletas del tipo:

```
sujeto → predicado → objeto
<http://datos.gob.mx/recurso/programa/Gertrudis-Bocanegra> → rdf:type → schema:GovernmentService
```

Así, una máquina puede navegar de un recurso a otro siguiendo los enlaces, igual que un humano sigue hipervínculos.

---

## Misión 1 — Fragilidad del Scraping vs. Datos Semánticos

En este proyecto construimos un scraper RSS (`scraper.py`) que extrae noticias de fuentes mexicanas. RSS ya es un paso hacia la semántica: es XML estructurado, no HTML libre. Aun así, tiene limitaciones:

| Característica | Scraping HTML | RSS/Atom | RDF / JSON-LD |
|---|---|---|---|
| Estructura | Ninguna | Parcial | Completa |
| Semántica | No | No | Sí |
| Estabilidad | Muy frágil | Estable | Estable |
| Reutilizable entre fuentes | No | Con adaptación | Sí (vocabularios compartidos) |

**El problema concreto:** si El País cambia el nombre de su clase CSS de `.article-title` a `.headline`, el scraper falla silenciosamente y obtiene cero noticias. Con RDF, el productor publica un endpoint SPARQL; el consumidor consulta `schema:headline` sin importar la implementación interna.

---

## Misión 2 — URIs y Disambiguación de Entidades

Uno de los problemas centrales en recuperación de información es la **ambigüedad léxica**. La palabra "Mencho" en nuestro dataset (`analisis_mencho_2026.json`) puede referirse a:

- Nemesio Oseguera Cervantes (líder del CJNG)
- Cualquier persona con ese apodo

Un sistema de recuperación basado solo en texto los trata igual. Con URIs semánticos:

```turtle
<http://wikidata.org/entity/Q16489518> a schema:Person ;
    schema:name "Nemesio Oseguera Cervantes" ;
    schema:alternateName "El Mencho" ;
    owl:sameAs <http://dbpedia.org/resource/Nemesio_Oseguera_Cervantes> .
```

Ahora dos bases de datos distintas pueden referirse al mismo recurso sin ambigüedad, y un motor de búsqueda puede enriquecer los resultados automáticamente.

---

## Misión 3 — SPARQL vs. Búsqueda por Palabras Clave

Nuestro sistema actual de recuperación funciona con TF-IDF (`TF-IDF.py`) y similitud coseno (`similitud_coseno.py`). Estos métodos son potentes para ranquear documentos, pero no pueden responder preguntas estructuradas.

**Pregunta:** *¿Qué programas de gobierno ofrecen becas para estudiantes universitarios en México?*

Con TF-IDF buscamos el texto más similar, pero podemos obtener artículos periodísticos, opiniones o resultados de otros países. Con SPARQL sobre un grafo semántico:

```sparql
SELECT ?programa ?descripcion WHERE {
  ?programa rdf:type schema:GovernmentService ;
            schema:audience <urn:grupo:estudiantesUniversitarios> ;
            schema:areaServed <urn:pais:Mexico> ;
            schema:description ?descripcion .
}
```

El resultado es exacto, sin ruido, y se puede combinar con otras fuentes enlazadas (Wikidata, datos.gob.mx) sin código adicional.

---

## Conclusión

La Web Semántica no reemplaza técnicas como TF-IDF o K-Means; las complementa. En un flujo ideal:

1. **Extracción** — RSS / scraping estructurado para obtener datos crudos.
2. **Enriquecimiento semántico** — anotación con entidades (NER) y URIs.
3. **Almacenamiento** — grafo RDF en lugar de CSV plano.
4. **Recuperación** — SPARQL para preguntas estructuradas + TF-IDF para búsqueda de texto libre.

Los CSVs de nuestro proyecto (`sentimientos_resultados.csv`, `clasificacion_sarcasmo_200.csv`) son el equivalente artesanal del paso 3. El siguiente nivel sería publicarlos como datos enlazados con vocabularios estándar (`schema:Review`, `nif:Sentence`) para que otros sistemas puedan consumirlos sin documentación adicional.
