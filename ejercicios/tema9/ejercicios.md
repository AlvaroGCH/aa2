# Ejercicios Prácticos - Unidad 5, Sesión 1
## Fundamentos de RAG: Embeddings, Vectores y Chunking

---

## Ejercicio 1: Análisis Conceptual de una Arquitectura RAG

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 5.1 sobre introducción a RAG y sus componentes principales

### Contexto
Retrieval-Augmented Generation (RAG) combina la capacidad generativa de los LLMs con la recuperación de información de fuentes externas para producir respuestas fundamentadas en datos reales. Antes de implementar un sistema RAG, es fundamental saber diseñar su arquitectura: elegir las fuentes de datos, la estrategia de chunking, el modelo de embeddings y la base de datos vectorial adecuada para cada caso de uso. Este ejercicio entrena la capacidad de tomar decisiones de diseño informadas.

### Objetivo de Aprendizaje
- Comprender los componentes fundamentales de un pipeline RAG
- Identificar las decisiones de diseño clave en cada etapa del pipeline
- Evaluar qué tecnologías y configuraciones son más adecuadas según el contexto
- Desarrollar pensamiento crítico sobre las limitaciones de RAG frente a fine-tuning

### Enunciado

Para cada uno de los siguientes escenarios empresariales, diseña la arquitectura RAG completando la tabla con las decisiones técnicas que tomarías. Justifica brevemente cada elección.

### Escenario A: Asistente Legal para un Despacho de Abogados

Un despacho de abogados con 15 años de actividad quiere un asistente que responda preguntas sobre jurisprudencia, legislación vigente y documentos internos (contratos, dictámenes). Los documentos incluyen PDFs escaneados, documentos Word y bases de datos de sentencias.

| Componente | Tu decisión | Justificación |
|------------|-------------|---------------|
| **Fuentes de datos** | PDFs escaneados y documentos Word internos, bases de datos de sentencias judiciales | Es la realidad de un despacho con años de historia, hay que trabajar con documentos heredados |
| **Preprocesamiento necesario** | OCR para PDFs escaneados, extracción de texto de Word con python-docx, limpieza de caracteres especiales | Los PDFs escaneados necesitan OCR para convertir imagen a texto, los Word necesitan parseo específico |
| **Estrategia de chunking** | Semantic chunking por párrafos legales, respetando estructura de artículos y cláusulas | Los documentos legales tienen estructura jerárquica clara que no se debe romper |
| **Tamaño de chunk recomendado** | 800-1000 tokens | Los textos legales son densos y necesitan contexto amplio para entender referencias cruzadas |
| **Modelo de embeddings** | Multilingual-E5-large (local) o modelo legal específico como Legal-BERT | Privacidad crítica, mejor modelo local. Legal-BERT está entrenado en lenguaje jurídico |
| **Base de datos vectorial** | Weaviate o Qdrant (self-hosted) | Datos confidenciales requieren solución on-premise, ambas opciones son robustas para producción |
| **Número de chunks a recuperar (top-k)** | 5-7 chunks | Documentos legales requieren contexto amplio, pero no saturar el LLM con demasiada info |
| **LLM para generación** | Claude Opus (API) o Llama 3 70B (local) | Claude es excelente en razonamiento legal. Si hay restricciones de privacidad, Llama 3 local |

### Escenario B: FAQ Inteligente para una Universidad

La universidad U-TAD quiere que los estudiantes puedan hacer preguntas sobre normativas académicas, planes de estudio, horarios, convocatorias de exámenes y servicios del campus. La información está en la web institucional, PDFs de normativa y documentos de Moodle.

| Componente | Tu decisión | Justificación |
|------------|-------------|---------------|
| **Fuentes de datos** | Web scraping de la web institucional, PDFs de normativa, exportación de contenidos de Moodle | Cubrir todas las fuentes donde está la información académica oficial |
| **Estrategia de chunking** | Chunking por pregunta-respuesta para FAQs, por sección para normativas | Las FAQs son unidades naturales, las normativas necesitan respetarse por artículos |
| **Modelo de embeddings** | text-embedding-3-small de OpenAI o all-MiniLM-L6-v2 | No hay datos sensibles, se puede usar API. Es un caso de uso estándar sin jerga específica |
| **Base de datos vectorial** | ChromaDB o Pinecone (tier gratuito) | Volumen moderado de datos, no requiere infraestructura compleja. ChromaDB para prototipo rápido |
| **LLM para generación** | GPT-4o-mini o Claude Haiku | Consultas simples y directas, no requieren el modelo más potente. Haiku es rápido y económico |

### Escenario C: Soporte Técnico para Documentación de Software

Una empresa SaaS con documentación técnica extensa (API reference, tutoriales, guías de migración, changelogs) quiere un chatbot que responda consultas técnicas de desarrolladores. La documentación se actualiza semanalmente.

| Componente | Tu decisión | Justificación |
|------------|-------------|---------------|
| **Fuentes de datos** | Markdown/HTML de documentación, archivos OpenAPI/Swagger, repositorio Git de changelogs | La doc técnica suele estar en estos formatos, fáciles de parsear y mantener sincronizados |
| **Estrategia de chunking** | Chunking por sección de documentación, endpoints API como unidades independientes | Cada endpoint o concepto técnico debe ser una unidad recuperable completa |
| **Frecuencia de reindexación** | Automática con webhook en cada commit a main | Actualización semanal requiere pipeline CI/CD que reindexe automáticamente |
| **Modelo de embeddings** | text-embedding-3-small o code-search-ada-002 | code-search-ada está optimizado para queries técnicas y snippets de código |
| **Base de datos vectorial** | Pinecone o Weaviate | Necesita escalabilidad y búsqueda híbrida (vectorial + keyword) para nombres exactos de funciones |
| **Estrategia de búsqueda** | Híbrida: vectorial para conceptos + keyword para nombres exactos de funciones/clases | Los devs buscan tanto conceptos ("cómo autenticar") como términos exactos ("función authenticateUser") |

### Preguntas de Reflexión

1. **RAG vs. Fine-tuning**: En el Escenario A, el despacho se plantea si sería mejor hacer fine-tuning de un modelo con todos sus documentos en lugar de usar RAG. ¿Qué le recomendarías y por qué? Considera aspectos como actualización de datos, alucinaciones, coste y trazabilidad de las respuestas.

   **Respuesta**: Recomendaría RAG antes que fine-tuning por varias razones. Primero, en el ámbito legal cada caso nuevo o sentencia reciente puede cambiar interpretaciones, y con RAG basta actualizar la base de datos vectorial, mientras que fine-tuning requeriría reentrenar el modelo (costoso en tiempo y recursos). Segundo, RAG permite trazabilidad: puedes mostrar exactamente qué documentos se usaron para cada respuesta, algo crítico en derecho. Tercero, el fine-tuning no elimina las alucinaciones, solo las hace más específicas al dominio legal, mientras que RAG ancla las respuestas en documentos reales. Finalmente, el coste: fine-tuning de calidad requiere miles de ejemplos y GPUs potentes, RAG solo necesita embeddings (mucho más barato). Fine-tuning sería complementario si quisieras que el modelo entienda mejor jerga legal específica, pero como estrategia principal RAG es superior.

2. **Privacidad**: El Escenario A maneja documentos legales confidenciales. ¿Cómo afecta esto a la elección de modelo de embeddings y LLM? ¿Usarías APIs en la nube o modelos locales?

   **Respuesta**: La privacidad es crítica aquí. Usaría modelos locales (on-premise) para ambos componentes. Para embeddings: modelos como Multilingual-E5-large o sentence-transformers que se pueden ejecutar localmente sin enviar datos fuera. Para LLM: Llama 3 70B o Mixtral 8x7B ejecutados en servidores propios del despacho. Si el presupuesto es limitado, podría considerar APIs en la nube solo si hay un contrato BAA (Business Associate Agreement) que garantice cumplimiento GDPR y que los datos no se usen para entrenamiento. Pero la opción más segura y recomendable es siempre mantener todo on-premise cuando hay datos legales confidenciales de clientes.

3. **Escalabilidad**: Si el Escenario C pasa de 1.000 a 100.000 documentos, ¿qué componentes de tu arquitectura necesitarían cambiar?

   **Respuesta**: Varios componentes necesitarían ajustarse. Primero, la base de datos vectorial: si empecé con ChromaDB (embebida), tendría que migrar a Pinecone, Weaviate o Qdrant en modo cluster para distribuir la carga. Segundo, el pipeline de indexación: necesitaría paralelización (procesamiento por lotes con workers concurrentes) y un sistema de cola (como RabbitMQ o Redis) para gestionar las actualizaciones. Tercero, la estrategia de chunking podría necesitar optimización para reducir el número total de chunks (quizás chunks más grandes o semantic chunking más agresivo). Cuarto, consideraría añadir un layer de caché (Redis) para queries frecuentes. Finalmente, el número top-k posiblemente debería ajustarse con reranking: recuperar 20-30 chunks candidatos, aplicar un reranker y seleccionar los mejores 5-7 para el LLM.

---

## Ejercicio 2: Experimentación con Embeddings y Similitud Semántica

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Lectura de la sección 5.2 sobre embeddings y espacios vectoriales, conocimientos básicos de Python y numpy

### Contexto
Los embeddings son representaciones numéricas densas de texto que capturan su significado semántico. La calidad de un sistema RAG depende directamente de la calidad de sus embeddings: si frases con significado similar no producen vectores cercanos, la recuperación fallará. Este ejercicio permite experimentar de primera mano con embeddings, entender la similitud coseno y descubrir tanto las capacidades como las limitaciones de estos modelos.

### Objetivo de Aprendizaje
- Generar embeddings usando la API de OpenAI o sentence-transformers
- Calcular e interpretar la similitud coseno entre vectores
- Identificar patrones: sinonimia, paráfrasis, negación, cambio de idioma
- Comprender las limitaciones de los embeddings para ciertos tipos de relaciones semánticas

### Enunciado

Escribe un programa en Python que genere embeddings para un conjunto de frases y analice las relaciones semánticas entre ellas mediante similitud coseno.

### Paso 1: Configuración del entorno

Elige **una** de las dos opciones:

**Opción A: OpenAI API** (requiere API key)
```python
from openai import OpenAI
import numpy as np

client = OpenAI()  # Usa OPENAI_API_KEY del entorno

def get_embedding(text, model="text-embedding-3-small"):
    """Genera el embedding de un texto usando OpenAI."""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return np.array(response.data[0].embedding)
```

**Opción B: Sentence-Transformers** (local, gratuito)
```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text, model=model):
    """Genera el embedding de un texto usando sentence-transformers."""
    return model.encode(text)
```

### Paso 2: Definir las frases de prueba

Usa el siguiente conjunto de frases diseñado para explorar diferentes relaciones semánticas:

```python
frases = {
    # Grupo 1: Frases semánticamente similares (paráfrasis)
    "A1": "El gato se sentó en la alfombra",
    "A2": "Un felino descansaba sobre el tapete",
    "A3": "The cat sat on the mat",  # Misma idea, otro idioma

    # Grupo 2: Frases sobre tecnología
    "B1": "Python es un lenguaje de programación muy popular",
    "B2": "JavaScript se usa mucho para desarrollo web",
    "B3": "Los lenguajes de programación son herramientas esenciales",

    # Grupo 3: Negación y contraste
    "C1": "El restaurante tiene buena comida",
    "C2": "El restaurante no tiene buena comida",
    "C3": "La comida del restaurante es terrible",

    # Grupo 4: Frases sin relación
    "D1": "La fotosíntesis convierte luz solar en energía",
    "D2": "El precio del petróleo subió un 5% ayer",
}
```

### Paso 3: Generar embeddings y calcular similitudes

```python
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    """Calcula la similitud coseno entre dos vectores."""
    return dot(a, b) / (norm(a) * norm(b))

# Generar embeddings para todas las frases
embeddings = {}
for key, frase in frases.items():
    embeddings[key] = get_embedding(frase)
    print(f"[{key}] Embedding generado - dimensiones: {len(embeddings[key])}")

# Calcular matriz de similitudes
print("\n--- MATRIZ DE SIMILITUD COSENO ---\n")
keys = list(frases.keys())
print(f"{'':>4}", end="")
for k in keys:
    print(f"{k:>8}", end="")
print()

for i, ki in enumerate(keys):
    print(f"{ki:>4}", end="")
    for j, kj in enumerate(keys):
        sim = cosine_similarity(embeddings[ki], embeddings[kj])
        print(f"{sim:>8.3f}", end="")
    print()
```

### Paso 4: Análisis de resultados

Responde a las siguientes preguntas basándote en los resultados obtenidos:

| Pregunta | Tu respuesta |
|----------|-------------|
| 1. ¿Cuál es la similitud entre A1 y A2 (paráfrasis en español)? ¿Es alta? | Con all-MiniLM-L6-v2 suele estar entre 0.65-0.75. Es alta pero no máxima porque "felino" y "gato", "alfombra" y "tapete" son sinónimos que el modelo captura bien pero no perfectamente |
| 2. ¿Cuál es la similitud entre A1 y A3 (misma idea, diferente idioma)? ¿Es comparable a A1-A2? | Con modelos multilingües como all-MiniLM-L6-v2 está entre 0.55-0.70, ligeramente más baja que A1-A2. Los modelos capturan semántica cross-lingual pero no tan bien como intra-idioma. Con modelos no multilingües sería mucho más baja (0.2-0.3) |
| 3. ¿Los embeddings de B1, B2 y B3 forman un grupo coherente? ¿Son más similares entre sí que con otros grupos? | Sí, forman un grupo coherente con similitudes entre 0.50-0.65 entre ellos. Son claramente más similares entre sí que con grupos A, C o D porque comparten el dominio semántico de "tecnología/programación" |
| 4. ¿Cuál es la similitud entre C1 ("buena comida") y C2 ("no tiene buena comida")? ¿Es sorprendentemente alta o baja? | Sorprendentemente alta, típicamente 0.75-0.85. Esto es una limitación conocida: los embeddings capturan tokens y contexto pero la negación es difícil de representar |
| 5. ¿Los embeddings capturan bien la negación? Compara C1-C2 vs C1-C3. ¿Cuál debería ser más diferente semánticamente? | No capturan bien la negación. C2 ("no tiene buena comida") tiene similitud alta con C1 (~0.80), mientras que C3 ("terrible") tiene similitud media-baja (~0.50-0.60). Semánticamente C2 debería ser más diferente de C1, pero los embeddings fallan aquí porque comparten muchos tokens |
| 6. ¿Las frases D1 y D2 tienen baja similitud con el resto de grupos, como esperarías? | Sí, típicamente <0.30 con otros grupos. D1 (fotosíntesis) y D2 (petróleo) no comparten dominio semántico con gatos, programación o restaurantes, por lo que quedan bien separadas |
| 7. ¿Cuál es la dimensionalidad de los embeddings generados? ¿Qué modelo usaste? | Con all-MiniLM-L6-v2: 384 dimensiones. Con text-embedding-3-small: 1536 dimensiones. Con text-embedding-3-large: 3072 dimensiones. Los modelos más grandes capturan más matices pero son más costosos de almacenar |

### Paso 5 (Bonus): Visualización

Si tienes tiempo, añade una visualización 2D usando PCA o t-SNE:

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Reducir a 2D
vectors = np.array(list(embeddings.values()))
pca = PCA(n_components=2)
coords = pca.fit_transform(vectors)

# Graficar
plt.figure(figsize=(10, 8))
colors = {'A': 'red', 'B': 'blue', 'C': 'green', 'D': 'orange'}
for i, key in enumerate(keys):
    grupo = key[0]
    plt.scatter(coords[i, 0], coords[i, 1], c=colors[grupo], s=100, zorder=5)
    plt.annotate(f"{key}: {frases[key][:30]}...",
                 (coords[i, 0], coords[i, 1]),
                 fontsize=8, ha='left', va='bottom')

plt.title("Embeddings proyectados en 2D (PCA)")
plt.xlabel("Componente 1")
plt.ylabel("Componente 2")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("embeddings_2d.png", dpi=150)
plt.show()
```

### Extensión (Opcional)

- Compara los resultados usando `text-embedding-3-small` vs `text-embedding-3-large` de OpenAI. ¿El modelo más grande captura mejor la negación?
- Añade frases en un tercer idioma (francés, alemán) y observa si se agrupan con sus equivalentes semánticos
- Experimenta con el parámetro `dimensions` de OpenAI para reducir la dimensionalidad del embedding y observa cómo afecta a las similitudes

---

## Ejercicio 3: Comparativa de Bases de Datos Vectoriales

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Exploración/Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 5.3 sobre bases de datos vectoriales

### Contexto
La elección de la base de datos vectorial es una de las decisiones arquitectónicas más importantes en un sistema RAG. No existe una opción universalmente mejor: la elección depende de factores como el volumen de datos, la necesidad de persistencia, el presupuesto, si se requiere búsqueda híbrida (vectorial + texto) y el nivel de experiencia del equipo. Este ejercicio te prepara para tomar esta decisión de forma informada en proyectos reales.

### Objetivo de Aprendizaje
- Conocer las principales bases de datos vectoriales del mercado
- Comparar sus características técnicas, modelos de pricing y casos de uso
- Evaluar qué solución es más adecuada según diferentes escenarios
- Distinguir entre soluciones locales, cloud-native y bases de datos tradicionales con extensiones vectoriales

### Enunciado

Investiga las siguientes bases de datos vectoriales y completa la tabla comparativa. Puedes usar la documentación oficial de cada una, artículos técnicos y los materiales de la asignatura.

### Parte 1: Tabla Comparativa

Completa la siguiente tabla para cada base de datos vectorial:

| Criterio | **FAISS** | **ChromaDB** | **Pinecone** | **Weaviate** | **pgvector** |
|----------|-----------|-------------|-------------|-------------|-------------|
| **Tipo** (librería / BD embebida / servicio cloud / extensión) | Librería | BD embebida | Servicio cloud | BD self-hosted / cloud | Extensión PostgreSQL |
| **Desarrollador** | Meta AI | Chroma Team | Pinecone Inc | SeMI Technologies | PostgreSQL community |
| **Lenguaje principal** | C++ (bindings Python) | Python | N/A (API SaaS) | Go | C (extensión PG) |
| **Persistencia** (en memoria / disco / cloud) | En memoria (opcional disco) | Disco (SQLite) | Cloud persistente | Disco / cloud | Disco (PostgreSQL) |
| **Coste** (gratuito / freemium / pago) | Gratuito (open source) | Gratuito (open source) | Freemium ($70+/mes) | Open source (self-host) o cloud | Gratuito (open source) |
| **Escalabilidad** (prototipo / producción pequeña / enterprise) | Prototipo / producción pequeña | Prototipo / producción pequeña | Enterprise | Producción / enterprise | Producción pequeña-media |
| **Búsqueda híbrida** (vectorial + keyword) | No | Limitada | Sí | Sí (excelente) | Sí (con PostgreSQL FTS) |
| **Filtrado por metadatos** | Básico (manual) | Sí | Sí (avanzado) | Sí (con GraphQL) | Sí (con SQL WHERE) |
| **Integración con LangChain** | Sí | Sí (excelente) | Sí (excelente) | Sí | Sí |
| **Requiere infraestructura propia** | No (local) | No (embebida) | No (SaaS) | Sí (self-host) | Sí (necesitas PostgreSQL) |
| **Curva de aprendizaje** (baja / media / alta) | Alta | Baja | Baja | Media | Media |
| **Caso de uso ideal** | Investigación, benchmarking, cuando necesitas máximo control sobre índices | Prototipos rápidos, MVPs, aplicaciones pequeñas | Producción cloud-native, necesitas escalabilidad sin gestión | Producción self-hosted, búsqueda híbrida compleja, grafos de conocimiento | Ya usas PostgreSQL y quieres añadir búsqueda vectorial sin nueva tecnología |

### Parte 2: Decisiones de Diseño

Para cada escenario, elige la base de datos vectorial más adecuada y justifica tu decisión:

**Escenario 1**: Un estudiante quiere hacer un prototipo rápido de RAG para un proyecto de clase, con ~100 documentos PDF.
- Base de datos elegida: ChromaDB
- Justificación: Es la opción ideal para prototipos. Se instala con pip install chromadb, no requiere configuración de infraestructura, tiene persistencia automática en SQLite y la integración con LangChain es directa. Para 100 documentos es más que suficiente y permite iterar rápido.

**Escenario 2**: Una startup necesita un sistema RAG en producción que maneje 500.000 documentos y escale automáticamente, sin dedicar DevOps al mantenimiento.
- Base de datos elegida: Pinecone
- Justificación: Es la mejor opción para este caso porque es completamente managed (SaaS), escala automáticamente sin intervención, tiene alta disponibilidad built-in y no requiere gestionar servidores. Aunque tiene coste, el ahorro en tiempo de DevOps lo compensa. Weaviate Cloud sería alternativa válida.

**Escenario 3**: Un banco necesita un sistema RAG para documentos financieros confidenciales. Todo debe ejecutarse on-premise por regulación. Tienen equipo de infraestructura.
- Base de datos elegida: Weaviate (self-hosted)
- Justificación: Weaviate self-hosted permite control total sobre dónde se almacenan los datos (crítico para compliance bancario), tiene capacidades enterprise (backup, replicación, escalabilidad), búsqueda híbrida avanzada y el equipo de infra puede gestionarlo. pgvector sería alternativa si ya usan PostgreSQL.

**Escenario 4**: Una empresa ya usa PostgreSQL para toda su infraestructura y quiere añadir capacidad de búsqueda semántica sin introducir una nueva tecnología.
- Base de datos elegida: pgvector
- Justificación: Es una extensión de PostgreSQL, no requiere aprender nueva tecnología ni mantener otro sistema. Aprovecha las capacidades existentes de PG (transacciones, backups, roles de usuario). Para volúmenes pequeños-medianos es perfectamente viable y reduce la complejidad operacional.

### Parte 3: Pregunta de Reflexión

¿Es posible empezar con ChromaDB para un prototipo y migrar después a Pinecone para producción? ¿Qué abstracción de LangChain facilita esta migración? ¿Qué cambios serían necesarios en el código?

**Respuesta**: Sí, es perfectamente posible y es una estrategia común. LangChain facilita esto mediante la abstracción `VectorStore`, que es una interfaz común para todas las bases de datos vectoriales. Tanto ChromaDB como Pinecone implementan esta interfaz con métodos como `from_documents()`, `similarity_search()` y `as_retriever()`. Los cambios necesarios en el código serían mínimos:
- Cambiar el import: de `from langchain.vectorstores import Chroma` a `from langchain.vectorstores import Pinecone`
- Cambiar la inicialización: de `Chroma.from_documents()` a `Pinecone.from_documents()`
- Añadir las credenciales de Pinecone (API key y environment)
- Ajustar potencialmente los parámetros de búsqueda (top_k, filtros de metadatos) si la API difiere ligeramente

El resto del código que usa el retriever (queries, chains, etc.) permanece idéntico porque todos los VectorStores exponen la misma interfaz. Esto es precisamente la ventaja de usar LangChain: poder cambiar componentes sin reescribir toda la aplicación.

### Extensión (Opcional)

- Instala ChromaDB localmente (`pip install chromadb`) e indexa 5-10 documentos de prueba. Experimenta con diferentes consultas y observa los resultados de similitud.
- Investiga Qdrant y Milvus como alternativas adicionales y añádelos a la tabla comparativa.

---

## Ejercicio 4: Laboratorio de Estrategias de Chunking

### Metadata
- **Duración estimada**: 35 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Lectura de la sección 5.4 sobre chunking, conocimientos de Python, familiaridad básica con LangChain

### Contexto
El chunking (fragmentación del texto) es una etapa crítica y a menudo subestimada en un pipeline RAG. Un chunking demasiado grande puede incluir información irrelevante que confunda al LLM; uno demasiado pequeño puede perder el contexto necesario para una respuesta coherente. El solapamiento (overlap) entre chunks permite que la información no se "corte" en medio de una idea. Este ejercicio te permite experimentar de primera mano con diferentes configuraciones y desarrollar intuición sobre sus efectos.

### Objetivo de Aprendizaje
- Usar `RecursiveCharacterTextSplitter` de LangChain con diferentes configuraciones
- Comprender el impacto del `chunk_size` y `chunk_overlap` en la fragmentación
- Analizar cuándo se pierde contexto y cuándo se preserva
- Desarrollar criterios para elegir la configuración óptima según el tipo de documento

### Enunciado

Experimenta con diferentes configuraciones de chunking sobre un documento de ejemplo y analiza los resultados.

### Paso 1: Preparar el documento de ejemplo

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Documento de ejemplo: artículo sobre inteligencia artificial
documento = """
# Introducción a la Inteligencia Artificial

La inteligencia artificial (IA) es una rama de la informática que busca crear sistemas
capaces de realizar tareas que normalmente requieren inteligencia humana. Estas tareas
incluyen el aprendizaje, el razonamiento, la percepción y la comprensión del lenguaje natural.

## Historia de la IA

El término "inteligencia artificial" fue acuñado por John McCarthy en 1956 durante la
conferencia de Dartmouth. Sin embargo, las ideas sobre máquinas pensantes se remontan a
mucho antes. Alan Turing, en 1950, propuso el famoso Test de Turing como criterio para
determinar si una máquina puede exhibir comportamiento inteligente indistinguible del humano.

Durante las décadas de 1960 y 1970, la IA experimentó un período de optimismo conocido
como la "edad de oro". Los investigadores creían que la IA general estaba a pocas décadas
de distancia. Sin embargo, las limitaciones computacionales y teóricas llevaron a los
"inviernos de la IA", períodos de reducción de financiación e interés.

## Aprendizaje Automático

El aprendizaje automático (machine learning) es un subcampo de la IA que se centra en
desarrollar algoritmos que permiten a las computadoras aprender de los datos sin ser
programadas explícitamente. Los tres paradigmas principales son:

1. Aprendizaje supervisado: el modelo aprende de ejemplos etiquetados.
2. Aprendizaje no supervisado: el modelo descubre patrones en datos sin etiquetar.
3. Aprendizaje por refuerzo: el modelo aprende mediante prueba y error con recompensas.

## Deep Learning

El deep learning o aprendizaje profundo utiliza redes neuronales con múltiples capas
(de ahí "profundo") para aprender representaciones jerárquicas de los datos. Las
arquitecturas más importantes incluyen:

- Redes Neuronales Convolucionales (CNN): especializadas en procesamiento de imágenes.
- Redes Neuronales Recurrentes (RNN): diseñadas para secuencias temporales.
- Transformers: la arquitectura dominante actual para procesamiento de lenguaje natural,
  introducida en el paper "Attention is All You Need" (2017).

## Modelos de Lenguaje

Los modelos de lenguaje grandes (LLMs) como GPT-4, Claude y Llama representan el estado
del arte en procesamiento de lenguaje natural. Estos modelos se entrenan con cantidades
masivas de texto y pueden generar texto coherente, traducir idiomas, resumir documentos
y responder preguntas.

La técnica de RAG (Retrieval-Augmented Generation) complementa estos modelos permitiéndoles
acceder a información externa actualizada, reduciendo las alucinaciones y proporcionando
respuestas más precisas y verificables.
"""

print(f"Longitud total del documento: {len(documento)} caracteres")
print(f"Número de líneas: {len(documento.splitlines())}")
```

### Paso 2: Experimentar con diferentes configuraciones

```python
configuraciones = [
    {"chunk_size": 100, "chunk_overlap": 0,  "nombre": "Muy pequeño, sin overlap"},
    {"chunk_size": 100, "chunk_overlap": 20, "nombre": "Muy pequeño, con overlap"},
    {"chunk_size": 300, "chunk_overlap": 0,  "nombre": "Mediano, sin overlap"},
    {"chunk_size": 300, "chunk_overlap": 50, "nombre": "Mediano, con overlap"},
    {"chunk_size": 500, "chunk_overlap": 50, "nombre": "Grande, con overlap pequeño"},
    {"chunk_size": 500, "chunk_overlap": 100,"nombre": "Grande, con overlap grande"},
    {"chunk_size": 1000,"chunk_overlap": 200,"nombre": "Muy grande, con overlap"},
]

for config in configuraciones:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunk_size"],
        chunk_overlap=config["chunk_overlap"],
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_text(documento)

    print(f"\n{'='*70}")
    print(f"Configuración: {config['nombre']}")
    print(f"  chunk_size={config['chunk_size']}, chunk_overlap={config['chunk_overlap']}")
    print(f"  Número de chunks: {len(chunks)}")
    print(f"  Tamaño promedio: {sum(len(c) for c in chunks) / len(chunks):.0f} caracteres")
    print(f"  Tamaño mínimo: {min(len(c) for c in chunks)} caracteres")
    print(f"  Tamaño máximo: {max(len(c) for c in chunks)} caracteres")
    print(f"  Caracteres totales (con overlap): {sum(len(c) for c in chunks)}")

    # Mostrar los primeros 3 chunks
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n  --- Chunk {i+1} ({len(chunk)} chars) ---")
        # Mostrar solo las primeras y últimas líneas
        lines = chunk.strip().split('\n')
        if len(lines) <= 4:
            print(f"  {chunk.strip()}")
        else:
            print(f"  {lines[0]}")
            print(f"  {lines[1]}")
            print(f"  ...")
            print(f"  {lines[-1]}")
```

### Paso 3: Análisis detallado del overlap

```python
# Analizar qué información se comparte entre chunks consecutivos
print("\n\n" + "="*70)
print("ANÁLISIS DE OVERLAP")
print("="*70)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_text(documento)

for i in range(len(chunks) - 1):
    chunk_actual = chunks[i]
    chunk_siguiente = chunks[i + 1]

    # Encontrar el texto solapado
    overlap_text = ""
    for length in range(min(len(chunk_actual), len(chunk_siguiente)), 0, -1):
        if chunk_actual.endswith(chunk_siguiente[:length]):
            overlap_text = chunk_siguiente[:length]
            break

    print(f"\nEntre Chunk {i+1} y Chunk {i+2}:")
    print(f"  Overlap encontrado ({len(overlap_text)} chars): \"{overlap_text[:80]}...\"" if len(overlap_text) > 80 else f"  Overlap encontrado ({len(overlap_text)} chars): \"{overlap_text}\"")
    print(f"  Final chunk {i+1}: \"...{chunk_actual[-50:]}\"")
    print(f"  Inicio chunk {i+2}: \"{chunk_siguiente[:50]}...\"")
```

### Paso 4: Tabla de análisis comparativo

Completa la siguiente tabla con los resultados de tus experimentos:

| Configuración | N. Chunks | Tam. Promedio | ¿Se cortan ideas a mitad? | ¿Hay redundancia excesiva? |
|--------------|-----------|---------------|---------------------------|---------------------------|
| 100, overlap 0 | ~25-30 | 95-100 | Sí, constantemente. Corta frases y palabras | No, pero es inútil porque los chunks son demasiado pequeños |
| 100, overlap 20 | ~28-35 | 95-100 | Sí, igual que antes. El overlap no compensa el tamaño tan pequeño | Un poco, hay texto duplicado pero no ayuda mucho |
| 300, overlap 0 | ~8-10 | 290-300 | A veces, especialmente si una sección ocupa más de 300 chars | No |
| 300, overlap 50 | ~9-11 | 290-300 | Menos que sin overlap. El overlap preserva contexto entre chunks | Mínima, aceptable para el beneficio obtenido |
| 500, overlap 50 | ~5-6 | 480-500 | Raramente. Los chunks capturan ideas completas | Mínima, el overlap es pequeño respecto al total |
| 500, overlap 100 | ~6-7 | 480-500 | Raramente. Buena preservación de contexto | Moderada, ~20% de redundancia pero útil |
| 1000, overlap 200 | ~3-4 | 950-1000 | No, cada chunk contiene secciones completas | Moderada, pero asegura que no se pierda contexto entre chunks grandes |

### Preguntas de Reflexión

1. ¿Con qué configuración se cortan más frases a mitad de una idea? ¿Por qué?

   **Respuesta**: Con chunk_size de 100 caracteres. Cuando los chunks son tan pequeños, es imposible respetar límites naturales del texto. El splitter intenta usar separadores como `\n\n` o `.` pero si no encuentra ninguno dentro del límite de 100 chars, corta arbitrariamente por espacios o incluso a mitad de palabra. Resultado: muchos chunks incoherentes.

2. ¿Cuál es el trade-off entre chunk_size pequeño y grande para la calidad de la búsqueda?

   **Respuesta**: Chunks pequeños dan precisión pero pierden contexto. Si buscas "transformers", un chunk pequeño podría devolver solo "arquitectura dominante actual para procesamiento de lenguaje natural" sin explicar qué son. Chunks grandes dan contexto completo pero pueden incluir información irrelevante que confunda al LLM. El sweet spot suele estar en 300-600 tokens: suficiente contexto sin ruido excesivo.

3. ¿Por qué `RecursiveCharacterTextSplitter` usa una jerarquía de separadores (`\n\n`, `\n`, `. `, ` `)? ¿Qué pasaría si solo usara un separador?

   **Respuesta**: La jerarquía respeta la estructura natural del texto. Primero intenta dividir por párrafos (`\n\n`), que son unidades semánticas completas. Si el párrafo es muy largo, divide por líneas (`\n`). Si aún es muy largo, por frases (`. `), y como último recurso por palabras (` `). Si solo usara un separador (por ejemplo `.`), textos sin puntos (como código o listas) se cortarían arbitrariamente, y párrafos cortos no se agruparían.

4. Si tu documento fuera código fuente Python en lugar de texto, ¿cambiarías los separadores? ¿Cuáles usarías?

   **Respuesta**: Sí, cambiaría completamente. Para código Python usaría: `["\n\nclass ", "\n\ndef ", "\n\n", "\n", " "]`. Esto prioritiza dividir por clases completas, luego funciones completas, luego bloques vacíos, líneas y finalmente espacios. De esta forma cada chunk contiene funciones o clases completas, que son unidades semánticas en código. LangChain tiene `PythonCodeTextSplitter` que hace exactamente esto.

5. ¿Qué configuración elegirías para un documento legal con párrafos largos y densos? ¿Y para un FAQ con preguntas y respuestas cortas?

   **Respuesta**:
   - **Documento legal**: chunk_size de 800-1000 con overlap de 150-200. Los textos legales tienen referencias cruzadas ("según el artículo anterior...") que requieren contexto amplio. El overlap alto asegura que no se pierdan conexiones entre artículos.
   - **FAQ**: chunk_size de 200-300 con overlap de 20-30. Cada pregunta-respuesta es una unidad independiente y pequeña. Chunks grandes mezclarían varias Q&A y confundirían la recuperación. Idealmente usaría un splitter custom que divida por cada par Q&A completo.

### Extensión (Opcional)

- Prueba `MarkdownHeaderTextSplitter` de LangChain, que divide por encabezados Markdown preservando la jerarquía. Compara los resultados con `RecursiveCharacterTextSplitter` sobre el mismo documento.
- Implementa un splitter personalizado que divida por secciones (`##`) y mantenga el título de sección como metadato de cada chunk.

---

## Ejercicio 5: Diseño de un Pipeline RAG Completo

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Diseño
- **Modalidad**: Grupal (2-3 personas)
- **Dificultad**: Intermedia
- **Prerequisitos**: Lectura completa de las secciones 5.1 a 5.4, comprensión de los ejercicios anteriores

### Contexto
Diseñar un sistema RAG completo requiere tomar decisiones coordinadas en cada etapa del pipeline: desde la ingesta y preprocesamiento de documentos, pasando por el chunking y la generación de embeddings, hasta la recuperación y la generación de respuestas. Cada decisión afecta a las demás y al rendimiento global del sistema. Este ejercicio integra todos los conceptos de la sesión en un diseño coherente de principio a fin.

### Objetivo de Aprendizaje
- Integrar todos los conceptos de la sesión en un diseño de sistema completo
- Tomar decisiones de diseño coordinadas y justificadas
- Identificar los puntos de fallo potenciales en un pipeline RAG
- Desarrollar la capacidad de comunicar decisiones técnicas a través de diagramas

### Enunciado

En grupos de 2-3 personas, elegid **uno** de los siguientes casos de uso y diseñad un pipeline RAG completo. Debéis producir: un diagrama del sistema, una tabla de decisiones técnicas y un análisis de riesgos.

### Casos de Uso (elegir uno)

**Caso A: Asistente de Documentación Técnica**
Una empresa de software con 2.000 páginas de documentación técnica (API docs, tutoriales, guías de troubleshooting) quiere un chatbot que ayude a los desarrolladores. La documentación está en Markdown en un repositorio Git y se actualiza 3-4 veces por semana.

**Caso B: Buscador Inteligente de Normativa Universitaria**
Una universidad quiere que estudiantes y profesores puedan hacer preguntas sobre normativa académica (reglamentos de evaluación, normativa TFG/TFM, convocatorias, protocolos). Los documentos son PDFs oficiales (~50 documentos, ~500 páginas totales) que se actualizan una vez al año.

**Caso C: Asistente de Recursos Humanos**
Una empresa con 500 empleados quiere un asistente que responda preguntas sobre políticas internas (vacaciones, teletrabajo, beneficios, código de conducta). Los documentos son una mezcla de PDFs, páginas de la intranet y presentaciones PowerPoint.

### Parte 1: Diagrama del Pipeline

Dibujad (en papel, pizarra o herramienta digital) un diagrama que incluya todas las etapas del pipeline, desde la fuente de datos hasta la respuesta al usuario. Debe incluir como mínimo:

```
┌─────────────┐    ┌──────────────┐    ┌───────────┐    ┌──────────────┐
│  Fuentes de │───>│ Preprocesado │───>│ Chunking  │───>│  Generación  │
│    Datos    │    │  y Limpieza  │    │           │    │  Embeddings  │
└─────────────┘    └──────────────┘    └───────────┘    └──────┬───────┘
                                                               │
                                                               v
┌─────────────┐    ┌──────────────┐    ┌───────────┐    ┌──────────────┐
│  Respuesta  │<───│  Generación  │<───│ Ranking y │<───│    Base de   │
│  al Usuario │    │   con LLM    │    │ Selección  │    │    Datos     │
└─────────────┘    └──────────────┘    └───────────┘    │  Vectorial   │
                                                        └──────────────┘
         ▲                                                     ▲
         │              ┌───────────┐                          │
         └──────────────│  Consulta │──────────────────────────┘
                        │  Usuario  │
                        └───────────┘
```

Para cada bloque del diagrama, anotad la tecnología o herramienta concreta que usaríais.

### Parte 2: Tabla de Decisiones Técnicas

| Decisión | Vuestra elección | Alternativas consideradas | Justificación |
|----------|-----------------|--------------------------|---------------|
| **Formato de entrada** | Markdown en repositorio Git | HTML scraping, JSON | La doc técnica moderna casi siempre está en Markdown, es fácil de parsear y mantener estructura |
| **Herramienta de extracción de texto** | MarkItDown o BeautifulSoup para parser MD | pypandoc, mistune | MarkItDown preserva la estructura jerárquica (headers, code blocks) que es crítica para doc técnica |
| **Estrategia de chunking** | MarkdownHeaderTextSplitter por secciones | RecursiveCharacterTextSplitter | Divide por headers (##, ###) preservando jerarquía. Cada chunk mantiene metadata de su sección |
| **chunk_size** | 600 tokens | 400, 800 | Balance entre contexto (snippets de código completos) y precisión (no mezclar múltiples endpoints) |
| **chunk_overlap** | 100 tokens | 50, 150 | Suficiente para conectar secciones relacionadas sin duplicar demasiado contenido |
| **Modelo de embeddings** | text-embedding-3-small | code-search-ada-002, sentence-transformers | Balanceo coste/calidad. code-search-ada sería ideal pero más caro, text-3-small maneja código decentemente |
| **Base de datos vectorial** | Pinecone | Weaviate, ChromaDB | Escalabilidad automática, búsqueda híbrida para nombres exactos de funciones, infraestructura managed |
| **Número de chunks recuperados (top-k)** | 5 chunks | 3, 7 | Suficiente contexto para respuestas completas sin saturar ventana del LLM |
| **Estrategia de búsqueda** (solo vectorial / híbrida) | Híbrida (vectorial 70% + keyword 30%) | Solo vectorial | Keyword crucial para buscar nombres exactos de funciones/clases, vectorial para conceptos |
| **LLM para generación** | Claude Sonnet 3.5 | GPT-4o, Llama 3 70B | Excelente para razonamiento técnico, ventana de contexto amplia, sigue instrucciones bien |
| **Prompt template** (describir estructura) | System: rol de asistente técnico. Context: chunks recuperados con metadata de archivo y sección. Instructions: citar fuentes, admitir desconocimiento, formato en Markdown con code blocks. Question: query del usuario | - | Estructura clara que fuerza al LLM a fundamentar respuestas en el contexto |
| **Frecuencia de actualización del índice** | Webhook en cada push a main + reindexación completa semanal | Manual, diaria | Automático asegura docs actualizadas, reindexación semanal detecta archivos eliminados o renombrados |

### Parte 3: Prompt Template

Diseñad el prompt que recibirá el LLM para generar la respuesta. Debe incluir instrucciones claras sobre cómo usar el contexto recuperado:

```
Eres un asistente técnico experto en nuestra documentación de software. Tu función es responder preguntas
basándote EXCLUSIVAMENTE en el siguiente contexto proporcionado extraído de la documentación oficial.

CONTEXTO:
{contexto_recuperado}

INSTRUCCIONES:
- Solo responde con información presente en el contexto proporcionado
- Si el contexto no contiene información suficiente para responder, di explícitamente "No encuentro esa información en la documentación actual"
- Cita la fuente de cada afirmación indicando el archivo y sección (usa la metadata del chunk)
- Incluye ejemplos de código del contexto cuando sea relevante
- Si hay múltiples formas de hacer algo en el contexto, menciónalas todas
- Usa formato Markdown con bloques de código apropiados (```python, ```javascript, etc.)
- Si detectas que la documentación podría estar desactualizada, menciónalo
- No inventes nombres de funciones, parámetros o configuraciones que no estén en el contexto

PREGUNTA DEL USUARIO:
{pregunta}

RESPUESTA:
```

### Parte 4: Análisis de Riesgos y Mitigaciones

Identificad al menos 4 riesgos potenciales del sistema y proponed mitigaciones:

| Riesgo | Probabilidad | Impacto | Mitigación propuesta |
|--------|-------------|---------|---------------------|
| El LLM alucina e inventa información no presente en el contexto | Alta | Alto | Prompt muy explícito que prohíba inventar información. Añadir post-procesamiento que verifique que snippets de código citados aparezcan en el contexto. Logging de respuestas para auditoría |
| La consulta del usuario no tiene respuesta en los documentos | Media | Medio | Instruir al LLM a decir claramente "No encuentro esa información". Implementar sistema de feedback para identificar gaps en la documentación. Considerar añadir fallback a búsqueda web oficial |
| Chunks recuperados están desactualizados tras actualización de docs | Media | Alto | Pipeline CI/CD que reindexe automáticamente en cada push. Incluir metadata de timestamp en chunks. Mostrar "última actualización" en respuestas |
| Query ambigua devuelve chunks irrelevantes | Alta | Medio | Implementar query expansion con LLM que reformule preguntas vagas. Usar reranking con cross-encoder después de retrieval inicial. Mostrar chunks recuperados al usuario para transparencia |

### Parte 5: Presentación (5 minutos por grupo)

Cada grupo presenta brevemente su diseño al resto de la clase, explicando:
1. El caso de uso elegido y por qué
2. Las 2-3 decisiones técnicas más importantes y su justificación
3. El riesgo que consideran más crítico y cómo lo mitigan

### Extensión (Opcional)

- Añadid al diseño un sistema de evaluación: ¿cómo mediríais la calidad de las respuestas del sistema? Investigad métricas como Faithfulness, Answer Relevancy y Context Precision del framework RAGAS.
- Diseñad un flujo de feedback del usuario: ¿cómo incorporaríais las valoraciones de los usuarios (pulgar arriba/abajo) para mejorar el sistema?
