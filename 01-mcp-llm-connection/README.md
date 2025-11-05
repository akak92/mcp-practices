# 01-mcp-llm-connection

## Descripción
Esta carpeta contiene un ejemplo avanzado de **Model Context Protocol (MCP)** que demuestra la integración entre un servidor MCP y un **LLM local** (qwen3:1.7b via Ollama) usando un **BFF proxy**. Este proyecto muestra cómo los LLMs pueden descubrir y utilizar herramientas MCP de forma inteligente y autónoma.

## ¿Qué es este Proyecto?
Este ejemplo implementa un flujo completo donde:
1. Un **servidor MCP** expone herramientas disponibles
2. Un **cliente inteligente** conecta el servidor MCP con un LLM local
3. El **LLM** puede descubrir, analizar y ejecutar herramientas según las consultas del usuario
4. Todo funciona **localmente** sin enviar datos a servicios externos

## Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Usuario       │───▶│  Cliente MCP    │───▶│  BFF Proxy      │───▶│ Ollama (qwen3)  │
│   "Suma 15+25"  │    │  (client.py)    │    │ localhost:9900  │    │ LLM Local       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                               │                        ▲
                               ▼                        │
                       ┌─────────────────┐             │
                       │  Servidor MCP   │─────────────┘
                       │  (server.py)    │ Ejecuta herramientas
                       └─────────────────┘
```

## Estructura del Proyecto

```
01-mcp-llm-connection/
├── server.py          # Servidor MCP con herramientas
├── client.py          # Cliente inteligente con integración LLM
├── utils/             # Módulos de utilidades
│   ├── __init__.py    # Inicialización del módulo
│   └── tools.py       # Herramientas matemáticas
├── requirements.txt   # Dependencias Python
├── Dockerfile         # Imagen Docker optimizada
├── .dockerignore      # Archivos a ignorar en Docker
├── run_docker.ps1     # Script Docker para Windows
└── run_docker.sh      # Script Docker para Unix
```

## Componentes Principales

### 1. Servidor MCP (`server.py`)
Servidor simplificado que expone:
- **Herramienta**: `add_tool(a: int, b: int)` - Suma dos números
- **Protocolo**: FastMCP con comunicación stdio
- **Propósito**: Demostrar cómo un LLM puede usar herramientas externas

### 2. Cliente Inteligente (`client.py`)
El componente más complejo que implementa:

#### **Funcionalidades Principales:**
- **Conexión MCP**: Se conecta al servidor via stdio
- **Integración LLM**: Comunica con qwen3 via BFF proxy
- **Conversión de Esquemas**: Adapta herramientas MCP al formato OpenAI Functions
- **Detección Inteligente**: Analiza respuestas del LLM para identificar uso de herramientas
- **Ejecución Automática**: Ejecuta herramientas detectadas y devuelve resultados
- **Logging Profesional**: Sistema de logs estructurado con timestamps

#### **Flujo de Procesamiento:**
```python
async def run():
    # 1. Conectar al servidor MCP
    # 2. Descubrir herramientas disponibles
    # 3. Convertir esquemas para el LLM
    # 4. Enviar consulta al LLM con contexto de herramientas
    # 5. Analizar respuesta del LLM
    # 6. Detectar y ejecutar herramientas mencionadas
    # 7. Mostrar resultados finales
```

### 3. BFF Proxy Integration
El cliente se comunica con un **Backend for Frontend (BFF)** que actúa como proxy hacia Ollama:

```python
async def call_llm(prompt, functions):
    url = "http://localhost:9900/chat"
    payload = {
        "model": "qwen3:1.7b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    # El BFF maneja la comunicación con Ollama
```

**Formato de Respuesta del BFF:**
```json
{
    "content": "Usé la herramienta add_tool con parámetros a=15 y b=25. El resultado es 40.",
    "model": "qwen3:1.7b",
    "usage": {"model": "qwen3:1.7b"}
}
```

### 4. Sistema de Logging
Implementación profesional de logging:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Tipos de Logs:**
- `✅ Connected to MCP server` - Conexión exitosa
- `🔧 LISTING TOOLS` - Descubrimiento de herramientas
- `🤖 CALLING BFF PROXY` - Comunicación con LLM
- `💬 LLM Response` - Respuestas del modelo
- `🎯 Detected tool usage` - Detección de uso de herramientas

## Requisitos del Sistema

### Software Necesario
- **Python 3.8+**
- **Ollama** con modelo qwen3:1.7b
- **BFF Proxy** ejecutándose en `localhost:9900`
- **Docker** (opcional, para containerización)

### Dependencias Python
```
fastmcp
httpx
asyncio
logging
```

## Instalación y Configuración

### 1. Configurar Ollama
```bash
# Instalar Ollama
# Descargar modelo qwen3:1.7b
ollama pull qwen3:1.7b

# Verificar que funciona
ollama run qwen3:1.7b
```

### 2. Configurar BFF Proxy
El BFF debe estar ejecutándose en `localhost:9900` y aceptar requests POST a `/chat`.

### 3. Instalación Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el proyecto
python client.py
```

### 4. Usando Docker
```bash
# Construir imagen
docker build -t mcp-llm-client .

# Ejecutar con acceso a localhost
docker run --rm --network="host" mcp-llm-client
```

## Flujo de Funcionamiento Detallado

### Fase 1: Inicialización
1. **Cliente** se conecta al **Servidor MCP** via stdio
2. **Cliente** descubre herramientas disponibles (`add_tool`)
3. **Cliente** convierte esquemas MCP al formato OpenAI Functions

### Fase 2: Procesamiento de Consulta
1. **Usuario** hace una pregunta: *"Can you help me add 15 and 25?"*
2. **Cliente** envía consulta al **LLM** via **BFF Proxy**
3. **LLM** analiza la consulta y el contexto de herramientas disponibles
4. **LLM** responde indicando qué herramienta usar y con qué parámetros

### Fase 3: Ejecución Inteligente
1. **Cliente** analiza la respuesta del **LLM** con regex/parsing
2. **Cliente** detecta: *"add_tool con parámetros a=15 y b=25"*
3. **Cliente** ejecuta la herramienta en el **Servidor MCP**
4. **Servidor** procesa `add_tool(15, 25)` y devuelve `40`

### Fase 4: Resultado Final
1. **Cliente** recibe el resultado de la herramienta
2. **Cliente** muestra tanto la respuesta del **LLM** como el resultado real
3. **Logging** registra todo el flujo para debugging

## Ejemplo de Ejecución

### Input del Usuario:
```
Can you help me add 15 and 25?
```

### Logs del Sistema:
```
2025-11-05 01:31:28,770 - __main__ - INFO - ✅ Connected to MCP server
2025-11-05 01:31:28,774 - __main__ - INFO - 📁 LISTING RESOURCES
2025-11-05 01:31:28,778 - __main__ - INFO - 🔧 LISTING TOOLS
2025-11-05 01:31:28,778 - __main__ - INFO - Tool: add_tool - Add two numbers
2025-11-05 01:31:28,778 - __main__ - INFO - 🎯 User Query: Can you help me add 15 and 25?
2025-11-05 01:31:28,778 - __main__ - INFO - 🤖 CALLING BFF PROXY at http://localhost:9900/chat
2025-11-05 01:31:36,791 - __main__ - INFO - 💬 LLM Response: Usé la herramienta add_tool con parámetros a=15 y b=25. El resultado es 40.
2025-11-05 01:31:36,791 - __main__ - INFO - 🎯 Detected add_tool usage with numbers: 15 + 25
2025-11-05 01:31:36,791 - __main__ - INFO - 🔧 Executing 1 tool call(s):
2025-11-05 01:31:36,801 - __main__ - INFO - Result: 40
```

### Output Final:
```
LLM Response: Usé la herramienta add_tool con parámetros a=15 y b=25. El resultado es 40.
Tool Result: 40
```

## Características Técnicas Avanzadas

### 1. Conversión de Esquemas
El cliente convierte automáticamente esquemas MCP al formato OpenAI Functions:

```python
def convert_to_llm_tool(tool):
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema.get("properties", {}),
                "required": list(tool.inputSchema.get("properties", {}).keys())
            }
        }
    }
```

### 2. Detección Inteligente de Herramientas
Usa regex para detectar uso de herramientas en respuestas del LLM:

```python
# Detecta patrones como "add_tool con parámetros a=15 y b=25"
tool_pattern = r'add_tool.*?a=(\d+).*?b=(\d+)'
match = re.search(tool_pattern, llm_response)
```

### 3. Manejo de Errores Robusto
- Timeout handling para requests HTTP
- Fallback si el LLM no usa herramientas
- Logging detallado para debugging
- Validación de parámetros de herramientas

### 4. Dockerización con Host Networking
```dockerfile
# Permite acceso a localhost desde el contenedor
docker run --network="host" mcp-llm-client
```

## Casos de Uso

### 1. **Asistente Matemático Local**
- Usuario pregunta operaciones matemáticas
- LLM identifica la operación necesaria
- Sistema ejecuta cálculos precisos

### 2. **Prototipo de IA Tool-Using**
- Demostrar capacidades de LLMs para usar herramientas
- Testing de integración MCP-LLM
- Desarrollo de sistemas de IA más complejos

### 3. **Educación en MCP**
- Entender cómo LLMs pueden usar herramientas externas
- Aprender patrones de integración MCP
- Base para proyectos más avanzados

## Ventajas del Enfoque

### ✅ **Privacidad Total**
- Todo funciona localmente
- No se envían datos a servicios externos
- Control completo sobre el procesamiento

### ✅ **Extensibilidad**
- Fácil agregar nuevas herramientas al servidor MCP
- LLM automáticamente las descubre y puede usarlas
- Arquitectura modular y escalable

### ✅ **Observabilidad**
- Logging detallado de todo el flujo
- Debugging fácil con timestamps
- Visibilidad completa del proceso

### ✅ **Containerización**
- Deploy fácil con Docker
- Ambiente reproducible
- Aislamiento de dependencias

## Próximos Pasos y Mejoras

### 🚀 **Expansión de Herramientas**
- Agregar más herramientas matemáticas
- Implementar herramientas de texto
- Conectar con APIs externas

### 🚀 **Mejora de IA**
- Usar modelos más grandes
- Implementar chain-of-thought
- Agregar memoria conversacional

### 🚀 **Optimización**
- Caching de respuestas
- Paralelización de herramientas
- Optimización de prompts

### 🚀 **Monitoreo**
- Métricas de performance
- Alertas de errores
- Dashboard de uso

## Conclusión

Este proyecto demuestra una implementación exitosa de **MCP + LLM local**, creando un sistema que permite a un modelo de lenguaje descubrir y utilizar herramientas externas de forma inteligente, manteniendo todo el procesamiento local y con total control sobre los datos.