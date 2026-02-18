# Proyecto de Recuperación de Información (IR)
## Guía de APIs por Ejes Temáticos (2026)

Este documento contiene las fuentes de datos (APIs) y sus respectivas documentaciones oficiales para el desarrollo de investigaciones en recuperación de información.

---

### 1. Inteligencia Artificial en la Vida Diaria
* **Hugging Face API:** [Documentación](https://huggingface.co/docs/hub/api)
* **arXiv API:** [Documentación](https://info.arxiv.org/help/api/basics.html)
* **INEGI (TIC):** [Documentación](https://www.inegi.org.mx/servicios/api_indicadores.html)

---

### 2. Salud Mental y Bienestar en Jóvenes
* **INEGI (BIARE):** [Documentación Técnica](https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/MANUAL_API_INDICADORES_V1_1.pdf)
* **WHO / OMS (Global Health Observatory):** [Documentación OData](https://www.who.int/data/gho/info/gho-odata-api)
* **World Bank Health:** [Documentación API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889387-api-documentation)

---

### 3. Algoritmos, Poder y Sociedad Digital
* **GDELT Project:** [Documentación Doc API](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
* **OpenAlex API:** [Documentación Técnica](https://docs.openalex.org/)
* **World Bank Digital Development:** [Documentación Temática](https://data.worldbank.org/topic/digital-development)

---

### 🛠️ Consejos Técnicos para la Recuperación
1. **Librerías Recomendadas:** Usa `requests` y `pandas` en Python.
2. **Tokens de Acceso:** Requeridos para INEGI y Hugging Face.
3. **Procesamiento:** Considera usar técnicas de NLP para limpiar los textos obtenidos de arXiv y GDELT.