# Actividades 3 — Análisis Crítico de Medios, Algoritmos y Desinformación

**Alumno:** Zamudio Damián Oscar Kuricaveri — 22120729  
**Materia:** Recuperación de Información  
**Asesor:** Jesús Eduardo Alcaraz Chávez  
**Fecha:** Abril 2026

---

## Objetivo

Analizar cómo los medios de comunicación cubren temas complejos, identificar el impacto del algoritmo de búsqueda en la construcción de la opinión pública y evaluar el sesgo en la presentación de información sobre salud digital en distintos buscadores.

---

## Ejercicio A — Análisis de cobertura mediática: violencia y crimen organizado

### Metodología

Se seleccionaron diez artículos sobre el mismo evento (operativo policial en Michoacán, febrero 2026) publicados en medios con líneas editoriales distintas. Los artículos fueron analizados según:
- Encuadre principal (seguridad, derechos humanos, político, económico)
- Fuentes citadas (gubernamentales, víctimas, expertos, anónimas)
- Carga emocional del lenguaje
- Presencia de datos verificables vs. afirmaciones sin respaldo

### Resultados observados

| Tipo de medio | Encuadre dominante | Fuentes predominantes | Carga emocional |
|---|---|---|---|
| Medios gubernamentales | Seguridad/Logro | Institucionales | Neutral-positiva |
| Medios nacionales (Reforma, El Universal) | Político | Mixtas | Neutral-crítica |
| Medios locales (Michoacán) | Derechos humanos | Comunidad/víctimas | Alta (negativa) |
| Portales alternativos | Denuncia | Anónimas, testimonios | Muy alta |
| Agencias internacionales (Reuters, AP) | Informativo | Gubernamentales + expertos | Neutral |

### Análisis

El mismo evento generó narrativas radicalmente distintas según el medio. Los medios gubernamentales enfatizaron los logros del operativo y las detenciones; los medios locales documentaron los daños colaterales en comunidades civiles; las agencias internacionales priorizaron el dato verificable sobre la interpretación. Ningún medio ofreció una visión completa por sí solo.

La primera página de Google para búsquedas sobre el tema devolvió predominantemente medios con mayor tráfico web, no necesariamente los que ofrecían la cobertura más rigurosa. Los medios locales con mayor proximidad al evento aparecieron en posiciones muy alejadas del primer resultado, a pesar de contener información primaria más detallada.

---

## Ejercicio B — Comparación de motores de búsqueda sobre tema de vigilancia

### Consulta realizada

`"vigilancia masiva" "derechos digitales" México 2025`

### Resultados comparados

**Google:**
- Primeros 5 resultados: medios digitales de alto tráfico (Animal Político, Expansión, Milenio).
- Predomina encuadre noticioso con énfasis en declaraciones políticas.
- Ninguna organización de derechos digitales en primera página.

**DuckDuckGo:**
- Primeros 5 resultados: Article 19 México, R3D (Red en Defensa de los Derechos Digitales), EFF.
- Predomina encuadre de derechos civiles con análisis técnico-jurídico.
- Mayor diversidad de perspectivas ideológicas.

**Ecosia:**
- Resultados similares a DuckDuckGo con inclusión de fuentes académicas de FLACSO y UNAM.
- Menor presencia de medios comerciales de alto tráfico.

### Interpretación

La diferencia en los resultados refleja distintos modelos de ranking. Google, al priorizar señales de autoridad basadas en backlinks y tráfico, eleva medios de comunicación masivos que cubren el tema superficialmente. DuckDuckGo, al no personalizar ni rastrear el historial, devuelve resultados más consistentes entre usuarios, pero no necesariamente más completos. La elección del motor de búsqueda influye directamente en la construcción de la imagen del tema que el usuario forma.

---

## Ejercicio C — Sesgo algorítmico en búsquedas sobre salud

### Consulta base

`vacunas efectividad COVID México`

### Variables modificadas

Se realizaron variantes de la consulta para medir el impacto en los resultados:
- Con y sin sesión de Google iniciada.
- Desde ubicaciones simuladas (Ciudad de México vs. zona rural de Guerrero).
- Con diferentes historiales de navegación previos.

### Hallazgos

1. **Personalización geográfica:** La misma consulta desde una IP asociada a zona rural devolvió dos resultados más de medios no verificados que desde una IP urbana, donde Google priorizó fuentes de la SSA y la OPS.

2. **Personalización por historial:** Un perfil con historial de búsquedas de medicina alternativa recibió en los primeros tres resultados páginas que cuestionaban la efectividad de las vacunas, frente a un perfil sin historial que recibió únicamente fuentes gubernamentales y científicas.

3. **Impacto de la formulación:** La consulta `"vacunas COVID" efectos secundarios` generó un primer resultado sobre eventos adversos raros, mientras que `vacunas COVID seguridad` devolvió resultados sobre estudios de eficacia.

### Consecuencias observadas

El algoritmo amplifica el sesgo de confirmación preexistente del usuario. Un usuario que previamente buscó información antivacunas recibirá más información en esa dirección, mientras que uno sin historial relevante recibirá información de consenso científico. Esto tiene implicaciones directas en la toma de decisiones de salud pública.

---

## Reflexión transversal: algoritmos como editores de la realidad

Los tres ejercicios confluyen en una conclusión común: los algoritmos de búsqueda y de contenido actúan como editores invisibles que determinan qué perspectivas se vuelven visibles y cuáles permanecen marginadas. A diferencia de un editor humano explícito, el algoritmo no declara su perspectiva ni su sesgo, lo que lo hace más difícil de cuestionar críticamente.

La alfabetización informacional en el siglo XXI requiere no solo saber leer críticamente un texto, sino comprender las reglas del sistema que decidió que ese texto llegara a nuestros ojos en primer lugar. La recuperación de información responsable implica resistir activamente la inercia del primer resultado y triangular siempre múltiples fuentes y plataformas.

---

## Conclusión general

Los tres ejercicios demuestran que la objetividad de la búsqueda de información es una ilusión operativa útil pero inexacta. Todo sistema de recuperación tiene sesgos estructurales derivados de su diseño, sus incentivos económicos y los datos con los que fue construido. Reconocer este hecho no debe llevar al escepticismo paralizante, sino a prácticas de búsqueda más deliberadas, diversas y críticas.
