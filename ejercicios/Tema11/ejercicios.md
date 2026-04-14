# Ejercicios Prácticos - Unidad 6, Sesión 1
## Introducción a MCP y Configuración de Servidores

---

## Ejercicio 1: Análisis de Arquitectura MCP

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 6.1 sobre el Model Context Protocol y su arquitectura cliente-servidor

### Contexto
El Model Context Protocol (MCP) propone una arquitectura estandarizada para conectar modelos de lenguaje con fuentes de datos y herramientas externas. Antes de MCP, cada integración requería un conector personalizado (N×M integraciones), lo que generaba un ecosistema fragmentado y difícil de mantener. MCP reduce esta complejidad a un modelo N+M: cada herramienta implementa un servidor MCP y cada cliente se conecta mediante un protocolo universal. Comprender esta arquitectura es el primer paso para diseñar sistemas de IA verdaderamente conectados.

### Objetivo de Aprendizaje
- Identificar los componentes clave de la arquitectura MCP: host, cliente, servidor y LLM
- Comprender el flujo de comunicación entre componentes
- Comparar el enfoque MCP con integraciones acopladas punto a punto
- Desarrollar la capacidad de diseñar arquitecturas MCP para escenarios reales

### Enunciado

Un equipo de producto quiere construir un **asistente de IA para gestión de proyectos** que pueda:
1. Leer y enviar correos electrónicos (Gmail)
2. Consultar y crear eventos en el calendario (Google Calendar)
3. Enviar mensajes y leer canales de Slack
4. Acceder a documentos en Google Drive

### Parte A: Diagrama de Arquitectura MCP (10 min)

Dibuja la arquitectura MCP completa para este escenario. Tu diagrama debe incluir:

| Componente | Qué debes identificar |
|------------|----------------------|
| **Host** | La aplicación que aloja al cliente MCP (ej: Claude Desktop) |
| **Cliente MCP** | El componente dentro del host que gestiona las conexiones |
| **Servidores MCP** | Un servidor por cada integración externa |
| **LLM** | El modelo de lenguaje que toma decisiones |
| **Recursos externos** | Las APIs/servicios finales (Gmail API, Calendar API, etc.) |
| **Flechas de comunicación** | Protocolo usado en cada conexión |

Esquema de referencia para tu diagrama:

```
┌─────────────────────────────────────────────┐
│                    HOST                     │
│  ┌─────────┐                                │
│  │   LLM   │                                │
│  └────┬────┘                                │
│       │                                     │
│  ┌────▼────────────────────────────────┐    │
│  │         CLIENTE MCP                 │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌─────┐ │    │
│  │  │Conn 1│ │Conn 2│ │Conn 3│ │ ..  │ │    │
│  └──┴───┬──┴─┴───┬──┴─┴───┬──┴─┴───┬─┘─┘    │
│         │        │        │        │        │
└─────────┼────────┼────────┼────────┼────────┘
          │JSON-RPC│        │        │
     ┌────▼───┐┌───▼────┐┌──▼─────┐┌─▼──────┐
     │Servidor││Servidor││Servidor││Servidor│
     │ Gmail  ││Calendar││ Slack  ││ Drive  │
     └───┬────┘└───┬────┘└──┬─────┘└─┬──────┘
         │         │        │        │
     ┌───▼───┐ ┌───▼────┐┌──▼───┐┌───▼───┐
     │Gmail  │ │Calendar││Slack ││Google │
     │ API   │ │  API   ││ API  ││Drive  │
     └───────┘ └────────┘└──────┘└───────┘
```

Completa los detalles de cada componente en la siguiente tabla:

| Componente | Nombre concreto | Responsabilidad |
|------------|----------------|-----------------|
| Host | Claude Desktop (aplicación de escritorio de Anthropic) | Alojar al cliente MCP, gestionar la interfaz de usuario y el ciclo de vida de los servidores MCP |
| LLM | Claude (modelo de Anthropic) | Analizar la pregunta del usuario, decidir qué herramientas invocar y con qué parámetros, y generar la respuesta final |
| Cliente MCP | Cliente MCP integrado en Claude Desktop | Orquestar las conexiones 1:1 con cada servidor MCP, descubrir herramientas disponibles, traducir peticiones del LLM a JSON-RPC y devolver resultados |
| Servidor MCP 1 | Servidor MCP de Gmail | Exponer herramientas para leer, enviar y gestionar correos electrónicos conectándose a la Gmail API |
| Servidor MCP 2 | Servidor MCP de Google Calendar | Exponer herramientas para consultar, crear y modificar eventos conectándose a la Google Calendar API |
| Servidor MCP 3 | Servidor MCP de Slack | Exponer herramientas para enviar mensajes y leer canales conectándose a la Slack API |
| Servidor MCP 4 | Servidor MCP de Google Drive | Exponer herramientas para acceder, buscar y gestionar documentos conectándose a la Google Drive API |

### Parte B: Comparación con Arquitectura Acoplada (10 min)

Ahora imagina que no existiera MCP. Dibuja cómo sería la integración directa (acoplada) donde el LLM necesita conectores específicos para cada servicio.

Responde las siguientes preguntas:

1. **Número de integraciones**: Si tienes 3 clientes de IA diferentes (Claude, ChatGPT, Gemini) y 4 servicios (Gmail, Calendar, Slack, Drive), ¿cuántas integraciones punto a punto necesitas? ¿Y con MCP?

   **Respuesta:** Sin MCP se necesitan 3 x 4 = **12 integraciones** punto a punto (cada cliente debe implementar un conector específico para cada servicio). Con MCP se necesitan solo 3 + 4 = **7 componentes** (3 clientes MCP + 4 servidores MCP), ya que cada cliente se conecta a cualquier servidor a través del protocolo estándar.

2. **Coste de mantenimiento**: Si Gmail cambia su API, ¿cuántos componentes hay que actualizar en cada modelo?

   **Respuesta:** Sin MCP hay que actualizar **3 componentes** (el conector de Gmail dentro de cada uno de los 3 clientes). Con MCP solo hay que actualizar **1 componente**: el servidor MCP de Gmail. Los 3 clientes siguen funcionando sin cambios porque se comunican con el servidor vía JSON-RPC estándar, no directamente con la API de Gmail.

3. **Escalabilidad**: Si añades un quinto servicio (ej: Notion), ¿cuántas integraciones nuevas requiere cada modelo?

   **Respuesta:** Sin MCP se necesitan **3 integraciones nuevas** (una por cada cliente). Con MCP solo se necesita **1 integración nueva**: crear el servidor MCP de Notion. Los 3 clientes existentes pueden usarlo automáticamente sin modificación.

Completa la tabla comparativa:

| Aspecto | Sin MCP (acoplado) | Con MCP |
|---------|-------------------|---------|
| Integraciones necesarias (3 clientes × 4 servicios) | 12 integraciones (N×M = 3×4) | 7 componentes (N+M = 3+4) |
| Cambio en API de Gmail afecta a... | Los 3 clientes (hay que actualizar el conector de Gmail en cada uno) | Solo al servidor MCP de Gmail (1 componente) |
| Añadir 1 servicio nuevo requiere... | 3 integraciones nuevas (una por cliente) | 1 servidor MCP nuevo (los clientes lo usan automáticamente) |
| Añadir 1 cliente nuevo requiere... | 4 integraciones nuevas (una por servicio) | 1 cliente MCP nuevo (se conecta a los 4 servidores existentes) |
| ¿Quién mantiene la integración? | Cada equipo de cada cliente mantiene todas las integraciones | El proveedor del servicio o la comunidad mantiene su servidor MCP; los clientes solo mantienen el protocolo MCP |


### Extensión (Opcional)
Investiga si existen servidores MCP reales para cada uno de los 4 servicios mencionados. Busca en [mcpservers.org](https://mcpservers.org) o en el [repositorio oficial de Anthropic](https://github.com/modelcontextprotocol/servers). Indica para cada uno: nombre del servidor, autor y si es oficial o comunitario.

---

## Ejercicio 2: Configuración del Servidor Filesystem en Claude Desktop

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Tener Claude Desktop instalado, Node.js (v18+) instalado, lectura de la sección 6.2 sobre configuración de servidores locales

### Contexto
El servidor Filesystem es uno de los servidores MCP oficiales más utilizados. Permite que Claude acceda al sistema de archivos local para leer, escribir, buscar y organizar archivos. Configurar este servidor es el punto de partida ideal para entender cómo funciona MCP en la práctica: editarás el archivo de configuración JSON de Claude Desktop, arrancarás el servidor mediante STDIO y verificarás que las herramientas aparecen disponibles en la interfaz.

### Objetivo de Aprendizaje
- Localizar y editar el archivo de configuración `claude_desktop_config.json`
- Configurar un servidor MCP basado en STDIO con `npx`
- Comprender los parámetros de configuración: `command`, `args` y `env`
- Verificar que las herramientas del servidor aparecen en Claude Desktop
- Probar operaciones básicas de lectura y escritura de archivos

### Enunciado

### Paso 1: Localizar el Archivo de Configuración (3 min)

El archivo de configuración de Claude Desktop se encuentra en una ubicación específica según tu sistema operativo:

| Sistema Operativo | Ruta del archivo |
|-------------------|-----------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |

1. Abre una terminal y verifica que el archivo existe:

**macOS:**
```bash
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows (PowerShell):**
```powershell
Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"
```

2. Si el archivo no existe, créalo con un contenido JSON vacío:
```bash
echo '{}' > ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Paso 2: Configurar el Servidor Filesystem (10 min)

1. Abre el archivo de configuración en tu editor favorito:

```bash
# macOS
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# O con cualquier editor de texto
open -a TextEdit ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. Escribe la siguiente configuración, sustituyendo las rutas por las de tu sistema:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/tu_usuario/Documents",
        "/Users/tu_usuario/Desktop"
      ]
    }
  }
}
```

> **Importante**: Las rutas que pasas como argumentos son los directorios a los que Claude tendrá acceso. Solo podrá leer y escribir dentro de estas carpetas. Esto es un mecanismo de seguridad fundamental.

3. Guarda el archivo.

### Paso 3: Reiniciar Claude Desktop y Verificar (5 min)

1. Cierra completamente Claude Desktop (no solo la ventana, sino la aplicación)
2. Vuelve a abrir Claude Desktop
3. En una nueva conversación, busca el icono de herramientas (martillo/llave) en la parte inferior del campo de texto
4. Haz clic en él: deberías ver las herramientas del servidor filesystem listadas:
   - `read_file` - Leer el contenido de un archivo
   - `write_file` - Escribir contenido en un archivo
   - `list_directory` - Listar el contenido de un directorio
   - `create_directory` - Crear un nuevo directorio
   - `move_file` - Mover o renombrar un archivo
   - `search_files` - Buscar archivos por nombre
   - `read_multiple_files` - Leer varios archivos a la vez
   - `get_file_info` - Obtener metadatos de un archivo
   - `list_allowed_directories` - Ver los directorios permitidos

### Paso 4: Probar Operaciones Básicas (12 min)

Escribe los siguientes prompts en Claude Desktop y verifica que funcionan correctamente:

**Prueba 1 - Listar archivos:**
```
Lista los archivos que hay en mi carpeta Documents
```
Resultado esperado: Claude invocará `list_directory` y mostrará el contenido.

**Prueba 2 - Crear un archivo:**
```
Crea un archivo llamado "prueba_mcp.txt" en mi escritorio con el texto:
"Este archivo fue creado por Claude usando MCP - Filesystem Server"
```
Resultado esperado: Claude invocará `write_file` y confirmará la creación. Verifica manualmente que el archivo existe en tu escritorio.

**Prueba 3 - Leer un archivo:**
```
Lee el contenido del archivo prueba_mcp.txt que acabamos de crear en el escritorio
```
Resultado esperado: Claude invocará `read_file` y mostrará el contenido.

**Prueba 4 - Buscar archivos:**
```
Busca todos los archivos con extensión .pdf en mi carpeta Documents
```
Resultado esperado: Claude invocará `search_files` y listará los PDFs encontrados.

Verificaciones:
- El icono de herramientas muestra 9 herramientas del servidor filesystem
- Las 4 pruebas se ejecutan correctamente, con Claude pidiendo permiso antes de cada operación
- El archivo `prueba_mcp.txt` existe físicamente en el escritorio

**Errores comunes y solución:**

| Error | Causa probable | Solución |
|-------|---------------|----------|
| No aparecen herramientas | JSON mal formado | Validar el JSON en [jsonlint.com](https://jsonlint.com) |
| `npx: command not found` | Node.js no instalado | Instalar Node.js desde [nodejs.org](https://nodejs.org) |
| `Error: Access denied` | Ruta no incluida en args | Añadir la ruta al array de `args` |
| Servidor no arranca | Puerto o proceso bloqueado | Reiniciar Claude Desktop completamente |

### Extensión (Opcional)
Añade variables de entorno al servidor para personalizar su comportamiento. Investiga qué ocurre si añades el campo `"env"` a la configuración:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/tu_usuario/Documents"],
      "env": {
        "NODE_ENV": "development"
      }
    }
  }
}
```
Además, intenta restringir el acceso a una sola subcarpeta y verifica que Claude no puede acceder fuera de ella.

---

## Ejercicio 3: Exploración de Servidores MCP Públicos

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Exploración
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 6.3 sobre el ecosistema de servidores MCP y criterios de seguridad

### Contexto
El ecosistema MCP ha crecido rápidamente y ya cuenta con cientos de servidores disponibles, tanto oficiales (mantenidos por Anthropic) como comunitarios. Saber navegar este ecosistema, evaluar la calidad y seguridad de un servidor, y elegir el adecuado para cada caso de uso es una competencia clave. No todos los servidores son iguales: algunos están bien mantenidos y auditados, mientras que otros pueden suponer riesgos de seguridad.

### Objetivo de Aprendizaje
- Navegar los principales directorios de servidores MCP
- Clasificar servidores por categoría funcional
- Aplicar criterios de seguridad para evaluar servidores de terceros
- Desarrollar criterio propio para seleccionar servidores fiables

### Enunciado

### Parte A: Exploración y Clasificación (12 min)

1. Visita los siguientes recursos:
   - [mcpservers.org](https://mcpservers.org) - Directorio comunitario de servidores MCP
   - [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) - Repositorio oficial de Anthropic
   - [mcp.so](https://mcp.so) - Otro directorio popular

2. Selecciona **10 servidores** y clasifícalos en la siguiente tabla:

| # | Nombre del Servidor | Categoría | Oficial/Comunitario | Descripción breve |
|---|-------------------|-----------|--------------------|--------------------|
| 1 | filesystem | Productividad | Oficial (Anthropic) | Acceso al sistema de archivos local: leer, escribir, buscar y organizar archivos |
| 2 | github | Desarrollo | Oficial (Anthropic) | Integración con la API de GitHub: repos, issues, pull requests, commits |
| 3 | slack | Comunicación | Oficial (Anthropic) | Enviar mensajes, leer canales y gestionar conversaciones en Slack |
| 4 | google-drive | Productividad | Oficial (Anthropic) | Acceder, buscar y gestionar documentos en Google Drive |
| 5 | postgresql | Desarrollo | Oficial (Anthropic) | Consultar y gestionar bases de datos PostgreSQL |
| 6 | brave-search | Datos | Oficial (Anthropic) | Búsqueda en internet utilizando la API de Brave Search |
| 7 | memory | Productividad | Oficial (Anthropic) | Grafo de conocimiento persistente para almacenar entidades y relaciones entre sesiones |
| 8 | puppeteer | Datos | Oficial (Anthropic) | Automatización de navegador web: navegar páginas, hacer capturas, interactuar con elementos |
| 9 | sqlite | Desarrollo | Oficial (Anthropic) | Consultar y gestionar bases de datos SQLite locales |
| 10 | fetch | Datos | Oficial (Anthropic) | Obtener contenido de URLs externas mediante peticiones HTTP |

**Categorías sugeridas** (puedes crear las tuyas):
- Productividad (archivos, notas, calendario)
- Desarrollo (Git, bases de datos, CI/CD)
- Comunicación (email, mensajería, redes sociales)
- Datos (APIs, web scraping, análisis)
- Creatividad (imágenes, diseño, audio)
- Infraestructura (cloud, DevOps, monitorización)

### Parte B: Evaluación de Seguridad (13 min)

Selecciona **3 servidores comunitarios** de tu lista anterior y evalúalos según los siguientes criterios de seguridad. Puntúa cada criterio de 1 (muy bajo) a 5 (excelente):

| Criterio de Seguridad | Servidor 1: puppeteer | Servidor 2: filesystem | Servidor 3: fetch |
|-----------------------|---------------------|---------------------|---------------------|
| **Código abierto** (¿se puede auditar el código?) | 5 | 5 | 5 |
| **Estrellas en GitHub** (popularidad como proxy de confianza) | 5 | 5 | 5 |
| **Frecuencia de actualizaciones** (¿se mantiene activo?) | 4 | 5 | 4 |
| **Documentación** (¿explica qué permisos necesita?) | 4 | 5 | 4 |
| **Principio de mínimo privilegio** (¿pide solo los permisos necesarios?) | 3 | 5 | 3 |
| **Autor/Organización** (¿es una entidad reconocida?) | 5 | 5 | 5 |
| **Issues y respuesta** (¿se atienden reportes de bugs/seguridad?) | 4 | 5 | 4 |
| **Total** | 30 /35 | 35 /35 | 30 /35 |

Para cada servidor evaluado, responde:

**Servidor 1 - puppeteer:**
1. **¿Lo instalarías?** Sí, pero con precaución. Al ser oficial de Anthropic tiene alta confianza, pero la automatización del navegador puede exponer datos sensibles si se visitan páginas con información privada.
2. **Riesgos:** Puede navegar a cualquier URL, potencialmente exponiendo datos del navegador. Riesgo de prompt injection si el LLM navega a páginas con contenido malicioso que intente manipular sus acciones.
3. **Mitigación:** Limitar las URLs permitidas, ejecutar en un navegador aislado (perfil separado), no usar sesiones con credenciales guardadas.

**Servidor 2 - filesystem:**
1. **¿Lo instalarías?** Sí. Es el servidor más seguro si se configuran correctamente las rutas permitidas, ya que implementa sandboxing por directorio.
2. **Riesgos:** Si se configura con acceso a directorios sensibles (ej: `/`, `~/.ssh`, carpetas con credenciales), podría leer o sobrescribir archivos críticos.
3. **Mitigación:** Restringir las rutas al mínimo necesario (solo carpetas de proyecto), nunca dar acceso al directorio raíz o home completo, revisar los permisos de escritura.

**Servidor 3 - fetch:**
1. **¿Lo instalarías?** Sí, con reservas. Útil para obtener contenido web, pero permite conexiones salientes a cualquier URL.
2. **Riesgos:** Podría ser usado para exfiltrar datos si un atacante manipula al LLM vía prompt injection (ej: enviar datos sensibles a una URL controlada por el atacante). También puede acceder a servicios internos de la red.
3. **Mitigación:** Monitorizar las URLs a las que se conecta, bloquear rangos de IP internos/privados, limitar el tamaño de las respuestas.

### Solución Esperada

**Parte A - Ejemplo de clasificación:**

| # | Nombre del Servidor | Categoría | Oficial/Comunitario |
|---|-------------------|-----------|---------------------|
| 1 | filesystem | Productividad | Oficial |
| 2 | github | Desarrollo | Oficial |
| 3 | slack | Comunicación | Oficial |
| 4 | google-drive | Productividad | Oficial |
| 5 | postgresql | Desarrollo | Oficial |
| 6 | brave-search | Datos | Oficial |
| 7 | memory | Productividad | Oficial |
| 8 | puppeteer | Datos | Oficial |
| 9 | sqlite | Desarrollo | Oficial |
| 10 | fetch | Datos | Oficial |

**Parte B - Criterios clave de evaluación:**
- Un servidor con puntuación inferior a 20/35 debería usarse con precaución
- Los servidores oficiales de Anthropic parten con ventaja en autor y mantenimiento
- La presencia de documentación clara sobre permisos es un indicador fuerte de calidad
- Servidores que piden acceso a todo el sistema de archivos o a todas las APIs sin restricción son una señal de alarma

### Extensión (Opcional)
Encuentra un servidor MCP que consideres potencialmente peligroso o con malas prácticas de seguridad. Documenta qué señales de alarma identificas y cómo podría un atacante explotar ese servidor (ej: prompt injection a través de herramientas MCP, exfiltración de datos, ejecución arbitraria de código).

---

## Ejercicio 4: Análisis de Mensajes JSON-RPC en MCP

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 6.4 sobre el protocolo JSON-RPC 2.0 y las capas de transporte

### Contexto
MCP utiliza JSON-RPC 2.0 como formato de mensajes para la comunicación entre clientes y servidores. Entender este formato es esencial para depurar problemas, analizar logs y comprender qué sucede "bajo el capó" cuando Claude invoca una herramienta MCP. En este ejercicio analizarás un intercambio real de mensajes entre un cliente y un servidor MCP.

### Objetivo de Aprendizaje
- Identificar los tipos de mensajes JSON-RPC: petición, respuesta y notificación
- Comprender la estructura de cada tipo de mensaje (campos obligatorios y opcionales)
- Trazar el flujo completo de una invocación de herramienta MCP
- Detectar errores en mensajes JSON-RPC malformados

### Enunciado

### Parte A: Identificación de Mensajes (8 min)

A continuación se muestra un intercambio de mensajes entre un cliente MCP y un servidor Filesystem. Para cada mensaje, identifica:
- **Dirección**: ¿Cliente → Servidor o Servidor → Cliente?
- **Tipo**: ¿Petición (request), Respuesta (response) o Notificación (notification)?
- **Propósito**: ¿Qué está haciendo este mensaje?

**Mensaje 1:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {
        "listChanged": true
      }
    },
    "clientInfo": {
      "name": "Claude Desktop",
      "version": "1.2.0"
    }
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | Cliente → Servidor |
| Tipo | Petición (request) — tiene `id` y `method` |
| Propósito | Handshake inicial: el cliente inicia la conexión con el servidor, enviando su versión del protocolo, sus capacidades y su información de identificación |

**Mensaje 2:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "filesystem",
      "version": "0.5.0"
    }
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | Servidor → Cliente |
| Tipo | Respuesta (response) — tiene `id` y `result`, sin `method` |
| Propósito | Respuesta al handshake: el servidor confirma la versión del protocolo, anuncia sus capacidades (soporta tools) y se identifica como "filesystem" v0.5.0 |

**Mensaje 3:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

| Campo | Valor |
|-------|-------|
| Dirección | Cliente → Servidor |
| Tipo | Notificación (notification) — tiene `method` pero NO tiene `id` |
| Propósito | El cliente notifica al servidor que la inicialización se ha completado correctamente y está listo para operar. No espera respuesta (es una notificación) |

**Mensaje 4:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

| Campo | Valor |
|-------|-------|
| Dirección | Cliente → Servidor |
| Tipo | Petición (request) — tiene `id` y `method` |
| Propósito | El cliente solicita al servidor la lista de herramientas (tools) disponibles para poder informar al LLM de qué puede usar |

**Mensaje 5:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "read_file",
        "description": "Read the complete contents of a file",
        "inputSchema": {
          "type": "object",
          "properties": {
            "path": {
              "type": "string",
              "description": "Path to the file to read"
            }
          },
          "required": ["path"]
        }
      },
      {
        "name": "write_file",
        "description": "Write content to a file",
        "inputSchema": {
          "type": "object",
          "properties": {
            "path": { "type": "string" },
            "content": { "type": "string" }
          },
          "required": ["path", "content"]
        }
      }
    ]
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | Servidor → Cliente |
| Tipo | Respuesta (response) — tiene `id` y `result`, sin `method` |
| Propósito | El servidor responde con la lista de herramientas disponibles: `read_file` y `write_file`, incluyendo la descripción y el esquema de parámetros (inputSchema) de cada una |

**Mensaje 6:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/Users/alumno/Documents/notas.txt"
    }
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | Cliente → Servidor |
| Tipo | Petición (request) — tiene `id` y `method` |
| Propósito | El cliente invoca la herramienta `read_file` para leer el archivo `notas.txt` del directorio Documents del usuario |

**Mensaje 7:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Apuntes de la clase de MCP:\n- JSON-RPC 2.0\n- Transporte STDIO\n- Servidores locales"
      }
    ]
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | Servidor → Cliente |
| Tipo | Respuesta (response) — tiene `id` y `result` |
| Propósito | El servidor devuelve el contenido del archivo `notas.txt` leído exitosamente, con los apuntes de clase sobre MCP |

**Mensaje 8:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/etc/shadow"
    }
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | Cliente → Servidor |
| Tipo | Petición (request) — tiene `id` y `method` |
| Propósito | El cliente intenta leer el archivo `/etc/shadow` (archivo de contraseñas del sistema), que está fuera de los directorios permitidos |

**Mensaje 9:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "error": {
    "code": -32602,
    "message": "Access denied: /etc/shadow is not within allowed directories"
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | Servidor → Cliente |
| Tipo | Respuesta de error (response) — tiene `id` y `error` (en lugar de `result`) |
| Propósito | El servidor rechaza la petición con código -32602 (parámetros inválidos) porque la ruta `/etc/shadow` está fuera de los directorios permitidos. Esto demuestra el mecanismo de sandboxing de seguridad |

### Parte B: Flujo Completo (7 min)

Ordena los mensajes anteriores en un diagrama de secuencia. Dibuja las flechas indicando la dirección:

```
  CLIENTE                         SERVIDOR
    │                                │
    │──── Mensaje 1: initialize ────▶│   (Petición: handshake inicial)
    │◀─── Mensaje 2: result init ────│   (Respuesta: confirmación + capacidades)
    │──── Mensaje 3: initialized ───▶│   (Notificación: listo para operar)
    │──── Mensaje 4: tools/list ────▶│   (Petición: solicitar herramientas)
    │◀─── Mensaje 5: result tools ───│   (Respuesta: lista de tools)
    │──── Mensaje 6: tools/call ────▶│   (Petición: read_file notas.txt)
    │◀─── Mensaje 7: result file ────│   (Respuesta: contenido del archivo)
    │──── Mensaje 8: tools/call ────▶│   (Petición: read_file /etc/shadow)
    │◀─── Mensaje 9: error ──────────│   (Respuesta error: acceso denegado)
    │                                │
```

### Parte C: Detección de Errores (5 min)

Los siguientes mensajes JSON-RPC contienen errores. Identifica qué está mal en cada uno:

**Mensaje erróneo A:**
```json
{
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": { "path": "/tmp/test.txt" }
  }
}
```

Error: Falta el campo obligatorio `"jsonrpc": "2.0"`. En JSON-RPC 2.0 este campo es obligatorio en todos los mensajes para identificar la versión del protocolo.

**Mensaje erróneo B:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": { "path": "/tmp/test.txt" }
  }
}
```

Error: Falta el campo `"id"`. Sin `id` este mensaje sería una notificación, pero `tools/call` es una petición que espera respuesta del servidor. Sin `id`, el servidor no podría correlacionar la respuesta con esta petición.

**Mensaje erróneo C:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": { "content": "texto" },
  "error": { "code": -32600, "message": "Invalid request" }
}
```

Error: Un mensaje JSON-RPC no puede contener simultáneamente los campos `result` y `error`. Una respuesta debe tener uno u otro, nunca ambos. Si la operación fue exitosa se incluye `result`; si falló se incluye `error`.

**Parte C - Errores:**
- **Mensaje A**: Falta el campo `"jsonrpc": "2.0"` (obligatorio en JSON-RPC 2.0)
- **Mensaje B**: Falta el campo `"id"`. Sin `id` sería una notificación, pero `tools/call` es una petición que espera respuesta, por lo que necesita un identificador
- **Mensaje C**: Un mensaje no puede contener simultáneamente `result` y `error`. Debe tener uno u otro, nunca ambos

### Extensión (Opcional)
Escribe tú mismo la secuencia completa de mensajes JSON-RPC que se intercambiarían si Claude invocara la herramienta `write_file` para crear un archivo nuevo. Incluye: petición del cliente, respuesta exitosa del servidor, y cómo sería la respuesta si el disco estuviera lleno (código de error `-32603` para error interno).

---

## Ejercicio 5: Configuración Multi-Servidor en Claude Desktop

### Metadata
- **Duración estimada**: 35 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Haber completado el Ejercicio 2, lectura de las secciones 6.2 y 6.5 sobre configuración de servidores y transporte STDIO

### Contexto
El verdadero poder de MCP se manifiesta cuando un mismo cliente conecta con múltiples servidores simultáneamente. En este escenario, Claude Desktop actúa como host que mantiene múltiples conexiones 1:1, y el LLM puede combinar herramientas de distintos servidores para resolver tareas complejas. Por ejemplo, puede leer un archivo (servidor filesystem), guardar información relevante (servidor memory) y buscar contexto adicional en la web (servidor brave-search), todo dentro de la misma conversación.

### Objetivo de Aprendizaje
- Configurar múltiples servidores MCP en un solo archivo de configuración
- Comprender que cada servidor se ejecuta como un proceso independiente
- Verificar que Claude puede combinar herramientas de distintos servidores
- Documentar una configuración completa y funcional

### Enunciado

### Paso 1: Planificación de Servidores (5 min)

Vas a configurar Claude Desktop con **tres servidores MCP** que trabajarán en conjunto:

| Servidor | Paquete npm | Función |
|----------|-------------|---------|
| **Filesystem** | `@modelcontextprotocol/server-filesystem` | Acceso al sistema de archivos local |
| **Memory** | `@modelcontextprotocol/server-memory` | Grafo de conocimiento persistente (entidades y relaciones) |
| **Brave Search** | `@modelcontextprotocol/server-brave-search` | Búsqueda en internet vía API de Brave |

> **Nota**: Para Brave Search necesitarás una API key gratuita. Si no la tienes, puedes sustituirlo por otro servidor como `@modelcontextprotocol/server-fetch` (que obtiene contenido de URLs) y no requiere API key.

**Respuesta - Planificación:**

Los tres servidores se ejecutarán como procesos independientes, cada uno con su propia conexión STDIO con Claude Desktop. Cada servidor expone un conjunto diferente de herramientas, y el LLM puede combinarlas en una misma conversación:

| Servidor | Proceso independiente | Transporte | Herramientas clave | Requiere credenciales |
|----------|----------------------|------------|--------------------|-----------------------|
| Filesystem | Sí (proceso Node.js) | STDIO | `read_file`, `write_file`, `list_directory` | No (solo rutas permitidas) |
| Memory | Sí (proceso Node.js) | STDIO | `create_entities`, `read_graph`, `add_observations` | No |
| Fetch | Sí (proceso Node.js) | STDIO | `fetch` | No |

Se elige `fetch` en lugar de `brave-search` porque no requiere API key, facilitando la configuración inicial.

### Paso 2: Escribir la Configuración JSON (15 min)

Edita tu archivo `claude_desktop_config.json` para incluir los tres servidores. Utiliza la siguiente plantilla y complétala con tus rutas y credenciales:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/tu_usuario/Documents/mcp_workspace"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "TU_API_KEY_AQUI"
      }
    }
  }
}
```

**Alternativa sin API key** (sustituye `brave-search` por `fetch`):

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/tu_usuario/Documents/mcp_workspace"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch"
      ]
    }
  }
}
```

Antes de guardar, verifica que tu JSON es válido:
1. Asegúrate de que no hay comas finales después del último elemento
2. Todas las llaves y corchetes están correctamente cerrados
3. Las cadenas de texto usan comillas dobles

**Respuesta - Configuración concreta para Windows (usando fetch):**

El archivo se ubica en `%APPDATA%\Claude\claude_desktop_config.json`. Ejemplo concreto:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/Users/alvar/Documents/mcp_workspace"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch"
      ]
    }
  }
}
```

**Verificación del JSON:**
- No hay comas tras `"fetch": { ... }` (último servidor) ni tras el último elemento dentro de cada bloque
- Todas las llaves `{}` y corchetes `[]` están correctamente emparejados (3 niveles de anidación)
- Todas las cadenas usan comillas dobles `""`
- Las rutas en Windows usan barras `/` (también válidas en JSON) en lugar de `\` para evitar problemas de escape

### Paso 3: Crear el Directorio de Trabajo (2 min)

Crea un directorio dedicado para este ejercicio:

```bash
mkdir -p ~/Documents/mcp_workspace
echo "Archivo de prueba para MCP" > ~/Documents/mcp_workspace/readme.txt
```

**Respuesta - Comandos adaptados a Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\Documents\mcp_workspace"
Set-Content -Path "$HOME\Documents\mcp_workspace\readme.txt" -Value "Archivo de prueba para MCP"
```

Esto crea la carpeta `mcp_workspace` dentro de Documentos y un archivo `readme.txt` con un texto de prueba. Este será el directorio al que el servidor filesystem tendrá acceso.

### Paso 4: Reiniciar y Verificar (5 min)

1. Reinicia Claude Desktop completamente
2. Abre una nueva conversación
3. Haz clic en el icono de herramientas: deberías ver herramientas de los **tres servidores**
4. Verifica contando las herramientas disponibles:

| Servidor | Herramientas esperadas |
|----------|----------------------|
| Filesystem | `read_file`, `write_file`, `list_directory`, `create_directory`, `move_file`, `search_files`, `read_multiple_files`, `get_file_info`, `list_allowed_directories` |
| Memory | `create_entities`, `create_relations`, `add_observations`, `delete_entities`, `delete_observations`, `delete_relations`, `read_graph`, `search_nodes`, `open_nodes` |
| Brave Search / Fetch | `brave_web_search`, `brave_local_search` / `fetch` |

**Respuesta - Verificación:**

Tras reiniciar Claude Desktop, en el icono de herramientas deberíamos ver un total de **9 + 9 + 1 = 19 herramientas** (con la configuración de fetch). Cada servidor arranca como un proceso independiente de Node.js que Claude Desktop gestiona automáticamente. Si algún servidor no aparece:

1. Abrir los logs en `%APPDATA%\Claude\logs\` para ver el error concreto
2. Verificar que `npx` está disponible ejecutando `npx --version` en la terminal
3. Validar el JSON del archivo de configuración con un validador online
4. Comprobar que la ruta de `mcp_workspace` existe y es accesible

### Paso 5: Prueba de Integración Multi-Servidor (8 min)

Ejecuta el siguiente flujo de trabajo que combina herramientas de los tres servidores:

**Prompt 1** (Filesystem + Memory):
```
Lee el archivo readme.txt de mi carpeta mcp_workspace.
Luego, guarda en tu memoria que existe un proyecto llamado
"Ejercicio MCP" con la descripción que encontraste en el archivo.
```

Resultado esperado: Claude usará `read_file` (filesystem) y luego `create_entities` (memory).

**Respuesta - Prompt 1:**

Claude ejecutará dos herramientas de dos servidores distintos en secuencia:

1. **`read_file`** (servidor filesystem): Lee `C:/Users/alvar/Documents/mcp_workspace/readme.txt` y obtiene el contenido `"Archivo de prueba para MCP"`.
2. **`create_entities`** (servidor memory): Crea una entidad en el grafo de conocimiento con los datos:
   ```json
   {
     "entities": [
       {
         "name": "Ejercicio MCP",
         "entityType": "project",
         "observations": ["Archivo de prueba para MCP"]
       }
     ]
   }
   ```

Esto demuestra la **composición multi-servidor**: el resultado de un servidor (filesystem) alimenta la acción de otro (memory).

**Prompt 2** (Brave Search / Fetch + Memory):
```
Busca en internet qué es el Model Context Protocol.
Guarda en tu memoria las 3 ideas principales que encuentres
como observaciones de una entidad llamada "MCP".
```

Resultado esperado: Claude usará `brave_web_search` o `fetch` y luego `create_entities` + `add_observations` (memory).

**Respuesta - Prompt 2:**

Claude ejecutará herramientas de dos servidores:

1. **`fetch`** (servidor fetch): Obtiene contenido de una URL sobre MCP (por ejemplo, la documentación oficial de Anthropic o la página del repositorio modelcontextprotocol).
2. **`create_entities`** + **`add_observations`** (servidor memory): Crea la entidad "MCP" y le añade 3 observaciones, por ejemplo:
   ```json
   {
     "entities": [
       {
         "name": "MCP",
         "entityType": "technology",
         "observations": [
           "MCP es un estándar abierto creado por Anthropic para conectar LLMs con herramientas externas",
           "Utiliza una arquitectura cliente-servidor con protocolo JSON-RPC 2.0",
           "Reduce la complejidad de integraciones de N×M a N+M mediante desacoplamiento"
         ]
       }
     ]
   }
   ```

Si se usa `brave-search` en vez de `fetch`, Claude invocará `brave_web_search` con una query como "Model Context Protocol MCP Anthropic" y luego almacenará las ideas principales.

**Prompt 3** (Memory + Filesystem):
```
Recupera todo lo que tienes guardado en tu memoria sobre MCP.
Genera un resumen y guárdalo como un archivo "resumen_mcp.md"
en la carpeta mcp_workspace.
```

Resultado esperado: Claude usará `read_graph` (memory) y luego `write_file` (filesystem).

**Respuesta - Prompt 3:**

Claude ejecutará herramientas en orden inverso al Prompt 1 (ahora lee de memory y escribe en filesystem):

1. **`read_graph`** (servidor memory): Recupera todas las entidades y relaciones almacenadas. Obtendrá las entidades "Ejercicio MCP" y "MCP" con sus observaciones.
2. **`write_file`** (servidor filesystem): Genera un resumen en formato Markdown y lo escribe en `C:/Users/alvar/Documents/mcp_workspace/resumen_mcp.md`. El contenido sería algo como:

   ```markdown
   # Resumen sobre MCP

   ## Proyecto: Ejercicio MCP
   - Archivo de prueba para MCP

   ## Tecnología: MCP (Model Context Protocol)
   - MCP es un estándar abierto creado por Anthropic para conectar LLMs con herramientas externas
   - Utiliza una arquitectura cliente-servidor con protocolo JSON-RPC 2.0
   - Reduce la complejidad de integraciones de N×M a N+M mediante desacoplamiento
   ```

Este prompt demuestra el flujo inverso: la información que entró por filesystem y fetch, almacenada en memory, ahora sale de memory y se persiste de nuevo en filesystem como un archivo Markdown.

**Prompt 4** (Verificación):
```
Lee el archivo resumen_mcp.md que acabamos de crear.
```

**Respuesta - Prompt 4:**

Claude invocará **`read_file`** (servidor filesystem) con la ruta `C:/Users/alvar/Documents/mcp_workspace/resumen_mcp.md` y mostrará el contenido del resumen generado en el Prompt 3, verificando que todo el flujo multi-servidor funcionó correctamente.

**Conclusión del ejercicio:** Este flujo demuestra que los tres servidores MCP trabajan de forma completamente independiente pero coordinada por el LLM. Cada servidor es un proceso aparte, se comunica con Claude Desktop vía STDIO usando JSON-RPC 2.0, y el LLM es quien decide qué herramienta de qué servidor usar en cada momento. El cliente MCP (Claude Desktop) orquesta todas las conexiones de forma transparente.

## Resumen de Ejercicios

| Ejercicio | Duración | Tipo | Dificultad | Tema principal |
|-----------|----------|------|------------|----------------|
| 1. Análisis de Arquitectura MCP | 20 min | Análisis | Básica | Componentes y flujo N+M vs N×M |
| 2. Configuración Servidor Filesystem | 30 min | Programación | Intermedia | Primer servidor MCP en Claude Desktop |
| 3. Exploración de Servidores Públicos | 25 min | Exploración | Básica | Ecosistema y evaluación de seguridad |
| 4. Análisis de JSON-RPC | 20 min | Análisis | Básica | Protocolo de comunicación MCP |
| 5. Configuración Multi-Servidor | 35 min | Programación | Intermedia | Múltiples servidores trabajando juntos |
| **Total** | **130 min** | | | |
