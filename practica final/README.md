# Asistente RAG sobre TFG con n8n + MCP

Sistema de asistente inteligente basado en **Retrieval-Augmented Generation (RAG)** que responde preguntas sobre un Trabajo Fin de Grado real. El conocimiento está centralizado en una base vectorial (Pinecone) y se expone a través de **dos interfaces independientes**: un bot de Telegram gestionado por un agente propio en n8n (GPT-4o-mini), y Claude Desktop conectado mediante un servidor **Model Context Protocol (MCP)** también implementado en n8n.

Proyecto final de la asignatura **Aprendizaje Automático 2** (grado en Ingeniería de Datos e Inteligencia Artificial).

---

## Índice

1. [Unidades del curso aplicadas](#unidades-del-curso-aplicadas)
2. [Arquitectura](#arquitectura)
3. [Tecnologías utilizadas](#tecnologías-utilizadas)
4. [Estructura del repositorio](#estructura-del-repositorio)
5. [Instalación y configuración](#instalación-y-configuración)
6. [Uso](#uso)
7. [Capturas / Demo](#capturas--demo)
8. [Decisiones técnicas](#decisiones-técnicas)
9. [Posibles mejoras](#posibles-mejoras)
10. [Autor](#autor)

---

## Unidades del curso aplicadas

El proyecto integra conceptos de **las 6 unidades del curso**:

| Unidad | Tema | Cómo se aplica en el proyecto |
|--------|------|-------------------------------|
| **U1** | IA Generativa y LLMs | Se utilizan dos modelos de lenguaje: **GPT-4o-mini** (OpenAI) como cerebro del agente de Telegram, y **Claude** (Anthropic) como cerebro del cliente MCP en Claude Desktop. Ambos son modelos basados en arquitectura Transformer y se invocan con prompts específicos al dominio del TFG. |
| **U2** | Prompt Engineering | El agente de Telegram usa un **system prompt estructurado** con el patrón *Rol — Tareas — Restricciones — Formato* que fuerza al LLM a apoyarse siempre en la tool de búsqueda, citar secciones del TFG y responder con un mensaje predefinido cuando no encuentra información. Las descripciones de las tools del servidor MCP también son prompts estructurados que Claude utiliza para decidir cuándo invocarlas. |
| **U3** | Transformers y APIs | Todo el sistema se comunica **programáticamente vía APIs**: OpenAI API (embeddings y modelo GPT-4o-mini), Anthropic API (Claude, consumida internamente por Claude Desktop), Pinecone API (base vectorial), Telegram Bot API (canal de mensajería) y PostgreSQL (Supabase, memoria de conversación). |
| **U4** | Agentes y Automatización | Se implementan **dos agentes distintos** con capacidad de decisión autónoma: (1) un agente propio en n8n con GPT-4o-mini que decide cuándo usar la tool de búsqueda vectorial para responder al usuario en Telegram, y (2) Claude (en Claude Desktop) actuando como agente que decide cuándo invocar `search_tfg` y/o `send_telegram_message` vía MCP. Todo está orquestado con workflows de n8n. |
| **U5** | RAG y Bases Vectoriales | Pipeline RAG completo: **ingesta** de 8 documentos (.txt) del TFG desde Google Drive, **chunking** con Recursive Character Text Splitter, **embeddings** con `text-embedding-3-small` (1536 dimensiones), **almacenamiento** en Pinecone (índice `asistente-tfg`, métrica coseno) y **recuperación semántica** con top-k=4 en cada consulta. El índice contiene **458 vectores** que cubren todo el TFG. |
| **U6** | MCP (Model Context Protocol) | Se implementa un **servidor MCP en n8n** (nodo `MCP Server Trigger`) que expone dos tools al exterior: `search_tfg` (búsqueda vectorial en Pinecone) y `send_telegram_message` (envío de mensajes a Telegram). Claude Desktop se conecta a este servidor como cliente MCP mediante el puente `mcp-remote`. |

---

## Arquitectura

El sistema tiene una **base de conocimiento compartida** (Pinecone) accesible desde dos entradas independientes:

```
                    BASE DE CONOCIMIENTO
                ┌───────────────────────────┐
                │   Pinecone (asistente-tfg)│
                │   458 vectores, 1536 dims │
                └────────────┬──────────────┘
                             │
            ┌────────────────┴─────────────────┐
            │                                  │
            ▼                                  ▼
    ┌───────────────┐                ┌────────────────────┐
    │ Workflow n8n  │                │ Workflow n8n       │
    │ Agente        │                │ MCP Server         │
    │ Telegram      │                │ Trigger            │
    │ (GPT-4o-mini) │                │                    │
    └───────┬───────┘                │ Tools expuestas:   │
            │                        │ • search_tfg       │
            │                        │ • send_telegram    │
            │                        └─────────┬──────────┘
            ▼                                  ▲
      ┌───────────┐                            │ MCP protocol
      │  Usuario  │                            │ (vía mcp-remote)
      │ Telegram  │                            │
      └───────────┘                  ┌─────────┴──────────┐
                                     │   Claude Desktop    │
                                     │   (cliente MCP)     │
                                     └─────────────────────┘

    FLUJO INDEPENDIENTE: Ingesta (ejecutada una vez)
    ┌───────────────────────────────────────────────────┐
    │ Manual Trigger                                    │
    │   → Google Drive (Search 8 .txt del TFG)          │
    │   → Google Drive (Download)                       │
    │   → Default Data Loader (Binary, Text)            │
    │   → Recursive Character Text Splitter (300/30)    │
    │   → Embeddings OpenAI (text-embedding-3-small)    │
    │   → Pinecone Vector Store (Insert)                │
    └───────────────────────────────────────────────────┘
```

### Los 3 workflows de n8n

1. **`RAG - Ingesta`**: carga los 8 documentos del TFG (resumen, introducción, estado de la cuestión, metodología, desarrollo, conclusiones, glosario y anexo del system prompt original del TFG) desde Google Drive, los trocea, genera embeddings y los almacena en Pinecone.
2. **`RAG - Asistente TFG (Telegram)`**: Telegram Trigger → AI Agent (GPT-4o-mini + memoria Postgres) → Send Telegram Message. El agente dispone de la tool vectorial conectada al índice `asistente-tfg`.
3. **`RAG - MCP Server`**: MCP Server Trigger que expone dos tools (`search_tfg` y `send_telegram_message`) accesibles vía el protocolo MCP.

### Cliente MCP

**Claude Desktop** se conecta al servidor MCP de n8n mediante el paquete `mcp-remote` (que actúa como puente entre el transporte stdio local de Claude Desktop y el endpoint HTTP del MCP Server de n8n Cloud). La configuración vive en `claude_desktop_config.json`.

---

## Tecnologías utilizadas

### Orquestación y no-code
- **n8n Cloud** — plataforma de automatización donde viven los 3 workflows (ingesta, agente Telegram y servidor MCP)

### Modelos de lenguaje (LLMs)
- **GPT-4o-mini** (OpenAI) — agente del bot de Telegram
- **Claude** (Anthropic) — agente en Claude Desktop (cliente MCP)

### Embeddings y base vectorial
- **text-embedding-3-small** (OpenAI) — modelo de embeddings de 1536 dimensiones, cubierto por los créditos gratuitos de n8n
- **Pinecone** — base vectorial serverless (AWS · us-east-1 · métrica coseno)

### Memoria y persistencia
- **Supabase** (PostgreSQL) — memoria conversacional del agente de Telegram, vía el nodo `Postgres Chat Memory` (session id = chat id de Telegram, ventana de contexto de 10 mensajes)

### Canales y protocolos
- **Telegram Bot API** — interfaz de usuario en Telegram
- **MCP (Model Context Protocol)** — exposición de tools desde n8n hacia Claude Desktop
- **mcp-remote** (npm) — puente que traduce MCP stdio (Claude Desktop) a HTTP (n8n Cloud)

### Fuente de documentos
- **Google Drive** — almacén de los 8 archivos `.txt` del TFG, leídos desde n8n Cloud vía los nodos oficiales de Drive

### Cliente MCP
- **Claude Desktop** — aplicación de escritorio de Anthropic con soporte nativo MCP

---

## Estructura del repositorio

```
practica final/
├── README.md                       # Este archivo
├── .gitignore                      # Archivos excluidos del repo
├── .env.example                    # Plantilla de variables de entorno
├── documentos/                     # Documentos fuente del RAG
│   ├── tfg_00_resumen.txt
│   ├── tfg_01_introduccion.txt
│   ├── tfg_02_estado_cuestion.txt
│   ├── tfg_03_metodologia.txt
│   ├── tfg_04_desarrollo.txt
│   ├── tfg_05_conclusiones.txt
│   ├── tfg_06_glosario.txt
│   └── tfg_07_anexo_prompt.txt
├── workflows/                      # Workflows n8n exportados
│   ├── RAG - Ingesta.json
│   ├── RAG - Asistente TFG - Telegram.json
│   └── RAG - MCP Server.json
└── capturas/                       # Capturas de pantalla del proyecto
    └── ... (33 capturas)
```

---

## Instalación y configuración

> El proyecto es **mayoritariamente no-code**: los 3 workflows viven en n8n Cloud. Lo único que se instala "localmente" es Claude Desktop y su configuración MCP. No hay Python, no hay `requirements.txt`.

### Requisitos previos

- Cuenta de **n8n Cloud** (o autoalojado)
- Cuenta de **Pinecone** (free tier)
- Cuenta de **OpenAI** (o usar los créditos gratuitos de n8n)
- Cuenta de **Supabase** (free tier, PostgreSQL)
- **Bot de Telegram** creado con [@BotFather](https://t.me/BotFather)
- Cuenta de **Google** con **Google Drive**
- **Claude Desktop** instalado ([descargar](https://claude.ai/download))
- **Node.js** ≥ 18 instalado (necesario para `npx mcp-remote`)

### Paso 1: Crear el índice de Pinecone

En el dashboard de Pinecone:
- **Index Name**: `asistente-tfg`
- **Dimensions**: `1536` (coincide con `text-embedding-3-small`)
- **Metric**: `cosine`
- **Cloud**: AWS, **Region**: `us-east-1` (free tier)
- **Capacity Mode**: Serverless

### Paso 2: Subir los documentos a Google Drive

Crear una carpeta en Drive (p.ej. `TFG_RAG_Documentos`) y subir los 8 archivos `.txt` de la carpeta `documentos/` de este repo.

### Paso 3: Importar los workflows en n8n

1. Importar los 3 JSON de `workflows/` en n8n (Create → Import from file).
2. Conectar las credenciales en cada nodo:
   - **Google Drive OAuth2** (workflow de ingesta)
   - **OpenAI** (embeddings + chat)
   - **Pinecone** (API key)
   - **Telegram Bot API** (token del bot)
   - **PostgreSQL / Supabase** (usar el **Session pooler** en modo IPv4, no la conexión directa — n8n Cloud no soporta IPv6)
3. En el workflow de ingesta: seleccionar la carpeta de Drive correspondiente en el nodo `Search files and folders`.
4. Verificar en todos los nodos Pinecone que el índice es `asistente-tfg`.
5. Verificar en todos los nodos Embeddings que el modelo es `text-embedding-3-small`.

### Paso 4: Ejecutar la ingesta (una vez)

Abrir el workflow `RAG - Ingesta` y pulsar **Execute Workflow**. Debería generar **~450 vectores** en Pinecone.

### Paso 5: Activar los workflows de servicio

Poner en **Active** los workflows `RAG - Asistente TFG (Telegram)` y `RAG - MCP Server`. Copiar la **Production URL** del MCP Server Trigger.

### Paso 6: Configurar Claude Desktop

Editar `%APPDATA%\Claude\claude_desktop_config.json` en Windows (o `~/Library/Application Support/Claude/claude_desktop_config.json` en macOS):

```json
{
  "mcpServers": {
    "tfg-asistente": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://TU-INSTANCIA.app.n8n.cloud/mcp/TU-PATH-UUID"
      ]
    }
  }
}
```

Sustituir la URL por la **Production URL** del MCP Server. Reiniciar Claude Desktop.

Ver `.env.example` para el listado completo de credenciales documentadas.

---

## Uso

### Interfaz 1: Bot de Telegram

Abrir el chat con el bot y escribir cualquier pregunta sobre el TFG. Ejemplos:

- *"¿Qué modelos de lenguaje se evaluaron en el TFG?"*
- *"¿Cuál fue el F1-Score de Claude en el caso GONJARA?"*
- *"¿Por qué se eligió Tesseract como OCR?"*
- *"¿Cuántas facturas tenía el dataset de IAG?"*
- *"¿Cuál es el menú del comedor de la empresa?"* (caso negativo — el agente responde que no dispone de esa info)

El bot usa GPT-4o-mini y guarda memoria de la conversación en Supabase (ventana de 10 mensajes por chat).

### Interfaz 2: Claude Desktop vía MCP

Abrir una conversación en Claude Desktop. Al tener el conector `tfg-asistente` activo, Claude dispone de las dos tools. Ejemplos:

- **Solo búsqueda**: *"Busca en mi TFG qué modelos de lenguaje se evaluaron y cuáles fueron sus F1-Scores"*
- **Solo envío**: *"Mándame por Telegram: Hola desde Claude Desktop"*
- **Combo (búsqueda + envío)**: *"Busca en mi TFG el hallazgo principal sobre el cuello de botella del sistema, haz un resumen de 2 líneas y mándamelo por Telegram"*

En el tercer caso Claude encadena las dos tools: primero `search_tfg` y después `send_telegram_message`.

El `chat_id` de Telegram está fijado en el workflow MCP (valor único del propietario del asistente), por lo que Claude solo necesita pasar el texto del mensaje.

---

## Capturas / Demo

Todas las capturas están en la carpeta [`capturas/`](capturas/).

### Ingesta (Unidad 5)

| Captura | Descripción |
|---------|-------------|
| `ingesta_workflow.png` | Canvas del workflow de ingesta con todos los nodos conectados |
| `registros_ingesta_pinecone.png` | Registros en Pinecone con contenido real del TFG |
| `metricas_ingesta_pinecone.png` | Métricas del índice `asistente-tfg` tras la ingesta |

### Agente Telegram (Unidades 1–5)

| Captura | Descripción |
|---------|-------------|
| `agente_telegram_workflow.png` | Canvas del workflow del agente de Telegram |
| `telegram_pregunta_1.png` a `telegram_pregunta_5.png` | 5 preguntas de prueba (3 positivas, 1 con dato numérico, 1 caso negativo) |
| `ejecucion_n8n_pregunta1.png` | Ejecución exitosa en n8n para la pregunta 1 |
| `ejecucion_n8n_pregunta1_vector.png` | Detalle de la llamada al Pinecone Vector Store Tool |
| `ejecucion_n8n_pregunta1_enbeddings.png` | Detalle de la generación de embeddings |

### Servidor MCP (Unidad 6)

| Captura | Descripción |
|---------|-------------|
| `workflow_mcp_server.png` | Canvas del workflow del servidor MCP |
| `trigger_mcp_server.png` | Configuración del MCP Server Trigger |
| `mcp_tool_pinecone.png` | Configuración de la tool `search_tfg` |
| `mcp_tool_telegram.png` | Configuración de la tool `send_telegram_message` |

### Claude Desktop como cliente MCP (Unidad 6)

| Captura | Descripción |
|---------|-------------|
| `claude_MCP_tool.png` | Claude Desktop reconociendo el conector `tfg-asistente` con sus 2 tools |
| `claude_pregunta_1.png` | Pregunta 1: búsqueda pura (solo `search_tfg`) |
| `claude_pregunta_2.png` + `claude_respuesta_2_telegram.png` | Pregunta 2: envío puro (solo `send_telegram_message`) |
| `claude_pregunta_3.png` + `claude_respuesta_3_telegram.png` | Pregunta 3 (**demo estrella**): combo — Claude busca en el TFG, resume y envía el resumen por Telegram |
| `ejercucion_n8n_MCP_pregunta1.png`, `_pregunta2.png`, `_pregunta3.png` | Trazas de las 3 ejecuciones en n8n disparadas por Claude |
| `vector_n8n_MCP_pregunta1.png` + `vector_n8n_MCP_pregunta3.png` | Detalle de la llamada al vector store en las preguntas 1 y 3 |
| `embedding_n8n_MCP_pregunta1.png` + `embedding_n8n_MCP_pregunta3.png` | Detalle de la generación de embeddings |
| `telegram_n8n_MCP_pregunta2.png` + `telegram_n8n_MCP_pregunta3.png` | Detalle del nodo Telegram enviando los mensajes |
| `ejercucion_search_tfg_n8n_MCP_pregunta3.png` | Traza de la tool `search_tfg` en la pregunta combo |

---

## Decisiones técnicas

### ¿Por qué n8n en lugar de Python?

Como base del proyecto se partió de la práctica 5 de RAG, que ya estaba montada en n8n. Mantener la misma plataforma facilita la trazabilidad (historial de commits y capturas consistente) y permite centrarse en lo nuevo: la capa MCP y la integración multicliente. Además, los workflows de n8n son **visualmente autoexplicativos**, algo especialmente útil para la defensa.

### ¿Por qué dos agentes independientes (Telegram y Claude) en lugar de uno compartido?

Porque demuestra con claridad el valor del enfoque **"conocimiento centralizado, clientes intercambiables"**: el mismo índice Pinecone da servicio a dos agentes distintos con cerebros distintos (GPT-4o-mini vs Claude) y un protocolo de acceso distinto (directo en n8n vs MCP). Es precisamente el argumento principal de MCP.

### ¿Por qué Pinecone?

Recomendado en la práctica 5 y ya familiar. Free tier suficiente para el volumen del proyecto. El índice se recreó desde cero (`asistente-tfg`) para no contaminar datos con la práctica anterior.

### ¿Por qué `text-embedding-3-small`?

- **Dimensión 1536** — estándar, compatible con el índice de Pinecone configurado
- **Incluido en los créditos gratuitos de n8n** (a diferencia de `text-embedding-ada-002`, que requiere créditos de pago en OpenAI)
- **Calidad actualizada** — OpenAI recomienda este modelo como reemplazo directo de `ada-002`

**Crítico**: el modelo de embeddings en la ingesta y en la recuperación (agente Telegram + tool MCP) **debe ser el mismo**. Si no, los vectores no viven en el mismo espacio y el RAG devuelve basura. Las tres ubicaciones en este proyecto usan `text-embedding-3-small`.

### ¿Por qué `gpt-4o-mini` para el agente de Telegram?

- **Barato y rápido** — coste de ~0,15$ por millón de tokens de entrada
- **Soporta tool use (function calling)** — imprescindible para que el agente pueda llamar a la tool de búsqueda vectorial. Se probaron modelos gratuitos de OpenRouter (`gemma-3-27b-it:free`, `llama-3.3-70b:free`) pero ninguno soportaba tool use de forma fiable.
- **Incluido en los créditos gratuitos de n8n**

### Chunk size = 300, overlap = 30

Se mantienen los parámetros recomendados en la práctica 5 para permitir comparación directa. Con chunk=300 los 89 KB de TFG limpio producen **458 vectores**, una granularidad razonable que permite recuperar pasajes específicos (cifras, definiciones) sin perder contexto. El overlap de 30 caracteres evita que se parta información en los límites de chunk.

### k = 4 documentos recuperados por consulta

Suficiente contexto para el agente sin saturar el prompt. Mismo valor que en la práctica 5 y en la práctica 4 (RAG clásico).

### Google Drive como fuente de documentos (en lugar de disco local)

n8n Cloud no tiene acceso al disco local del usuario, así que se usó Google Drive como "almacén remoto" accesible vía su integración nativa. Ventaja añadida: añadir un documento nuevo al asistente es tan simple como arrastrarlo a la carpeta de Drive y re-ejecutar la ingesta — no hay que tocar el workflow.

### Supabase para memoria del agente de Telegram

Reutilizado de la práctica 5. La sesión se identifica por `chat.id` de Telegram, así que cada usuario mantiene su propio hilo conversacional. Se usa el **Session pooler** (IPv4, puerto 5432) porque n8n Cloud no soporta el modo IPv6 que usa la conexión directa de Supabase — este detalle costó un rato de depuración y merece aparecer aquí.

### `chat_id` fijo en la tool `send_telegram_message`

La tool se configuró con `chat_id` como **valor literal** (el chat del propietario del asistente) en lugar de `$fromAI("chat_id", ...)`. Así Claude solo tiene que pasar el texto del mensaje y nunca necesita conocer el identificador del chat. La tool queda más simple, el diálogo en Claude Desktop queda más natural y la defensa es más fluida (*"mándame por Telegram..."* funciona directamente).

### System prompt del agente de Telegram

Estructurado con el patrón **Rol — Tareas — Restricciones — Formato**. La restricción más importante es que el agente **solo puede responder con información presente en la documentación vectorizada**; para cualquier pregunta fuera del TFG responde con un mensaje predefinido. Esto fuerza al modelo a no alucinar datos sobre el TFG.

### Claude Desktop como cliente MCP (no Python)

Claude Desktop tiene soporte nativo para MCP y su configuración es solo un JSON. Esto simplifica enormemente la integración comparado con implementar un cliente MCP a mano con Python + el SDK de Anthropic. Como el MCP Server de n8n expone transporte HTTP (SSE) pero Claude Desktop consume MCP vía stdio, se usa el puente oficial **`mcp-remote`** (paquete npm ejecutado vía `npx`) como traductor entre ambos transportes.

---

## Posibles mejoras

### 1. Re-ranking de los resultados de Pinecone

Pinecone ofrece un módulo de re-ranking disponible en el propio nodo de n8n (opción desactivada en este proyecto). Introducir un paso de re-ranking mejoraría la precisión en consultas ambiguas donde los primeros resultados por similitud vectorial no coinciden necesariamente con los más relevantes semánticamente.

### 2. Habilitar RLS (Row Level Security) en Supabase

La tabla `n8n_chat_histories` está actualmente expuesta sin Row Level Security. En un entorno de producción conviene activar RLS para aislar las memorias de conversación por usuario de forma segura. Supabase lo señaló como *critical issue* durante la configuración — se documenta como mejora pendiente.

### 3. Ampliar la base documental más allá del TFG

El diseño permite añadir documentos nuevos sin tocar código: basta con subirlos a la carpeta de Google Drive y re-ejecutar la ingesta. Podrían añadirse las memorias de prácticas de empresa, apuntes de asignaturas o publicaciones personales, convirtiendo el asistente en una "segunda memoria" personal consultable desde Telegram y Claude Desktop.

### 4. Tool adicional en el MCP Server: `send_email`

Añadir una tercera tool que envíe correos (por ejemplo vía Gmail o SendGrid). Cubriría el caso de uso *"mándame esto por email"* en paralelo a Telegram, y demostraría aún mejor la naturaleza extensible del servidor MCP.

### 5. Reducir dependencia de proveedores externos con modelos locales

Actualmente todo pasa por OpenAI (embeddings y chat), Pinecone (vectores) y Anthropic (Claude). Una versión autoalojada podría usar **Ollama** con LLaMA o Mistral, embeddings locales (`nomic-embed-text`, `bge-m3`) y **Qdrant** o **ChromaDB** como base vectorial. Se ganaría en privacidad y coste a cambio de algo de precisión.

### 6. Despliegue en un servidor persistente

El sistema depende de n8n Cloud y Claude Desktop. Una mejora sería alojar n8n en Railway/Render y hacer que el MCP Server sea accesible desde cualquier cliente MCP compatible (Cursor, Zed, otros Claude Desktop...). Ya se dan todos los ingredientes técnicos; solo falta el despliegue.

---

## Autor

**Álvaro García-Calderón Huerta**
Grado en Ingeniería de Datos e Inteligencia Artificial
Aprendizaje Automático 2 — Curso 2025/2026
