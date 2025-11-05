from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
import json
from datetime import datetime

app: FastAPI = FastAPI()

# Simulamos un estado global para el streaming
streaming_state = {
    "current_step": 0,
    "total_steps": 15,
    "messages": [],
    "is_complete": False,
    "started_at": None
}

@app.post("/start-process")
async def start_process():
    """Inicia un proceso que simula trabajo en background"""
    global streaming_state
    
    # Reiniciar estado
    streaming_state = {
        "current_step": 0,
        "total_steps": 15,
        "messages": [],
        "is_complete": False,
        "started_at": datetime.now().isoformat()
    }
    
    # Iniciar proceso en background
    asyncio.create_task(background_process())
    
    return JSONResponse({
        "status": "started",
        "message": "Proceso iniciado, usa /status para ver el progreso",
        "process_id": streaming_state["started_at"]
    })

async def background_process():
    """Simula un proceso largo que actualiza el estado"""
    global streaming_state
    
    for i in range(1, streaming_state["total_steps"] + 1):
        await asyncio.sleep(1)  # Simular trabajo
        
        # Actualizar estado
        streaming_state["current_step"] = i
        streaming_state["messages"].append({
            "step": i,
            "message": f"Completado paso {i} de {streaming_state['total_steps']}",
            "timestamp": datetime.now().isoformat(),
            "progress": (i / streaming_state["total_steps"]) * 100
        })
        
        print(f"📋 Paso {i} completado")
    
    streaming_state["is_complete"] = True
    print("✅ Proceso completado")

@app.get("/status")
async def get_status():
    """Endpoint para obtener el estado actual del proceso"""
    return JSONResponse({
        "current_step": streaming_state["current_step"],
        "total_steps": streaming_state["total_steps"],
        "progress_percentage": (streaming_state["current_step"] / streaming_state["total_steps"]) * 100,
        "is_complete": streaming_state["is_complete"],
        "messages": streaming_state["messages"],
        "started_at": streaming_state["started_at"]
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8444)