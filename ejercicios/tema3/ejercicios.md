# Ejercicios Prácticos Tema 3 - Unidad 2, Sesión 1
## Fundamentos de Prompt Engineering

---

## Ejercicio 1: Anatomía de un Prompt

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de teoría sobre componentes del prompt

### Contexto
Antes de crear buenos prompts, es importante reconocer los componentes en prompts existentes.

### Objetivo de Aprendizaje
- Identificar los componentes de un prompt (rol, contexto, tarea, formato, restricciones)
- Evaluar la completitud de un prompt

### Enunciado
Analiza los siguientes prompts e identifica sus componentes. Indica qué componentes faltan y como los mejorarías.

### Prompt A
```
Eres un experto en marketing digital especializado en startups tecnológicas.

Contexto: Nuestra startup vende software de gestión de proyectos para equipos remotos.
Acabamos de lanzar una nueva funcionalidad de videoconferencias integradas.

Tarea: Escribe 3 posts para LinkedIn anunciando esta funcionalidad.

Formato:
- Cada post debe tener entre 100-150 palabras
- Incluir un emoji relevante al inicio
- Terminar con un call-to-action

No menciones competidores ni uses jerga demasiado técnica.
```

### Prompt B
```
Dame ideas para mejorar mi aplicación
```

### Prompt C
```
Traduce este texto al inglés y hazlo más formal:

"""
Hola! Queria saber si podemos quedar mañana para hablar del proyecto.
Avisame cuando puedas.
"""
```

### Tabla de Análisis

Completa la siguiente tabla para cada prompt:

| Componente | Prompt A | Prompt B | Prompt C |
|------------|----------|----------|----------|
| Rol | Experto en marketing digital especializado en startups tecnológicas | No especificado | Traductor/Corrector de estilo |
| Contexto | Muy detallado: startup de gestión de proyectos, lanzamiento de nueva funcionalidad | Inexistente: no se sabe qué tipo de app | Mínimo: solo el texto a traducir, sin contexto sobre la audiencia |
| Tarea | Clara y específica: escribir 3 posts anunciando la funcionalidad | Vaga y general: "ideas para mejorar" | Clara pero limitada: traducir y hacer formal |
| Formato | Muy bien definido: 100-150 palabras, emoji al inicio, CTA al final | No existe especificación de formato | No se especifica formato de salida |
| Restricciones | Claras: no mencionar competidores, evitar jerga técnica | Ninguna restricción | Ninguna restricción explícita |
| Ejemplos | No incluye ejemplos de posts anteriores | No aplica | No incluye ejemplos de traducción formal |
| **Evaluación (1-10)** | **8/10** - Muy completo y bien estructurado | **2/10** - Extremadamente vago y genérico | **5/10** - Básico pero funcional, falta contexto |

### Preguntas de Reflexión
1. **¿Cuál de los tres prompts producirá mejores resultados? ¿Por qué?**
   
   El Prompt A produciría los mejores resultados porque:
   - Define claramente el rol esperado (experto especializado)
   - Proporciona contexto abundante y específico
   - Especifica exactamente el formato de salida deseado
   - Incluye restricciones claras que evitarán contenido no deseado
   - La tarea es concreta y medible (3 posts con rangos de palabras específicos)

2. **¿Qué añadirias al Prompt B para hacerlo efectivo?**
   
   El Prompt B necesita:
   - **Rol**: "Eres un experto en UX/desarrollo de software"
   - **Contexto**: Tipo de aplicación (mobile/web), sector, audiencia objetivo, problemas actuales
   - **Tarea específica**: "Identifica 5 mejoras prioritarias"
   - **Formato**: "Presenta cada idea con: descripción, impacto estimado, complejidad"
   - **Restricciones**: "Enfócate en funcionalidades viables en 2-3 sprints"
   - **Ejemplos**: Mostrar el tipo de ideas que buscamos

3. **¿El Prompt C necesita rol? ¿Por qué si o por qué no?**
   
   No estrictamente necesario, pero sí recomendable porque:
   - **SÍ necesita rol si**: Queremos que traduzca manteniendo cierto tono empresarial específico
   - **NO necesita si**: Es una tarea mecánica de traducción estándar
   - **Mejora potencial**: Especificar "Traduce como si fuera para un email profesional a un cliente" añadiría valor al resultado

---

## Ejercicio 2: Zero-shot vs Few-shot

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Experimentación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Acceso a ChatGPT, Claude o Gemini

### Contexto
Comparar el rendimiento de diferentes técnicas de prompting en una tarea de clasificación.

### Objetivo de Aprendizaje
- Experimentar con zero-shot y few-shot prompting
- Comparar resultados y entender cuándo usar cada técnica

### Enunciado
Vas a clasificar sentimientos de reseñas de productos usando tres enfoques diferentes.

### Parte A: Zero-shot (10 min)

Usa el siguiente prompt con 5 reseñas de prueba:

```
Clasifica el sentimiento de la siguiente reseña como: Positivo, Negativo o Neutro.

Reseña: "[INSERTAR RESEÑA]"

Sentimiento:
```

**Reseñas de prueba:**
1. "Excelente producto, superó mis expectativas. Lo recomiendo totalmente."
2. "No funciona como esperaba. Devolución solicitada."
3. "Esta bien para el precio. Hace lo que promete, nada más."
4. "Llegó rápido pero la caja estaba dañada. El producto funciona correctamente."
5. "HORRIBLE. Peor compra de mi vida. NO COMPREN."

**Resultados Zero-shot obtenidos:**

| Reseña # | Texto | Resultado Zero-shot | Razonamiento |
|----------|-------|---------------------|--------------|
| 1 | "Excelente producto, superó mis expectativas. Lo recomiendo totalmente." | **Positivo** | Palabras clave positivas: "Excelente", "superó expectativas", "recomiendo" |
| 2 | "No funciona como esperaba. Devolución solicitada." | **Negativo** | Palabras clave negativas: "No funciona", "no esperaba", "devolución" |
| 3 | "Esta bien para el precio. Hace lo que promete, nada más." | **Neutro** | Expresión neutral: "bien", "como se describe", sin entusiasmo ni crítica |
| 4 | "Llegó rápido pero la caja estaba dañada. El producto funciona correctamente." | **Positivo/Mixto** | Sentimientos conflictivos: negativo en empaque, positivo en producto. El modelo tiende a lo positivo (producto funciona) |
| 5 | "HORRIBLE. Peor compra de mi vida. NO COMPREN." | **Negativo** | Palabras extremadamente negativas: "HORRIBLE", "peor", "NO COMPREN" en mayúsculas |

**Observación:** El zero-shot produce resultados razonables pero con ambigüedad en casos mixtos (reseña 4), donde el modelo debe elegir entre sentimientos conflictivos sin contexto adicional.

### Parte B: Few-shot (15 min)

Crea un prompt few-shot con 3 ejemplos (uno por categoría) y pruebalo con las mismas reseñas:

```
Clasifica el sentimiento de reseñas de productos.

Ejemplos:
Reseña: "Producto fantástico, excelente relación calidad-precio. Superó expectativas."
Sentimiento: Positivo

Reseña: "Defectuoso, no funciona y el servicio al cliente no responde. Muy insatisfecho."
Sentimiento: Negativo

Reseña: "Funciona como se describe. Nada especial, pero cumple su propósito."
Sentimiento: Neutro

Ahora clasifica:
Reseña: "[RESEÑA DE PRUEBA]"
Sentimiento:
```

### Parte C: Comparación (5 min)

Completa la tabla:

| Reseña | Zero-shot | Few-shot | ¿Coinciden? |
|--------|-----------|----------|-------------|
| 1 | Positivo | Positivo | Sí |
| 2 | Negativo | Negativo | Sí |
| 3 | Neutro | Neutro | Sí |
| 4 | Mixto/Positivo* | Positivo | Sí* |
| 5 | Negativo | Negativo | Sí |

*La reseña 4 contiene sentimientos mixtos (negativo sobre el empaque, positivo sobre el producto)

### Preguntas
1. **¿Hubo diferencias en los resultados? ¿Cuáles?**
   
   Diferencias observadas:
   - **Reseña 4**: El zero-shot podría mostrar ambigüedad al detectar sentimientos mixtos, mientras que el few-shot tiende a un resultado más definido (generalmente positivo por el sentimiento del producto)
   - **Claridad**: El few-shot produce respuestas más consistentes y predecibles
   - **Confianza**: El few-shot reduce la variabilidad entre ejecuciones

2. **¿La reseña 4 fue difícil de clasificar? ¿Por qué?**
   
   Sí, la reseña 4 presenta un desafío porque:
   - Contiene **sentimientos mixtos/conflictivos**: negatividad sobre la caja, positividad sobre el producto
   - La mayoría de sistemas tenderán a clasificarla como el sentimiento dominante (Positivo, porque el producto funciona)
   - Sin contexto adicional, es ambiguo cuál aspecto importa más al usuario
   - **Solución mejorada**: Añadir una opción "Mixto" en clasificaciones futuras

3. **¿Qué técnica usarias en producción? ¿Por qué?**
   
   **Recomendación: Few-shot**
   
   Razones:
   - Mayor **consistencia y predecibilidad** en resultados
   - Mejor **desempeño en casos ambiguos** como la reseña 4
   - Menores **variaciones entre llamadas** (reproducibilidad)
   - Mejor **claridad de expectativas** para el modelo
   - Trade-off: Token cost ligeramente mayor vs. mejor calidad
   
   **Alternativa para escala**: Fine-tuning con datos etiquetados si el volumen justifica el costo

---

## Ejercicio 3: Desarrollo Iterativo de Prompts

### Metadata
- **Duración estimada**: 35 minutos
- **Tipo**: Programación/Iteración
- **Modalidad**: Parejas
- **Dificultad**: Intermedia
- **Prerequisitos**: Acceso a un LLM

### Contexto
El desarrollo iterativo es la clave del Prompt Engineering profesional. Vamos a practicar el ciclo completo.

### Objetivo de Aprendizaje
- Aplicar el proceso iterativo de mejora de prompts
- Documentar cambios y su impacto

### Enunciado
Desarrolla un prompt para generar descripciones de productos para e-commerce.

### Escenario
Trabajas en una tienda online de electrónica. Necesitas un prompt que genere descripciones de productos atractivas y consistentes.

**Producto de prueba:**
```
Nombre: EchoBuds Pro X3
Tipo: Auriculares inalambricos
Precio: 149.99€
Características:
- Cancelación de ruido activa
- 30 horas de bateria (con estuche)
- Resistentes al agua IPX5
- Bluetooth 5.3
- Incluye 3 tamaños de almohadillas
```

### Iteración 1: Prompt Básico

**Prompt:**
```
Escribe una descripción para este producto:

Nombre: EchoBuds Pro X3
Tipo: Auriculares inalambricos
Precio: 149.99€
Características:
- Cancelación de ruido activa
- 30 horas de bateria (con estuche)
- Resistentes al agua IPX5
- Bluetooth 5.3
- Incluye 3 tamaños de almohadillas
```

**Resultado esperado (simulado):**
> "Los EchoBuds Pro X3 son auriculares inalámbricos con cancelación de ruido activa. Tienen una duración de batería de 30 horas con el estuche. Son resistentes al agua IPX5 y tienen Bluetooth 5.3. El paquete incluye 3 tamaños diferentes de almohadillas."

**Problemas identificados:**
- Muy robótico y carente de emoción
- No destaca beneficios, solo lista características
- No crea urgencia de compra
- Sin call-to-action
- Lenguaje plano, poco marketing
- No enfatiza la propuesta de valor

### Iteración 2: Añadir Estructura

**Prompt mejorado:**
```
Eres un redactor de e-commerce especializado en electrónica. Tu objetivo es crear descripciones de productos que vendan.

Escribe una descripción de producto para esta categoría: Auriculares.

Producto:
Nombre: EchoBuds Pro X3
Precio: 149.99€
Características:
- Cancelación de ruido activa
- 30 horas de bateria (con estuche)
- Resistentes al agua IPX5
- Bluetooth 5.3
- Incluye 3 tamaños de almohadillas

Formato de salida:
- Gancho inicial (1 línea): Frase impactante que capte atención
- Cuerpo (4-5 líneas): Describe beneficios transformadores, no solo características
- Especificaciones técnicas (2 líneas): Detalles técnicos importantes
- CTA (1 línea): Llamada a la acción clara

Longitud total: 150-200 palabras
Tono: Profesional pero accesible, enfocado en beneficios del usuario
```

**Resultado esperado:**
> "Vive la música sin límites. Con los EchoBuds Pro X3, sumérgete en tu mundo de audio sin distracciones. La cancelación de ruido activa te aísla del caos externo, permitiéndote concentrarte, relajarte o simplemente disfrutar de tu contenido favorito sin interrupciones. 
> 
> Con 30 horas de autonomía (gracias al estuche de carga), estos auriculares acompañan cada momento de tu día. Tanto si trabajas desde la playa como si saltas en la lluvia, su certificación IPX5 los hace resistentes al agua. La conectividad Bluetooth 5.3 garantiza una conexión estable y rápida con cualquier dispositivo.
>
> Especificaciones clave: Cancelación de ruido activa | 30h batería | IPX5 resistentes al agua | Bluetooth 5.3 | 3 tamaños de almohadillas incluidas.
>
> Descubre la libertad del audio sin cables. Añade los EchoBuds Pro X3 a tu carrito hoy."

**Mejoras observadas:**
- Lenguaje más emocional y marketing-oriented
- Beneficios claros (concentración, relajación, libertad)
- Estructura clara y fácil de leer
- CTA explícita
- Mejor ratio características/beneficios

### Iteración 3: Añadir Contexto y Tono

**Prompt refinado:**
```
Eres un redactor de e-commerce experto en auriculares premium. Especialista en conectar características técnicas con beneficios reales para el usuario.

CONTEXTO DE LA MARCA:
- Tienda: TechSound Store
- Posicionamiento: Premium pero accesible, tecnología de vanguardia
- Audiencia: Profesionales, estudiantes y amantes de la música de 25-45 años

PRODUCTO A DESCRIBIR:
Nombre: EchoBuds Pro X3
Categoría: Auriculares inalámbricos premium
Precio: 149.99€

CARACTERÍSTICAS:
- Cancelación de ruido activa (ANC)
- Duración de batería: 30 horas (con estuche)
- Resistencia al agua: IPX5
- Bluetooth 5.3
- 3 tamaños de almohadillas para ajuste personalizado

INSTRUCCIONES:
1. Comienza con un gancho que destaque BENEFICIOS, no características
2. Desarrolla cómo cada característica resuelve un problema real del usuario
3. Agrupa características relacionadas en párrafos temáticos
4. Incluye lenguaje aspiracional pero realista

ESTRUCTURA REQUERIDA:
[Gancho impactante - 1 línea]

[Beneficio 1 - Enfoque en concentración/productividad con ANC]

[Beneficio 2 - Libertad y movilidad con batería extendida]

[Beneficio 3 - Durabilidad y fiabilidad con IPX5 + Bluetooth 5.3]

[Personalización con almohadillas]

[CTA final]

RESTRICCIONES:
- Máximo 220 palabras
- NO usar superlativos exagerados (evitar "el mejor", "perfecto")
- Enfatizar aspectos técnicos pero en contexto de beneficios
- Tono: Confiable, moderno, accesible (no elitista)
```

**Resultado esperado:**
> "Auriculares que se adaptan a tu mundo.
>
> La cancelación de ruido activa te devuelve el control. En cafés ruidosos, en transportes públicos o en espacios compartidos, desconecta el mundo exterior y reconecta con lo que importa: tu trabajo, tu música, tu concentración.
>
> 30 horas de libertad. Con el estuche de carga rápida, tienes autonomía de casi un mes entre recargas. Trabaja una jornada completa sin pensar en la batería. Viaja sin adapters adicionales. Vive sin límites de tiempo.
>
> Durabilidad para la vida real. Resistentes al agua IPX5 para salpicar agua o sudor. Bluetooth 5.3 garantiza conexiones estables incluso en ambientes con múltiples dispositivos. Diseñados para resistir.
>
> Tu comodidad, personalizada. Incluye 3 tamaños de almohadillas para ese ajuste perfecto que evita dolor tras horas de uso.
>
> Suena a libertad. Siénte la diferencia con TechSound Store. Descubre EchoBuds Pro X3."

**Mejoras clave:**
- Énfasis en beneficios emocionales y prácticos
- Párrafos temáticos claros
- Lenguaje menos hype, más honesto
- Referencia a la marca
- Mejor conexión con audiencia objetivo

### Iteración 4: Refinamiento Final

**Prompt final optimizado:**
```
Eres un redactor de e-commerce especializado en auriculares y audio portátil. Tu objetivo es crear descripciones que conviertan visitantes en compradores, balanceando marketing con transparencia.

CONTEXTO:
- Marca: TechSound Store (Premium, accesible, innovadora)
- Público objetivo: Profesionales y estudiantes 25-45 años que valoran calidad y funcionalidad
- Objetivo de conversión: Destacar relación precio-valor

PRODUCTO:
Nombre: EchoBuds Pro X3 | Precio: 149.99€

ESPECIFICACIONES TÉCNICAS:
- Cancelación de ruido activa (ANC)
- Batería: 30h (con estuche)
- Resistencia: IPX5
- Conectividad: Bluetooth 5.3
- Incluye: 3 tamaños de almohadillas

FORMATO Y TONALIDAD:
Estructura: Gancho → 3 Beneficios principales → Detalles de precisión → CTA
Tono: Profesional, inspirador, honesto (sin exagerar)
Longitud: 180-220 palabras
Audiencia: Personas ocupadas que buscan tecnología confiable

INSTRUCCIONES ESPECÍFICAS:
1. Abre con una pregunta o afirmación que resene con la audiencia
2. Cada párrafo debe conectar Una Característica con Un Beneficio Real
3. Sección técnica: Especificaciones en párrafo narrativo, no lista de puntos
4. Cierra con CTA específica (no genérico "compra ahora")
5. Palabras clave a incluir: "productividad", "libertad", "precisión", "inversión"

PALABRAS A EVITAR:
- "Mejor", "Perfecto", "Revolucionario"
- Jerga excesiva sin explicación
- Promesas no verificables

CTA RECOMENDADA:
Dirigida a tipo: "Profesionales que reclaman libertad en su equipamiento"
Tono: Empoderador, no presionador

EJEMPLOS DE GANCHO EFECTIVOS:
- "¿Cansado de sacrificar calidad de audio por comodidad?"
- "Auriculares diseñados para tu ritmo, no para el de otros"
- "Donde la tecnología se adapta a tu vida, no al revés"
```

**Resultado esperado (FINAL):**
> "¿Cansado de auriculares que prometen mucho y entregan poco? EchoBuds Pro X3 es la respuesta.
>
> Escucha sin interrupciones. La cancelación de ruido activa no solo reduce sonidos externos: te devuelve horas productivas. Enfócate en tu trabajo, en tu música, en ti. Cada sesión es tuya, sin distracciones.
>
> Libertad sin límites. 30 horas de autonomía significa que tus auriculares viajan contigo todo el mes. Olvídate de buscar enchufes. Olvídate de elegir entre movilidad y duración. Ambas son tuyas.
>
> Construidos para la realidad. Resistencia IPX5 contra lluvia, sudor y accidentes cotidianos. Bluetooth 5.3 te conecta de forma estable sin importar si estás en la oficina ruidosa o en la calle. Tecnología que simplemente funciona.
>
> Personalización que se nota. Tres tamaños de almohadillas incluidas aseguran que ese ajuste perfecto existe para tus oídos, no para unos oídos imaginarios.
>
> Por 149.99€, no es una compra. Es una inversión en tu comodidad. Únete a miles que ya viven la diferencia. 
>
> Ver detalles técnicos completos → Añadir a carrito"

### Entregable

**1. Resumen de los 4 prompts:**
- Iteración 1: Prompt minimalista → Resultado genérico
- Iteración 2: Estructura + rol → Mejor marketing, más organizado
- Iteración 3: Contexto + audiencia → Beneficios más claros, emocional
- Iteración 4: Optimización completa → Conversión oriented, balanceado

**2. Cambio con mayor impacto:**
El giro más significativo fue en la **Iteración 2**, cuando se añadió:
- Rol específico del LLM
- Formato estructurado de salida
- Enfoque en beneficios vs. características
- CTA explícita

Esto mejoró el output de forma más drástica que mejoras posteriores.

**3. Prompt final recomendado:**
Ver Iteración 4 completa. Equilibra especificidad sin rigidez excesiva.

---

## Ejercicio 4: Diseño de Prompts para Casos de Uso

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Diseño
- **Modalidad**: Grupal (3-4 personas)
- **Dificultad**: Intermedia
- **Prerequisitos**: Comprensión de componentes del prompt

### Contexto
En equipos, diseñaran prompts para casos de uso empresariales reales.

### Objetivo de Aprendizaje
- Aplicar los componentes del prompt a problemas reales
- Colaborar en el diseño y crítica de prompts

### Enunciado
Cada grupo recibira un caso de uso y deberá diseñar el prompt completo.

---

## Caso A: Generador de Emails de Seguimiento

### Prompt Diseñado

```
Eres un especialista en ventas B2B con 10 años de experiencia cerrando deals. 
Tu objetivo es generar emails de seguimiento post-demo personalizados que reabran 
conversaciones y cierren más oportunidades.

CONTEXTO DEL PROSPECTO:
- Nombre: [INSERTAR]
- Empresa: [INSERTAR]
- Cargo: [INSERTAR]
- Puntos discutidos en demo: [INSERTAR]
  (ej: integración con Salesforce, reportes en tiempo real, onboarding rápido)
- Objeciones mencionadas: [INSERTAR]
  (ej: "Necesitamos integración con X", "El precio es alto", "Quieren ver ROI")
- Siguiente paso acordado: [INSERTAR]
  (ej: "Enviar propuesta", "Llamada con CFO", "Prueba de 15 días")
- Tono de la demo: [INSERTAR]
  (ej: "Muy interesado", "Escéptico pero abierto", "Neutral")

INSTRUCCIONES DE REDACCIÓN:
1. Subject line: Intrigante pero específico (máx 60 caracteres)
2. Saludo personalizado con primer nombre del prospecto
3. Párrafo 1 (2-3 líneas): Referencia específica a UN punto clave de la demo
4. Párrafo 2: Dirección a objeción mencionada de forma empática
5. Párrafo 3 (2-3 líneas): Propuesta clara del siguiente paso
6. Firma: Nombre, cargo, teléfono directo
7. PS: Oferta pequeña o recurso útil

REQUISITOS DE TONO:
- Conversacional pero profesional
- Empático a las preocupaciones del prospecto
- Enfocado en beneficio del prospecto, no de nuestra empresa
- Sin hype, sin presión agresiva

RESTRICCIONES IMPORTANTES:
- NO mencionar a competencia
- NO exagerar promesas
- NO usar términos genéricos ("revolucionario", "disruptivo")
- Máximo 250 palabras (body)
- Incluir UN dato o estadística relevante si aplica

OUTPUT ESPERADO:
Salida estructurada en 3 secciones claramente etiquetadas:
[SUBJECT LINE]
[CUERPO DEL EMAIL]
[FIRMA + PS]
```

### Justificación de Decisiones

- **Rol específico**: "Especialista en ventas B2B con 10 años" → Establece credibilidad y experiencia, el LLM entiende qué tipo de lenguaje usar
- **Contexto detallado**: Campos de input específicos → Asegura personalización real, no superficial
- **Formato estructurado**: Apartados claros (Subject, Body, Firma) → Salida reproducible y lista para copiar-pegar
- **Restricciones claras**: Qué NO hacer → Evita promesas falsas o lenguaje de spam
- **Limitación de palabras**: 250 max → Respeta el hecho de que emails largos no se leen en ventas

### Limitaciones Identificadas

- **Edge case**: Objeciones muy técnicas que requieren soluciones customizadas (el email podría no capturar complejidad)
- **Mejora futura**: Incluir template de propuesta adjunta o link a casos de éxito similares
- **Variación**: El mismo prompt podría necesitar ajustes si el prospecto es empresa Fortune 500 vs startup

---

## Caso B: Resumidor de Reuniones

### Prompt Diseñado

```
Eres un asistente ejecutivo experto en sintetizar reuniones complejas en documentos 
accionables. Tu objetivo es convertir transcripciones largas en resúmenes que ejecutivos 
ocupados puedan escanear en 2 minutos y actuar inmediatamente.

INPUT:
- Transcripción completa de la reunión: [INSERTAR]
- Duración de la reunión: [INSERTAR] minutos
- Lista de participantes con cargos: [INSERTAR]
- Contexto previo (si aplica): [INSERTAR]

ESTRUCTURA DE SALIDA OBLIGATORIA (En este orden exacto):

1. RESUMEN EJECUTIVO
   - Máximo 4 oraciones
   - Responde: ¿Qué se decidió? ¿Por qué? ¿Cuál es el impacto?
   - Dirigido a alguien que NO estuvo en la reunión

2. DECISIONES TOMADAS
   - Formato: Viñetas con decisión clara
   - Incluir: Quién la propuso, quién está a favor/en contra
   - Ejemplo: "Retrasar lanzamiento Q3 a Q4 (Propuesto por Producto, CFO de acuerdo, Ventas pidió semana más)"

3. ACTION ITEMS
   - Formato: Tabla: Tarea | Responsable | Fecha límite | Prioridad (Alta/Media/Baja)
   - SOLO tareas explícitas mencionadas o claramente inferidas
   - Ejemplo:
     | Obtener presupuesto de provedor A | Juan García (Ops) | 15 feb | Alta |

4. TEMAS PENDIENTES
   - Decisiones pospuestas o sin resolver
   - Puntos de fricción identificados
   - Información faltante que necesitan para decidir
   - Ejemplo: "Falta confirmación de disponibilidad del Team A para Q4"

NOTAS IMPORTANTES:
- Usa nombres REALES de participantes, no "el presentador dijo"
- Si hay conflicto entre participantes, documéntalo (ej: "Juan quería X, María insistía en Y")
- Errores/problemas mencionados → incluir en Temas Pendientes
- Solo incluir lo que fue HABLADO, no lo que debería haberse hablado

FORMATO PROHIBIDO:
- NO resumen narrativo largo
- NO paráfrasis genéricas
- NO incluir divagaciones o comentarios fuera de tema
```

### Justificación de Decisiones

- **Rol especializado**: "Asistente ejecutivo experto" → Entiende la necesidad de concisión y accionabilidad
- **Estructura OBLIGATORIA**: 4 secciones claras → Cada ejecutivo sabe dónde buscar qué
- **Formato específico**: Viñetas, tablas, emojis (✓) → Escaneable, no narrativo
- **Inclusión de conflictos**: Documentar desacuerdos → Información crucial que resúmenes planos ocultan
- **Limitación a lo hablado**: No especular → Mantiene documento como fuente de verdad

### Limitaciones Identificadas

- **Problema**: Transcripciones mal formatadas o con oradores no etiquetados
- **Edge case**: Reuniones con múltiples conversaciones paralelas simultáneas (¿cuál documentar?)
- **Mejora futura**: Especificar si hay dudas sobre quién es responsable de qué item
- **Variación por sector**: Financiero vs Producto vs Ingeniería podrían necesitar fields adicionales

---

## Caso C: Revisor de Código Automatizado

### Prompt Diseñado

```
Eres un Senior Code Reviewer con 15 años de experiencia en [LENGUAJE]. 
Tu objetivo es identificar issues reales que impacten calidad, seguridad o mantenibilidad. 
NO eres un linter automático; eres un reviewer humano experto.

CONTEXTO:
- Lenguaje de programación: [INSERTAR]
- Proyecto/Repositorio: [INSERTAR]
- Tipo de cambio: [Bug fix / Feature / Refactor / Otros]
- Archivo(s) modificado(s): [INSERTAR NOMBRES]
- Estándares del equipo (si aplica): [INSERTAR]
  (Ej: "Máximo 3 niveles de indentación", "Usar async/await no callbacks")

INPUT - CÓDIGO A REVISAR:
[INSERTAR DIFF O CÓDIGO COMPLETO]

INSTRUCCIONES DE REVISIÓN:

1. IDENTIFICAR ISSUES
   - Severidad: CRÍTICO (falla en prod) | MAYOR (bug/seguridad) | MENOR (estilo/mantenibilidad)
   - Para cada issue, proporciona:
     a) Línea del código
     b) Qué está mal (be specific, no "malo")
     c) Por qué es un problema
     d) Sugerencia de corrección
     e) Código corregido (si aplica)

2. ANALIZAR COMPLEJIDAD
   - ¿Es el código más complejo de lo necesario?
   - ¿Hay duplicación de código?
   - ¿Falta documentación en lógica no obvia?

3. VALIDAR PATRONES
   - ¿Sigue los estándares del equipo?
   - ¿Es consistente con el resto de la base de código?
   - ¿Usa las librerías/frameworks de forma apropiada?

4. CONSIDERACIONES DE TESTING
   - ¿El cambio necesita casos de test?
   - ¿Qué casos edge podrían romper esto?

OUTPUT REQUERIDO:

## RESUMEN EJECUTIVO
- Issue count: X críticos, Y mayores, Z menores
- Recomendación: Aprobar | Cambios menores | Rechazar

## ISSUES ENCONTRADOS
[Para cada issue]
**[ID] - SEVERIDAD**
- Línea: [XX]
- Problema: [descripción concisa]
- Impacto: [por qué importa]
- Sugerencia: [qué cambiar]
- Código sugerido:
  \`\`\`[lenguaje]
  [código corregido]
  \`\`\`

## FORTALEZAS ENCONTRADAS
- [Si hay patrones buenos a destacar]

## OBSERVACIONES GENERALES
- [Tendencias, patrones a mejorar en futuro]

RESTRICCIONES:
- NO reportar issues de linting puro (trailing spaces, indentación de 2 vs 4 espacios)
- NO sugerir refactoring masivo a menos que bloquee el merge
- SÍ enfocarte en: lógica, seguridad, performance, mantenibilidad
- NO asumir que el autor es junior; ofrece feedback adulto
```

### Justificación de Decisiones

- **Rol senior específico**: Define expectativa de análisis profundo, no superficial
- **Severidades claras**: CRÍTICO/MAYOR/MENOR → Prioriza qué arreglar primero
- **Contexto lingüístico**: El lenguaje cambia cómo revisar (Go vs Python vs JS) → crucial
- **Output estructurado**: Resumen + detalle + fortalezas → Constructivo, no solo crítica
- **Exclusión de linting**: Los linters ya existen, el valor del LLM es analysis lógico
- **Sugerencias de código**: No solo "esto está mal", sino "así se arregla" → accionable

### Limitaciones Identificadas

- **Límite de tokens**: Código muy largo podría no entrar en contexto
- **Edge case**: Cambios en infraestructura o DevOps (terraform, k8s) necesitan reviewer diferente
- **Problema**: Dependencias externas no incluidas (el reviewer no ve si la lib que usas tiene vulnerabilidades)
- **Mejora futura**: Integración con SonarQube o similar para análisis automático primero, LLM de segunda pasada

---

## Ejercicio 5: Identificación de Anti-patrones

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis/Corrección
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de sección de anti-patrones

### Contexto
Identificar y corregir prompts problemáticos es una habilidad esencial.

### Objetivo de Aprendizaje
- Reconocer anti-patrones comunes en prompts
- Proponer correcciones efectivas

### Enunciado
Para cada prompt problemático, identifica el anti-patrón y proporciona una versión corregida.

### Prompt 1
```
Necesito que me ayudes con algo de código que no funciona bien y que tiene
algunos errores que no se cuales son pero que hacen que no funcione como
debería y necesito que lo arregles y también que me expliques que estaba
mal y que me des algunas sugerencias de mejora y que sea rápido porque
tengo prisa.
```

**Anti-patrón identificado:** Falta de claridad, ambigüedad total, múltiples peticiones en una, lenguaje coloquial excesivo, expectativas de velocidad imposibles

**Versión corregida:**
```
Eres un experto en debugging de Python. Necesito ayuda urgente.

CÓDIGO CON ERROR:
[Pega aquí el código completo]

CONTEXTO:
- Lenguaje: Python 3.9
- Framework: Flask
- Qué intenta hacer: [Describe el objetivo en 1 oración]
- Qué error ves: [Copia el mensaje de error exacto]
- Cuándo falla: [¿En qué circunstancia específica?]

AYUDA NECESARIA (en este orden):
1. ¿Cuál es la causa raíz del error?
2. Código corregido (solo la sección afectada)
3. 2-3 sugerencias de refactoring para evitar esto en futuro

Formato: Secciones claras, código en bloques [```]
```

**Cambios aplicados:**
- Rol específico (Python + debugging)
- Estructura clara: contexto + error + peticiones en orden de prioridad
- Input estructurado en campos
- Expectativa realista de tiempo

---

### Prompt 2
```
Escribe un artículo muy detallado pero breve sobre inteligencia artificial.
```

**Anti-patrón identificado:** Contradicción directa (detallado ↔ breve), audiencia indefinida, scope infinito (IA es enorme), sin contexto de uso

**Versión corregida:**
```
Eres un periodista científico que explica temas complejos para público general.

ESCRIBE UN ARTÍCULO sobre Inteligencia Artificial.

ESPECIFICACIONES:
- Audiencia: Ejecutivos no técnicos (CEO, CFO, directores)
- Longitud: 800-1000 palabras
- Propósito: Entender qué es IA, cómo impacta negocio, dónde invertir
- Nivel de detalle técnico: Bajo (evita fórmulas, explica conceptos)

ESTRUCTURA REQUERIDA:
1. Gancho (1 párrafo): Por qué debe importar ahora
2. ¿Qué es la IA? (2 párrafos): Definición simple + ejemplos reales
3. Impacto en negocios (2 párrafos): Oportunidades + riesgos
4. Dónde invertir (2 párrafos): Sectores emergentes + red flags
5. Conclusion (1 párrafo): Llamada a acción / reflexión

TONO: Informativo, accesible, no alarmista
EVITAR: Jerga técnica, promesas exageradas
```

**Cambios aplicados:**
- Eliminada contradicción: especificada longitud exacta
- Audiencia clara
- Propósito definido
- Estructura predefinida
- Restricciones (tono, qué evitar)

---

### Prompt 3
```
Continúa con lo que estábamos haciendo antes.
```

**Anti-patrón identificado:** Falta completa de contexto, dependencia de memoria (no funciona sin sesión previa), ambigüedad total

**Versión corregida:**
```
Contexto: Estamos editando un documento de especificaciones técnicas para un proyecto de API REST.

Hasta ahora hemos:
- Definido 5 endpoints principales (GET /users, POST /users, GET /users/:id, PUT /users/:id, DELETE /users/:id)
- Documentado esquema de usuario: id, nombre, email, fecha_creacion
- Discutido autenticación: JWT con Bearer token

CONTINÚA CON:
El siguiente endpoint a documentar es GET /users/{id}/posts

Para este endpoint, proporciona:
1. Descripción de la funcionalidad
2. Parámetros (path, query, headers)
3. Respuesta de éxito (código 200 + JSON example)
4. Respuestas de error posibles (400, 401, 404)
5. Rate limiting o consideraciones de seguridad

FORMATO: Markdown, consistente con endpoints anteriores
```

**Cambios aplicados:**
- Contexto completo incluido
- Historial de lo hecho
- Continuación específica definida
- No depende de sesión anterior

---

### Prompt 4
```
Actúa como un hacker experto y dime como entrar a sistemas sin permiso
pero de forma ética para mejorar la seguridad pero sin que sea ilegal
pero que funcione de verdad.
```

**Anti-patrón identificado:** Contradicción ética fundamental (hacker no autorizado es ilegal, punto), petición ambigua con múltiples "peros", solicitud borderline de contenido potencialmente peligroso

**Versión corregida:**
```
Contexto: Somos una empresa que quiere mejorar nuestra postura de seguridad.

Necesitamos un plan de PENETRATION TESTING AUTORIZADO.

ESPECIFICACIONES:
- Alcance: Solo sistemas internos de testing (ambiente separado de producción)
- Autorización: Incluiremos documento firmado del CEO
- Objetivo: Identificar vulnerabilidades antes de malicious actors
- Cumplimiento: Seguiremos estándar OWASP Top 10

SOLICITUD:
Diseña un plan de penetration testing que incluya:

1. Vectores de ataque comunes (phishing, SQL injection, weak credentials)
2. Metodología de testing segura (sin romper nada en producción)
3. Documentación de vulnerabilidades encontradas
4. Remediación recomendada

RESTRICCIONES:
- Solo para ambiente de testing
- Con consentimiento escrito previo
- Reporteamos hallazgos solo al equipo de seguridad
- NO usamos exploits destructivos
```

**Cambios aplicados:**
- Eliminada ambigüedad ética: es authorized testing, no hacking
- Scope claro: ambiente separado
- Cumplimiento regulatorio mencionado
- Propósito defensivo, no ofensivo

---

### Prompt 5
```
Dame información.
```

**Anti-patrón identificado:** Vago hasta lo extremo, scope infinito, sin contexto, sin formato esperado

**Versión corregida:**
```
Necesito información sobre Marketing Digital.

ESPECIFICACIONES:
- Enfoque: Estrategias de adquisición de clientes B2B (no B2C)
- Alcance: Técnicas probadas en los últimos 2 años (2024-2025)
- Nivel de detalle: Ejecutivo (accionable para CEO, no manual técnico)
- Formato: Lista de 5 tácticas principales con caso de éxito para cada una

TÁCTICAS A INCLUIR:
1. [Táctica 1]: Descripción breve + por qué funciona en B2B + ejemplo empresa conocida
2. [Táctica 2]: ...
3. [Táctica 3]: ...
4. [Táctica 4]: ...
5. [Táctica 5]: ...

PARA CADA TÁCTICA:
- Inversión requerida (bajo/medio/alto)
- Tiempo a resultados (semanas/meses)
- ROI típico
- Errores comunes a evitar

CONTEXTO ADICIONAL:
- Industria: SaaS
- Tamaño de empresa: Series A startups
- Presupuesto anual: $50-100k

TONO: Profesional, conciso, data-driven
```

**Cambios aplicados:**
- Tema específico: Marketing Digital → Marketing Digital B2B
- Scope definido: 5 tácticas (no infinito)
- Formato estructurado: viñetas + criterios específicos
- Contexto de aplicación: SaaS, Series A
- Formato de respuesta clara

---

### Tabla Resumen

| # | Anti-patrón | Solución Aplicada |
|---|-------------|-------------------|
| 1 | Ambigüedad total + múltiples peticiones confusas | Estructura clara con campos específicos y prioridades ordenadas |
| 2 | Contradicción directa (detallado ↔ breve) | Especificar longitud exacta (800-1000 palabras) + público objetivo |
| 3 | Falta completa de contexto + dependencia de memoria | Incluir contexto completo + historial de trabajo previo |
| 4 | Ambigüedad ética + contradicciones morales | Especificar que es authorized testing, no hacking ilegal |
| 5 | Vaguedad extrema sin scope | Tema → audiencia → formato → contexto → tono |

---

## Ejercicio Extra: Prompt para tu Trabajo

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Aplicación Práctica
- **Modalidad**: Individual
- **Dificultad**: Avanzada

### Enunciado
Identifica una tarea repetitiva de tu trabajo o estudios qué podría beneficiarse de un LLM. Diseña un prompt completo siguiendo todo lo aprendido.