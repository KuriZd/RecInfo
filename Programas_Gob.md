# Programas de Gobierno Relacionados con Información, Datos y Digitalización

**Zamudio Damián Oscar Kuricaveri — 22120729**  
**Recuperación de Información | ITM Morelia — 2026**

---

## 1. Contexto: el Estado como productor y regulador de información

Los gobiernos son actores fundamentales en el ecosistema de la información por tres razones simultáneas: producen enormes volúmenes de datos públicos (estadísticas, registros, normatividad), regulan cómo la información puede circular (leyes de protección de datos, transparencia) y financian infraestructura para su acceso (portales de datos abiertos, plataformas de identidad digital).

---

## 2. México: Programas nacionales relevantes

### 2.1 Datos Abiertos del Gobierno Federal (datos.gob.mx)

Plataforma que centraliza datasets publicados por dependencias federales en formatos abiertos (CSV, JSON, XML). Permite a investigadores, desarrolladores y ciudadanos acceder a información oficial de forma estandarizada.

**Tipos de datos disponibles:**
- Estadísticas del INEGI (demografía, economía, TIC)
- Datos de salud (SSA, IMSS)
- Información geográfica (INEGI)
- Contratos de gobierno (CompraNet)
- Registros educativos (SEP)

**Relevancia para recuperación de información:** Estos datasets pueden ser consumidos mediante APIs REST y procesados con pandas y requests en Python, constituyendo fuentes primarias para investigación en minería de datos.

### 2.2 CURP Biométrica

El gobierno mexicano implementó gradualmente la CURP Biométrica, que integra huellas digitales, iris y rostro al registro de identidad nacional. A partir de 2026, es el documento oficial para trámites que requieren verificación de identidad.

**Debates asociados:**
- Voluntariedad vs. obligatoriedad en la recolección biométrica.
- Protección de datos conforme al artículo 16 constitucional y la Ley Federal de Protección de Datos Personales.
- Riesgo de uso secundario de la base biométrica sin consentimiento informado.

### 2.3 Plataforma Llave MX

Sistema de identidad digital del gobierno federal para autenticación de ciudadanos en trámites en línea. Genera debate público por la recolección de datos biométricos y la centralización de información personal en una sola plataforma gubernamental.

---

## 3. Unión Europea: marcos regulatorios de referencia

### 3.1 Reglamento General de Protección de Datos (GDPR)

El GDPR establece derechos fundamentales de los ciudadanos europeos sobre sus datos personales:

| Derecho | Descripción |
|---|---|
| Acceso | Conocer qué datos se tienen sobre el ciudadano |
| Rectificación | Corregir datos inexactos |
| Supresión ("derecho al olvido") | Eliminar datos cuando ya no son necesarios |
| Portabilidad | Obtener los datos en formato estructurado |
| Oposición | Negarse a ciertos tipos de procesamiento |

**Impacto en recuperación de información:** Los sistemas que indexan información personal (motores de búsqueda, bases de datos) deben cumplir con mecanismos de eliminación de información cuando un ciudadano ejerce el derecho al olvido.

### 3.2 Digital Services Act (DSA)

Regulación que exige a plataformas con más de 45 millones de usuarios europeos:
- Transparencia sobre sus algoritmos de recomendación.
- Mecanismos de denuncia de contenido ilegal.
- Auditorías de riesgo sistémico (incluyendo efectos en salud mental).
- Opciones para desactivar la personalización algorítmica.

**Relevancia:** El DSA es el primer marco legal que requiere explícitamente que las plataformas rindan cuentas sobre sus sistemas de recuperación y recomendación de contenido.

### 3.3 European Digital Identity (EUDI) Wallet

Reglamento (UE) 2024/1183 que exige a los Estados miembros ofrecer una cartera de identidad digital para finales de 2026. Permitirá a ciudadanos europeos autenticarse en servicios públicos y privados usando una app en el teléfono, con control granular sobre qué información comparten.

---

## 4. Iniciativas de transparencia y acceso a la información

### México — INAI

El Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales supervisa el cumplimiento de la Ley Federal de Transparencia y Acceso a la Información Pública. Cualquier ciudadano puede solicitar información a dependencias federales mediante la Plataforma Nacional de Transparencia (PNT).

### OGP — Open Government Partnership

Iniciativa multilateral donde los países miembros se comprometen a publicar planes de acción con compromisos concretos de gobierno abierto: datos abiertos, participación ciudadana y rendición de cuentas. México es miembro fundador.

---

## 5. Programas de conectividad e inclusión digital

| Programa | País | Objetivo |
|---|---|---|
| Internet para Todos | México | Conectar comunidades rurales sin acceso |
| UNICO – Bono Social | España | Subsidio de banda ancha para familias vulnerables |
| BConnect | Francia | Subsidio de 200€ para equipos a familias con bajos ingresos |
| FCC Affordable Connectivity | EE.UU. | Descuento mensual en servicios de internet |

---

## 6. Implicaciones para la investigación en recuperación de información

Los programas gubernamentales generan oportunidades concretas para proyectos académicos:

1. **APIs de datos abiertos** (INEGI, Banco de México) son fuentes de datos reales para análisis de series temporales y visualización.
2. **Registros de transparencia** pueden minarse para detectar patrones en el gasto público o en la frecuencia de solicitudes de información.
3. **Debates regulatorios** (GDPR, DSA) definen los límites éticos y legales de los sistemas de recuperación de información construidos por desarrolladores.
4. **Plataformas de identidad** crean desafíos de privacidad que requieren soluciones técnicas en anonimización y privacidad diferencial.

---

## 7. Conclusión

Los programas de gobierno relacionados con información y datos no son solo contexto político: son infraestructura sobre la que operan los sistemas de recuperación de información modernos. Entender el marco regulatorio (GDPR, DSA, Ley Federal de Transparencia), las fuentes de datos disponibles (datos.gob.mx, INEGI) y los debates sobre identidad digital y conectividad equipa a cualquier profesional de sistemas computacionales para diseñar soluciones técnicas responsables, legalmente conformes y socialmente pertinentes.
