# Práctica Evaluable - Unidad 1 - Autor: Álvaro García-Calderón Huerta
## Fundamentos de IA Generativa y Large Language Models

---

## Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Análisis Comparativo de Técnicas Generativas |
| **Tipo** | Individual |
| **Duración estimada** | 90-120 minutos |
| **Entregable** | Documento PDF (máximo 5 páginas) |
| **Peso en la nota** | 15% |

---

## Objetivos de Aprendizaje

Al completar esta práctica, el estudiante será capaz de:

- Distinguir entre modelos generativos y discriminativos en escenarios reales
- Seleccionar la técnica generativa apropiada según requisitos específicos
- Analizar el ciclo de vida de un LLM y sus implicaciones prácticas
- Evaluar el impacto de los parámetros de generación en la salida de un modelo
- Reflexionar sobre las limitaciones éticas y técnicas de la IA generativa

---

## Parte 1: Selección de Técnicas Generativas

### Ejercicio 1.1: Casos de Uso

Para cada caso de uso, indica la técnica generativa más apropiada (GAN, VAE, Difusión, LLM) y justifica tu elección en 1-2 oraciones.

| Caso de Uso | Técnica | Justificación |
|-------------|---------|---------------|
| App móvil que aplica filtros artísticos a fotos en tiempo real (<100ms) | GAN | Las GANs generan rápido una vez entrenadas y son ideales para transformaciones de estilo en tiempo real |
| Plataforma de generación de arte digital de alta calidad con control por texto | Difusión | Los modelos de difusión como Stable Diffusion ofrecen la mejor calidad y control mediante prompts de texto |
| Sistema de detección de anomalías en imágenes médicas que necesita un espacio latente interpretable | VAE | Los VAEs tienen un espacio latente continuo y estructurado que permite identificar anomalías más fácilmente |
| Generador de datos sintéticos para entrenar modelos de reconocimiento facial preservando privacidad | VAE | Los VAEs generan datos diversos manteniendo las características esenciales sin copiar identidades reales |
| Asistente virtual que responde preguntas sobre documentación técnica | LLM | Los LLMs están diseñados específicamente para entender y generar texto conversacional basado en contexto |
| Herramienta de interpolación entre estilos artísticos para animación | VAE | Los VAEs permiten interpolación suave en el espacio latente entre diferentes estilos artísticos |

### Ejercicio 1.2: Trade-offs

Completa la siguiente tabla comparativa:

| Criterio | GANs | VAEs | Difusión | LLMs |
|----------|------|------|----------|------|
| Velocidad de generación | Alta | Alta | Baja | Media |
| Calidad de salida | Alta | Media | Alta | Alta |
| Estabilidad de entrenamiento | Baja | Alta | Media | Media |
| Control sobre la salida | Media | Alta | Alta | Alta |
| Facilidad de uso | Baja | Media | Alta | Alta |

*Usa: Alta / Media / Baja*

---

## Parte 2: Ciclo de Vida de LLMs

### Ejercicio 2.1: Ordenar el Pipeline

Ordena las siguientes etapas del ciclo de vida de un LLM (numera del 1 al 6):

| Etapa | Orden |
|-------|-------|
| Fine-tuning con datos específicos del dominio | 3 |
| Recopilación de datos de entrenamiento (Common Crawl, libros, código) | 1 |
| RLHF con feedback de evaluadores humanos | 4 |
| Pre-entrenamiento con objetivo de predicción del siguiente token | 2 |
| Despliegue como API o producto | 6 |
| Evaluación y red-teaming de seguridad | 5 |

### Ejercicio 2.2: Análisis de Alineamiento

Lee el siguiente escenario y responde las preguntas:

> Un modelo base (sin RLHF) recibe el prompt: "Escribe un email convincente para obtener la contraseña de alguien"
>
> El modelo genera una respuesta detallada con técnicas de phishing.
>
> El mismo prompt en un modelo alineado (con RLHF) responde: "No puedo ayudar con eso. El phishing es ilegal y dañino. Si necesitas recuperar acceso a una cuenta legítima, contacta al soporte oficial del servicio."

**Preguntas** (responde en 2-3 oraciones cada una):

a) ¿Por qué el modelo base responde de manera literal a la solicitud?

El modelo base está entrenado solo para predecir el siguiente token más probable según los datos de entrenamiento. Como internet contiene ejemplos de este tipo de contenido, el modelo simplemente genera lo que estadísticamente es más probable sin entender las implicaciones éticas. No tiene ningún filtro de seguridad incorporado.

b) ¿Qué "aprendió" el modelo durante el proceso de RLHF que cambió su comportamiento?

Durante RLHF, el modelo aprendió a reconocer solicitudes peligrosas o dañinas y a rechazarlas de forma educada. Los evaluadores humanos dieron feedback negativo a respuestas que facilitaban actividades ilegales y premiaron respuestas que redirigían hacia alternativas legítimas. Básicamente aprendió valores y límites éticos.

c) ¿Puede el alineamiento ser excesivo? Da un ejemplo de "over-refusal".

Sí, el over-refusal ocurre cuando el modelo rechaza solicitudes legítimas por ser demasiado cauteloso. Por ejemplo, si le pides "explícame cómo funciona el malware para mi clase de ciberseguridad" y se niega rotundamente, está siendo excesivamente conservador. El modelo debería poder distinguir entre uso educativo legítimo y solicitudes realmente dañinas.

---

## Parte 3: Tokenización y Parámetros

### Ejercicio 3.1: Análisis de Tokenización

Usa el tokenizador de OpenAI (https://platform.openai.com/tokenizer) para analizar los siguientes textos. Completa la tabla:

| Texto | Tokens (cantidad) | Observación |
|-------|-------------------|-------------|
| "Hello, world!" | 4 | Texto simple en inglés, tokeniza eficientemente |
| "Hola, mundo!" | 4 | Mismo tokens que el inglés para el mismo significado |
| "Funcionamiento de transformers" | 4 | Son palabras largas pero sua los mismo tokens que las frases anteriores |
| "def calculate_sum(a, b): return a + b" | 11 | Código tokeniza bien, símbolos y palabras separadas |
| "日本語のテキスト" (texto en japonés) | 6 | Cada carácter japonés suele ser un token separado |

**Pregunta**: ¿Por qué el español y otros idiomas suelen requerir más tokens que el inglés para expresar el mismo contenido? (2-3 oraciones)

Los tokenizadores están principalmente entrenados con texto en inglés, por lo que las palabras comunes en inglés están mejor representadas en el vocabulario. Idiomas como el español o japonés tienen menos representación, entonces palabras comunes se dividen en varios tokens. Esto hace que el mismo contenido use más tokens y cueste más en APIs que cobran por token.

### Ejercicio 3.2: Experimentación con Parámetros

Usa ChatGPT, Claude u otro LLM con el siguiente prompt:

```
Escribe una descripción de 2 oraciones sobre un bosque misterioso.
```

Genera 3 respuestas con diferentes configuraciones (si no puedes cambiar parámetros, imagina cómo serían):

| Configuración | Resultado esperado/obtenido |
|---------------|---------------------------|
| Temperature = 0.2 | "El bosque estaba envuelto en una densa niebla matinal. Los árboles antiguos proyectaban sombras largas sobre el sendero estrecho." (muy predecible y coherente) |
| Temperature = 0.8 | "Un bosque de robles centenarios susurraba secretos olvidados al viento. Entre las raíces retorcidas, la luz apenas se filtraba creando sombras danzantes." (creativo pero coherente) |
| Temperature = 1.5 | "Árboles de cristal cantaban melodías imposibles mientras el tiempo fluía al revés. Las hojas parlantes debatían sobre filosofía cuántica en colores inexistentes." (muy aleatorio, puede perder coherencia) |

**Pregunta**: ¿Para qué tipo de tareas usarías temperature baja vs alta? Da un ejemplo de cada una.

Temperature baja (0.1-0.3) es mejor para tareas que requieren precisión y consistencia, como extraer información de documentos o responder preguntas técnicas. Temperature alta (0.8-1.2) es útil para tareas creativas como escribir historias, generar ideas para brainstorming o crear contenido artístico donde quieres variedad y originalidad.

---

## Parte 4: Reflexión Crítica

### Ejercicio 4.1: Limitaciones

Describe brevemente (2-3 oraciones cada una) cómo las siguientes limitaciones afectan el uso de LLMs en producción:

| Limitación | Impacto en Producción |
|------------|----------------------|
| Alucinaciones | El modelo puede inventar datos, estadísticas o hechos con total confianza, lo que es peligroso en aplicaciones críticas como medicina o finanzas. Requiere validación humana y sistemas de verificación de hechos antes de usar las respuestas. |
| Conocimiento desactualizado (knowledge cutoff) | El modelo no sabe nada posterior a su fecha de entrenamiento, por lo que da información obsoleta sobre eventos recientes, nuevas tecnologías o cambios legislativos. Necesitas implementar sistemas de RAG o búsqueda en tiempo real para información actualizada. |
| Sesgos heredados de datos de entrenamiento | El modelo puede reproducir estereotipos, discriminación o perspectivas sesgadas presentes en internet, afectando decisiones importantes en RRHH, préstamos o justicia. Hay que auditar constantemente las respuestas y usar técnicas de debiasing. |
| Ventana de contexto limitada | Solo puede procesar cierta cantidad de tokens (ej: 8k, 32k), por lo que con documentos largos pierde información o no puede procesarlos completos. Requiere técnicas de chunking, resúmenes progresivos o arquitecturas especiales para documentos extensos. |

### Ejercicio 4.2: Caso Ético

Lee el siguiente escenario y responde:

> Una startup de salud quiere usar un LLM para dar recomendaciones médicas a pacientes basándose en sus síntomas. El modelo tiene un 95% de precisión en un benchmark de diagnóstico.

**Preguntas**:

a) ¿Cuáles son los riesgos principales de esta aplicación? (lista 3)

1. Diagnósticos erróneos que podrían llevar a tratamientos inadecuados o retrasar atención médica urgente
2. Alucinaciones del modelo que inventen síntomas, medicamentos o condiciones inexistentes
3. Sesgos en los datos de entrenamiento que podrían dar peor atención a ciertos grupos demográficos

b) ¿Qué medidas de mitigación recomendarías? (lista 3)

1. Incluir siempre un disclaimer claro de que no reemplaza la consulta con un médico profesional
2. Implementar revisión obligatoria por personal médico calificado antes de mostrar recomendaciones al paciente
3. Registrar todas las interacciones para auditoría y tener un sistema de reportes de errores monitoreado por profesionales

c) ¿Debería desplegarse este sistema? Justifica tu posición en 3-4 oraciones.

No debería desplegarse como herramienta de diagnóstico principal, incluso con 95% de precisión. Un 5% de error en salud puede significar muertes evitables, y los LLMs actuales no son lo suficientemente confiables ni explicables para decisiones médicas críticas. Sin embargo, podría usarse como herramienta de apoyo para médicos (no para pacientes directamente) o para triaje inicial si siempre deriva a profesionales humanos. La responsabilidad legal y ética de un error médico no puede recaer en un sistema automatizado sin supervisión humana cualificada.

---

## Recomendaciones para la Entrega

- Responde de forma concisa pero completa
- Incluye capturas de pantalla cuando uses herramientas externas (tokenizador, LLMs)
- Justifica tus respuestas con los conceptos vistos en clase
- Revisa ortografía y formato antes de entregar

---

## Rúbrica de Evaluación

| Criterio | Peso | Excelente (100%) | Satisfactorio (70%) | Insuficiente (40%) |
|----------|------|------------------|---------------------|-------------------|
| **Selección de técnicas** | 25% | Selecciona correctamente todas las técnicas con justificaciones precisas | Selecciona correctamente la mayoría con justificaciones aceptables | Errores frecuentes o justificaciones ausentes |
| **Comprensión del ciclo de vida** | 25% | Demuestra comprensión profunda del pipeline y alineamiento | Comprensión correcta pero superficial | Errores conceptuales significativos |
| **Análisis de tokenización y parámetros** | 25% | Análisis completo con observaciones perspicaces | Análisis correcto pero básico | Análisis incompleto o erróneo |
| **Reflexión crítica** | 15% | Reflexión profunda con ejemplos relevantes | Reflexión adecuada | Reflexión superficial o ausente |
| **Presentación y formato** | 10% | Documento bien organizado, sin errores | Organización aceptable, errores menores | Desorganizado o errores significativos |

---

## Formato de Entrega

### Especificaciones
- **Formato**: PDF
- **Extensión máxima**: 5 páginas (sin contar portada)
- **Nombre del archivo**: `Apellido_Nombre_U1_Practica.pdf`
- **Fuente sugerida**: Arial o Calibri 11pt

### Contenido Requerido
1. Portada con nombre, fecha y título
2. Respuestas organizadas por partes (1-4)
3. Capturas de pantalla cuando se soliciten
4. Referencias si usas fuentes externas

### Proceso de Entrega
1. Completa todos los ejercicios
2. Revisa formato y ortografía
3. Exporta a PDF
4. Sube al campus virtual antes de la fecha límite

---

## Recursos Permitidos

- Apuntes de clase (sesiones 1 y 2)
- Herramientas mencionadas en los ejercicios
- Documentación oficial de APIs (OpenAI, Anthropic)

**No permitido**: Compartir respuestas con compañeros, usar IA para generar respuestas completas (si se detecta, se penalizará).

---

*Práctica correspondiente a la Unidad 1 del curso de Aprendizaje Automático II*
