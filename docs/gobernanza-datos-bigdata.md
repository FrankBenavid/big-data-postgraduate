# Guía general de gobernanza de datos en Big Data

[Índice del curso](../README.md) · [Pipelines y DataOps](pipelines-dataops.md) · [Panorama de herramientas](panorama-opensource-2026.md)

La gobernanza de datos establece quién puede decidir sobre los datos, con qué reglas y cómo se comprueba su cumplimiento. Su propósito es que los datos sirvan para decisiones confiables y usos autorizados durante todo su ciclo de vida. Esta guía conecta esas decisiones con el pipeline trabajado en clase. No sustituye la asesoría jurídica ni las políticas de una organización.

## 1. Estrategia y alcance

Antes de seleccionar una plataforma, formular el problema, los resultados esperados y los riesgos. Identificar dominios de datos, consumidores, fuentes y productos prioritarios. Acordar qué decisiones necesitan datos confiables, qué activos son críticos y quién financia y supervisa su gestión.

| Decisión estratégica | Pregunta orientadora | Evidencia |
|---|---|---|
| Objetivo | ¿Qué decisión o servicio se busca mejorar? | Caso de uso y responsable |
| Alcance | ¿Qué dominios, fuentes y productos incluye? | Inventario priorizado |
| Riesgo | ¿Qué daño causaría un error, acceso indebido o retraso? | Registro de riesgos |
| Medición | ¿Cómo sabremos si mejora? | Indicadores, metas y revisión |

## 2. Responsabilidades y decisiones

Un patrocinador asigna prioridades y recursos. El **propietario del dominio** decide usos y niveles de riesgo aceptables. El **administrador o steward** mantiene definiciones y reglas de calidad con expertos del negocio. El **responsable técnico** implementa controles, operación y recuperación. Seguridad, privacidad y cumplimiento asesoran y verifican. Los consumidores notifican errores y documentan necesidades. Una persona puede asumir varios papeles en equipos pequeños, pero cada decisión debe tener un responsable identificable.

El comité de gobernanza resuelve conflictos entre dominios, aprueba políticas y revisa excepciones. Registrar la decisión, responsable, fecha, justificación, vigencia y condición de revisión. Una excepción debe tener duración y controles compensatorios explícitos.

## 3. Inventario, catálogo y significado

El catálogo permite descubrir activos y comprenderlos antes de utilizarlos. Para cada conjunto o producto registrar:

- Nombre, descripción, propósito, propietario y contacto.
- Fuente, fecha de corte, cobertura, licencia y restricciones de uso.
- Unidad de observación, granularidad, esquema, tipos, unidades y valores ausentes.
- Clasificación de sensibilidad, reglas de acceso, retención y disponibilidad.
- Reglas de calidad, frecuencia de actualización, versión y limitaciones conocidas.
- Dependencias, transformaciones, destinos y enlaces a evidencias.

El **glosario** define términos de negocio; el **diccionario** describe campos concretos; el **catálogo** reúne y relaciona esos metadatos. El **linaje** muestra de dónde proviene un resultado y qué transformaciones lo produjeron. Un catálogo sin responsables ni mantenimiento pierde utilidad.

## 4. Contratos y calidad

Un contrato de datos acuerda productor, consumidor, estructura, significado, claves, unidades, frecuencia, reglas de calidad, tratamiento de errores y procedimiento de cambio. Diferenciar cambios compatibles de los que requieren coordinación con consumidores. Registrar la versión del contrato junto a cada ejecución.

| Dimensión | Pregunta | Ejemplo de control |
|---|---|---|
| Completitud | ¿Faltan valores necesarios? | Porcentaje de códigos territoriales presentes |
| Validez | ¿Cumplen el dominio acordado? | pH numérico en rango físico, conservando el original |
| Unicidad | ¿La clave representa una sola observación? | Conteo de duplicados por clave acordada |
| Consistencia | ¿Coinciden reglas y unidades entre fuentes? | Comprobar unidad, vigencia y cardinalidad del join |
| Oportunidad | ¿Llegó el corte cuando se necesitaba? | Edad del último corte frente al acuerdo |
| Trazabilidad | ¿Puede reproducirse la cifra? | Fuente, versión, reglas y registro de ejecución |

Los umbrales dependen del uso. Definir severidad, responsable y acción: aceptar, poner en cuarentena, detener o publicar con una advertencia. Registrar numerador, denominador y cobertura de cada indicador. Un control aprobado no demuestra que todos los datos sean correctos.

## 5. Seguridad, privacidad y uso responsable

Clasificar los datos por sensibilidad y riesgo; aplicar acceso mínimo necesario y revisar permisos periódicamente. Proteger credenciales con un gestor de secretos, cifrar según la política de la organización y registrar accesos y cambios. Separar ambientes y funciones sensibles. Definir respuesta ante incidentes, canales de reporte y responsabilidades.

Recoger y conservar solo lo necesario para el propósito autorizado. Evaluar riesgos de identificación, combinación de fuentes y publicación de grupos pequeños. La agregación o seudonimización por sí sola no garantiza anonimato. Revisar licencias, condiciones de uso y legislación aplicable con las áreas responsables. Los datos PQRS de salud requieren especial cuidado: un reporte no equivale a una persona y una muestra docente no autoriza publicar registros individuales.

## 6. Ciclo de vida y operación técnica

1. **Ingreso:** verificar origen, autorización, integridad y corte; conservar el original bajo acceso controlado.
2. **Preparación:** perfilar, aplicar contrato y documentar transformaciones, rechazados y cambios de esquema.
3. **Procesamiento:** versionar código y configuración; asociar entradas, ejecución y salidas. En sistemas distribuidos controlar particiones, reintentos y duplicados.
4. **Publicación:** validar calidad, conciliar totales y grupos, revisar permisos y aprobar la versión candidata.
5. **Uso y seguimiento:** ofrecer catálogo, soporte, métricas, auditoría y gestión de incidentes.
6. **Retención y eliminación:** definir plazos por tipo de dato, copias y obligaciones aplicables; comprobar la eliminación o disposición autorizada, incluyendo réplicas cuando corresponda.

En eventos, documentar tiempo de evento y de llegada, ventanas, tardanza, duplicados y recuperación de estado. En datos geográficos, registrar sistema de referencia, escala y vigencia. En modelos analíticos, documentar particiones temporales, posibles fugas y límites de uso.

## 7. Caso del curso: pipeline PQRS

| Etapa | Decisión de gobernanza | Control y evidencia |
|---|---|---|
| Fuente | Identificar corte y condiciones de uso | Manifiesto, fecha, archivo y huella |
| Perfil | Definir unidad: reporte, no persona | Esquema, nulos y cobertura documentados |
| Validación | Acordar campos y reglas | Registros aceptados y pendientes con motivo |
| Transformación | Definir período y territorio | Código y contrato versionados |
| Publicación | Autorizar detalle o agregado apropiado | Conciliación por grupo y total, revisión de acceso |
| Reejecución | Evitar duplicación y explicar cambios | Comparación de contenido y registro de ejecuciones |

Las muestras de clase permiten practicar controles en un portátil. No son necesariamente representativas de todos los reportes. Las reglas y umbrales didácticos deben revisarse antes de un uso institucional.

## 8. Herramientas y arquitectura

Las funciones de gobernanza pueden comenzar con archivos de manifiesto, diccionario y controles versionados. A mayor escala pueden incorporarse catálogo, gestión de políticas, linaje, observabilidad y auditoría centralizados. Ejemplos de productos incluyen Apache Atlas, OpenMetadata, DataHub, Microsoft Purview y catálogos gestionados de nube. Son alternativas con capacidades y costos diferentes; su adopción requiere evaluar integración, licencias, seguridad y operación. Una herramienta no asigna por sí sola responsables ni define políticas.

En producción pueden convivir almacenamiento de objetos, tablas con metadatos, motores distribuidos, orquestación y controles de acceso. La robustez debe responder a disponibilidad, volumen, concurrencia y riesgo, no al número de productos instalados. Consultar el [panorama del ecosistema](panorama-opensource-2026.md) y verificar versiones y condiciones vigentes antes de elegir.

## 9. Hoja de ruta y seguimiento

**Inicio:** seleccionar un producto prioritario, nombrar responsables, registrar fuentes y clasificar datos. **Piloto:** acordar contrato, controles, acceso y evidencia para un pipeline. **Extensión:** automatizar captura de metadatos, alertas y revisiones; aplicar el modelo a otros dominios. **Mejora:** analizar incidentes, excepciones y cambios de uso, y ajustar reglas con los consumidores.

Indicadores posibles: proporción de activos críticos con responsable y contrato, controles aprobados por corte, tiempo de resolución de incidentes, solicitudes de acceso atendidas y activos con linaje verificable. Cada indicador necesita definición, fuente, frecuencia, meta y responsable. Una meta se acuerda según el contexto, no se deduce de esta guía.

### Lista de comprobación para un producto

- [ ] Pregunta, consumidor, propietario y unidad de análisis definidos.
- [ ] Fuente, fecha, cobertura, licencia y clasificación documentadas.
- [ ] Contrato y reglas de calidad acordados, con tratamiento de fallos.
- [ ] Accesos, retención, privacidad y publicación revisados.
- [ ] Código, parámetros, linaje y evidencia de ejecución conservados.
- [ ] Resultado conciliado, limitaciones visibles y responsable de aprobación identificado.
- [ ] Incidentes, cambios y revisiones cuentan con un procedimiento.

## Referencias

- [NIST: definición de gobernanza de datos](https://csrc.nist.gov/glossary/term/data_governance).
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework).
- [Microsoft: estrategia de gobernanza](https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-governance) y [responsabilidades de propiedad y administración](https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-content-ownership-and-management).
- [Google Cloud: linaje de datos](https://docs.cloud.google.com/knowledge-catalog/docs/about-data-lineage).
- [Microsoft: principios de gobernanza de datos e IA](https://learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/data-governance/).
