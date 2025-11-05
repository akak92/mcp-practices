import requests
import json
import time
import sys
from datetime import datetime

def http_polling_client():
    """Cliente que hace polling HTTP para simular streaming"""
    base_url = "http://localhost:8444"
    
    print("🚀 Iniciando proceso via HTTP polling...")
    print("=" * 50)
    
    try:
        # 1. Iniciar el proceso
        start_response = requests.post(f"{base_url}/start-process")
        if start_response.status_code == 200:
            start_data = start_response.json()
            print(f"✅ {start_data['message']}")
            print(f"🆔 Process ID: {start_data['process_id']}")
            print()
        else:
            print(f"❌ Error iniciando proceso: {start_response.status_code}")
            return
        
        # 2. Hacer polling del estado
        last_step = 0
        while True:
            # Hacer request del estado actual
            status_response = requests.get(f"{base_url}/status")
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                
                # Mostrar nuevos mensajes
                if status_data['current_step'] > last_step:
                    for message in status_data['messages'][last_step:]:
                        print(f"📨 [{datetime.now().strftime('%H:%M:%S')}] "
                              f"Paso {message['step']}: {message['message']} "
                              f"({message['progress']:.1f}%)")
                        sys.stdout.flush()
                    
                    last_step = status_data['current_step']
                
                # Verificar si terminó
                if status_data['is_complete']:
                    print()
                    print("🎉 ¡Proceso completado!")
                    print(f"📊 Total pasos: {status_data['total_steps']}")
                    print(f"⏱️  Iniciado en: {status_data['started_at']}")
                    break
                
                # Esperar antes del siguiente poll
                time.sleep(0.5)  # Polling cada 500ms
            
            else:
                print(f"❌ Error obteniendo estado: {status_response.status_code}")
                break
                
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor. ¿Está ejecutándose en puerto 8444?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    http_polling_client()