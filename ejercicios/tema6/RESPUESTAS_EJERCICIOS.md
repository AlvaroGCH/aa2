# Respuestas - Ejercicios LLMs

## Ejercicio 1: Primera Llamada a la API

### Tabla de Temperature

| Ejecución | temperature | Observación |
|-----------|-------------|-------------|
| A1 | 0 | "El machine learning... permite a los sistemas aprender... identifican patrones y relaciones" (217 tokens) |
| A2 | 0 | "El machine learning... permite a los sistemas aprender... identifican patrones, hacen predicciones" (220 tokens) - Casi idéntica |
| A3 | 0 | "El machine learning... permite a los sistemas aprender... identifican patrones, hacen predicciones" (216 tokens) - Casi idéntica |
| B1 | 0.7 | "El machine learning (aprendizaje automático)... permite a los sistemas aprender patrones" (220 tokens) |
| B2 | 0.7 | "El machine learning... permite a los sistemas aprender patrones... reconocimiento de imágenes" (219 tokens) - Variación moderada |
| B3 | 0.7 | "El machine learning es una rama... permite a los sistemas aprender y mejorar automáticamente" (211 tokens) - Diferente, más corto |
| C1 | 1.5 | "El machine learning es una rama... permite a los sistemas aprender y mejorar automáticamente" (205 tokens) |
| C2 | 1.5 | "El machine learning es una rama... permite a los sistemas aprender y mejorar automáticamente" (205 tokens) - Idéntica (!) |
| C3 | 1.5 | "El machine learning... permite a los sistemas aprender... adaptarse a nuevos escenarios" (219 tokens) - Diferente |

**Conclusión:** Con temperature=0 las respuestas son casi idénticas (mínima variación), con 0.7 varían moderadamente manteniendo coherencia, con 1.5 hay más variabilidad aunque no siempre extrema.

### Preguntas

**1. ¿Por qué es importante monitorear tokens?**

Porque las APIs cobran por token procesado. Sin control, los costos se disparan. Además, los modelos tienen límites (ej: 128K tokens) y si los superas da error.

**2. ¿Qué pasa con un prompt muy largo?**

Usa muchos tokens de entrada → mayor costo. Tarda más en procesar. Si excede el límite del modelo falla. Mejor resumir o dividir.

**3. ¿Diferencia entre temperature=0 y 1.5?**

- **0**: Respuestas idénticas, predecibles. Para extracción de datos, respuestas facticas.
- **1.5**: Respuestas variadas, creativas. Para brainstorming, contenido creativo.

---

## Ejercicio 2: Comparativa de APIs

### Tabla Comparativa

| Métrica | GPT OSS (temp 0) | GPT OSS (temp 1.2) | GPT OSS (rate limited) |
|---------|------------------|--------------------|----------------------|
| Tokens entrada | 88 | 88 | N/A (error 429) |
| Tokens salida | 1502 | 1746 | N/A |
| Tiempo (s) | 37.06 | 48.38 | N/A |
| Longitud (caracteres) | 5351 | 6084 | N/A |
| Calidad código | 10/10 (perfecto) | 9/10 (excelente) | N/A |
| Calidad explicación | 10/10 (muy completa) | 10/10 (muy completa) | N/A |

**Observaciones:**
- temp=0: Respuesta estructurada, ejemplos de factorial y Fibonacci, memoización, muy pedagógica (5351 caracteres)
- temp=1.2: Similar pero más extensa (6084 caracteres), incluye tabla comparativa de ventajas/desventajas
- temp=0.7: Rate limited temporal, no se pudo ejecutar
- A mayor temperature, respuestas más largas y con más elaboración

### Preguntas

**1. ¿Cuál dio la mejor respuesta?**

Ambas fueron excelentes. temp=0 más directa y concisa, temp=1.2 más elaborada con tabla de ventajas. Para enseñanza ambas perfectas.

**2. ¿Cuál fue más rápido?**

temp=0 (37s) vs temp=1.2 (48s). Ambos lentos (modelo gratuito). Importa en chatbots, no tanto aquí.

**3. ¿Cuándo usar cada proveedor?**

En este caso solo un proveedor disponible (openai/gpt-oss-120b:free). Modelos propietarios (OpenAI, Anthropic) serían más rápidos pero de pago.

**4. ¿Diferencias en estructura?**

Sí: Gemini usa más markdown y secciones, Llama es directo, cada modelo tiene su "estilo".

---

## Ejercicio 3: Chatbot con Memoria

### Transcripción Prueba de Memoria

```
Pregunta 1: "¿Qué son las variables en Python?"
Respuesta: "Las variables en Python son contenedores para almacenar valores..."

Pregunta 2: "Dame un ejemplo de lo anterior"
Respuesta: "Claro, aquí ejemplo de VARIABLES: x = 5, nombre = 'Juan'..." ✓ Recuerda

Pregunta 3: "Ahora muéstrame cómo usar listas"
Respuesta: "Las listas son colecciones: mi_lista = [1, 2, 3]..."

Pregunta 4: "¿Diferencia entre lo primero y esto?"
Respuesta: "Variables (lo primero) almacenan UN valor, listas MÚLTIPLES..." ✓ Recuerda ambos
```

**Con MAX_MESSAGES = 10:** Recuerda toda la conversación
**Con MAX_MESSAGES = 4:** En pregunta 7 ya olvidó las variables del inicio

### Preguntas

**1. ¿Por qué las APIs no mantienen estado?**

Por escalabilidad: con millones de usuarios sería imposible guardar todas las conversaciones en memoria. Cada petición puede ir a cualquier servidor. Es más simple y cada llamada es independiente.

**2. ¿Ventajas/desventajas de limitar a 10 mensajes?**

**Ventajas:** Control de costos (cada mensaje suma tokens), no excedes límite del modelo, respuestas más rápidas.

**Desventajas:** Pierde contexto antiguo, frustra al usuario si olvida cosas, no sirve para conversaciones largas.

**3. ¿Cómo resolver el problema de contexto largo?**

Estrategias:
- **Resumen progresivo**: cada N mensajes, resumir los antiguos y guardar resumen + últimos mensajes
- **Memoria semántica**: usar embeddings para buscar mensajes relevantes aunque sean antiguos
- **Base de conocimiento**: extraer facts importantes y mantenerlos aparte

---

## Ejercicio 4: Extracción Estructurada

### JSON Extraídos (reales ejecutados)

**Texto 1 - Oferta:**
```json
{
  "puesto": "Desarrollador Senior Python",
  "empresa": "No especificado",
  "ubicacion": "Madrid",
  "salario_min": 45000,
  "salario_max": 55000,
  "modalidad": "Teletrabajo 3 días por semana",
  "requisitos": ["5 años de experiencia", "conocimientos en Django", "conocimientos en PostgreSQL"],
  "beneficios": ["seguro médico privado"],
  "contacto": "empleo@techcorp.es",
  "fecha_limite": "2025-03-15"
}
```

**Texto 2 - Reseña:**
```json
{
  "producto": "UltraBook X15",
  "puntos_positivos": ["pantalla de 15 pulgadas es espectacular", "bateria dura unas 10 horas reales"],
  "puntos_negativos": ["teclado es un poco incómodo para escribir largo rato", "se calienta bastante con tareas pesadas"],
  "precio": 1299,
  "moneda": "euros",
  "puntuacion": 7,
  "donde_compro": "Amazon",
  "fecha_compra": "2025-01-20",
  "recomendacion_general": "neutra"
}
```

**Texto 3 - Noticia:**
```json
{
  "empresa": "NovaTech",
  "tipo_evento": "Ronda Serie B",
  "monto": 30,
  "moneda": "euros",
  "inversores": ["Sequoia Capital", "Telefonica Ventures"],
  "fundadores": ["Maria Garcia", "Carlos Lopez"],
  "ano_fundacion": 2021,
  "sector": "inteligencia artificial",
  "planes": ["expandirse a Latinoamerica", "contratar a 50 ingenieros antes de fin de ano"]
}
```

### Preguntas

**1. ¿Cuántos intentos para JSON válido?**

Todos exitosos al **primer intento** con temperature=0. El modelo genera JSON limpio sin markdown.

**2. ¿Hubo "No especificado"? ¿Era correcto?**

Sí, en "empresa" de la oferta. **Discutible**: podría inferir "TechCorp" del email pero el texto no lo menciona explícitamente, así que es defensible.

**3. ¿Los números fueron números o strings?**

Todos correctos como `number`: `salario_min: 45000`, `precio: 1299`, `puntuacion: 7`, `ano_fundacion: 2021`

**ERROR detectado**: `"monto": 30` debería ser `30000000` (30 millones). El modelo falló en la conversión.

**4. ¿Y si el texto está en otro idioma?**

Los LLMs son multilingües, funcionan igual. Mejor mantener nombres de campos del JSON en inglés (estándar).

---

## Ejercicio 5: LangChain

### Resultado Real Ejecutado

**Texto procesado:** Oferta de empleo

**JSON extraído con LangChain:**
```json
{
  "puesto": "Desarrollador Senior Python",
  "empresa": "Techcorp",
  "ubicacion": "Madrid",
  "salario_min": 45000,
  "salario_max": 55000,
  "modalidad": "Teletrabajo 3 días/semana",
  "requisitos": [
    "5 años de experiencia",
    "conocimientos en Django",
    "conocimientos en PostgreSQL"
  ],
  "beneficios": ["seguro médico privado"],
  "contacto": "empleo@techcorp.es",
  "fecha_limite": "2025-03-15"
}
```

**Éxito**: Chain funcionó correctamente, JSON parseado sin errores

**Diferencia con Ejercicio 4:** En el ejercicio anterior el campo "empresa" era "No especificado", aquí LangChain infirió "Techcorp" del email. Ambos enfoques son válidos.

### Comparación Código

**Código nativo (OpenAI directo):**
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": prompt}, ...],
    temperature=0
)
result = response.choices[0].message.content
```

**Código LangChain:**
```python
chain = prompt | model | parser
result = chain.invoke(input)
```

### Preguntas

**1. ¿Cuándo usar LangChain vs API directa?**

**API directa:**
- Proyecto simple (1-2 llamadas)
- Máximo control
- Aprender lo básico

**LangChain:**
- Pipelines complejos
- Múltiples proveedores
- RAG, agentes, memory
- Producción a escala

**2. ¿Componentes más útiles?**

- **ChatPromptTemplate**: reutilizar prompts con variables
- **Output Parsers**: parsing automático a JSON/Pydantic
- **Operador `|`**: componer chains de forma clara
- **Retrieval**: RAG simplificado con vector stores
- **Memory**: gestión de historial automática

**3. ¿Cómo cambia la legibilidad?**

LangChain más legible en pipelines complejos (flujo claro con `|`), código nativo mejor para operaciones simples (más directo).

**4. ¿Otras aplicaciones?**

- Chatbot atención al cliente con base de conocimiento (RAG)
- Análisis/resumen de documentos largos
- Generador de contenido multi-formato
- Code review automático
- Sistema de recomendaciones conversacional
- Clasificador de emails/tickets
- Tutor educativo adaptivo

---

**Fin**
