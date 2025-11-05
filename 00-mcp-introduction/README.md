# 00-mcp-introduction

## Descripción
Esta carpeta contiene un ejemplo básico de **Model Context Protocol (MCP)** usando FastMCP. Es un servidor MCP simple que demuestra cómo estructurar herramientas (tools) y recursos (resources) en un proyecto organizado con una arquitectura modular.

## ¿Qué es MCP?
**Model Context Protocol (MCP)** es un protocolo estándar para conectar modelos de lenguaje (LLMs) con fuentes de datos y herramientas externas. Permite que los LLMs accedan a información en tiempo real y ejecuten acciones sin necesidad de re-entrenar el modelo.

## Estructura del Proyecto

```
00-mcp-introduction/
├── server.py          # Servidor MCP principal
├── client.py          # Cliente de prueba para el servidor
├── utils/             # Módulos de utilidades
│   ├── __init__.py    # Inicialización del módulo
│   ├── tools.py       # Herramientas matemáticas
│   └── resources.py   # Recursos de mensajes
├── requirements.txt   # Dependencias Python
├── Dockerfile         # Imagen Docker
├── .dockerignore      # Archivos a ignorar en Docker
├── run_demo.ps1       # Script para Windows PowerShell
└── run_demo.sh        # Script para sistemas Unix
```

## Componentes Principales

### 1. Servidor MCP (`server.py`)
El archivo principal que:
- Crea una instancia de FastMCP
- Registra herramientas desde `utils.tools`
- Registra recursos desde `utils.resources`
- Expone las funcionalidades via protocolo MCP

**Herramientas disponibles:**
- `add_tool(a: int, b: int)`: Suma dos números
- `subtract_tool(a: int, b: int)`: Resta dos números

**Recursos disponibles:**
- `greeting://{name}`: Genera un saludo personalizado
- `farewell://{name}`: Genera una despedida personalizada

### 2. Cliente de Prueba (`client.py`)
Un cliente simple que:
- Se conecta al servidor MCP via stdio
- Lista herramientas y recursos disponibles
- Ejecuta pruebas de las funcionalidades
- Demuestra cómo interactuar con el servidor

### 3. Módulo de Herramientas (`utils/tools.py`)
Contiene las funciones matemáticas básicas:
```python
def add(a: int, b: int) -> int:
    """Suma dos números"""
    return a + b

def subtract(a: int, b: int) -> int:
    """Resta dos números"""
    return a - b
```

### 4. Módulo de Recursos (`utils/resources.py`)
Contiene funciones para generar mensajes:
```python
def get_greeting(name: str) -> str:
    """Genera un saludo personalizado"""
    return f"¡Hola, {name}! Bienvenido al servidor MCP."

def get_farewell(name: str) -> str:
    """Genera una despedida personalizada"""
    return f"¡Adiós, {name}! Gracias por usar el servidor MCP."
```

## Instalación y Uso

### Requisitos
- Python 3.8+
- Dependencias en `requirements.txt`

### Instalación Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor (en una terminal)
python server.py

# Ejecutar el cliente (en otra terminal)
python client.py
```

### Usando Scripts de Demostración
```bash
# Windows PowerShell
.\run_demo.ps1

# Linux/Mac
./run_demo.sh
```

### Usando Docker
```bash
# Construir la imagen
docker build -t mcp-basic-demo .

# Ejecutar el contenedor
docker run --rm mcp-basic-demo
```

## Flujo de Funcionamiento

1. **Inicialización**: El servidor FastMCP se inicializa con un nombre y descripción
2. **Registro de Herramientas**: Se registran las funciones matemáticas como herramientas MCP
3. **Registro de Recursos**: Se registran los generadores de mensajes como recursos MCP
4. **Conexión Cliente**: El cliente se conecta via stdio al servidor
5. **Descubrimiento**: El cliente lista las herramientas y recursos disponibles
6. **Ejecución**: El cliente puede llamar herramientas y acceder a recursos
7. **Respuesta**: El servidor procesa las solicitudes y devuelve resultados

## Casos de Uso

- **Aprendizaje**: Entender los conceptos básicos de MCP
- **Prototipado**: Base para desarrollar servidores MCP más complejos
- **Testing**: Probar conectividad y funcionalidad MCP
- **Ejemplo educativo**: Demostrar la arquitectura modular con utils/

## Tecnologías Utilizadas

- **FastMCP**: Framework simplificado para crear servidores MCP
- **Python asyncio**: Para operaciones asíncronas
- **Docker**: Containerización para fácil despliegue
- **Stdio**: Protocolo de comunicación estándar entre cliente y servidor

## Próximos Pasos

Para ejemplos más avanzados, consulta:
- `01-mcp-llm-connection/`: Integración MCP con LLMs locales
- Documentación oficial de MCP
- Ejemplos de herramientas más complejas