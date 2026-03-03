"""
Ejercicio 1: Primera Llamada a la API
Objetivo: Configurar el entorno y realizar llamadas basicas a la API de LLMs
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear el cliente con OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
MODEL = "openai/gpt-oss-120b:free"

# NOTA: Los modelos gratuitos pueden cambiar. Si este no funciona, consulta:
# https://openrouter.ai/models?q=free
# y actualiza MODEL con un modelo disponible

# Si prefieres usar OpenAI directo (de pago), descomenta:
# client = OpenAI()
# MODEL = "gpt-4o-mini"


def primera_llamada():
    """Paso 2: Primera llamada a la API"""
    print("="*60)
    print("PASO 2: PRIMERA LLAMADA A LA API")
    print("="*60)
    
    # Realizar la llamada a la API
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "¿Qué es el machine learning? Responde en 3 oraciones."}
        ],
        temperature=0.7
    )
    
    # Extraer e imprimir los datos solicitados
    # 1. El texto de la respuesta
    print("\n1. Respuesta:")
    print(response.choices[0].message.content)
    
    # 2. El modelo utilizado
    print(f"\n2. Modelo: {response.model}")
    
    # 3. Tokens del prompt
    print(f"\n3. Prompt tokens: {response.usage.prompt_tokens}")
    
    # 4. Tokens de la respuesta
    print(f"4. Completion tokens: {response.usage.completion_tokens}")
    
    # 5. Total de tokens
    print(f"5. Total tokens: {response.usage.total_tokens}")
    
    return response


def experimentar_temperature():
    """Paso 3: Experimentar con temperature"""
    print("\n" + "="*60)
    print("PASO 3: EXPERIMENTANDO CON TEMPERATURE")
    print("="*60)
    
    temperatures = [0, 0.7, 1.5]
    prompt = "¿Qué es el machine learning? Responde en 3 oraciones."
    
    for temp in temperatures:
        print(f"\n{'='*60}")
        print(f"TEMPERATURE = {temp}")
        print("="*60)
        
        # Ejecutar 3 veces para ver variabilidad
        for i in range(1, 4):
            print(f"\n--- Ejecucion {i} ---")
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temp
            )
            print(response.choices[0].message.content)
            print(f"Tokens: {response.usage.total_tokens}")


def analizar_observaciones():
    """Imprime las observaciones sobre temperature"""
    print("\n" + "="*60)
    print("OBSERVACIONES SOBRE TEMPERATURE")
    print("="*60)
    
    observaciones = """
    TEMPERATURE = 0:
    - Las respuestas son identicas o muy similares entre ejecuciones
    - Estilo consistente y predecible
    - Ideal para: Asistente de atencion al cliente, extraccion de datos,
      respuestas facticas donde se requiere consistencia
    
    TEMPERATURE = 0.7:
    - Las respuestas varian ligeramente entre ejecuciones
    - Balance entre creatividad y coherencia
    - Ideal para: Conversaciones generales, tutores, chatbots interactivos
    
    TEMPERATURE = 1.5:
    - Las respuestas son muy diferentes entre ejecuciones
    - Mayor creatividad y variabilidad, a veces menos coherente
    - Ideal para: Generador de poesia, brainstorming creativo,
      generacion de ideas novedosas
    
    PREGUNTAS DE REFLEXION:
    
    1. ¿Por que es importante monitorear el consumo de tokens?
    - Porque los tokens determinan el costo de cada llamada a la API
    - Permite optimizar presupuestos y detectar uso ineficiente
    - Ayuda a dimensionar la capacidad de procesamiento necesaria
    
    2. ¿Que sucede si envias un prompt muy largo?
    - Aumenta significativamente el consumo de tokens de entrada
    - Incrementa el costo proporcionalmente
    - Puede acercarse al limite de contexto del modelo
    - El tiempo de respuesta puede aumentar
    
    3. ¿Cual es la diferencia entre temperature=0 y temperature=1.5?
    - temperature=0: Respuestas deterministicas y conservadoras
    - temperature=1.5: Respuestas creativas y mas aleatorias
    - A mayor temperature, mayor variabilidad en las respuestas
    """
    print(observaciones)


if __name__ == "__main__":
    # Verificar que hay API key configurada
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: No se encontro OPENROUTER_API_KEY")
        print("Por favor configura tu archivo .env con tu API key de OpenRouter")
        print("Obten una gratis en: https://openrouter.ai/keys")
        exit(1)
    
    # Ejecutar los pasos del ejercicio
    primera_llamada()
    
    # Preguntar si desea ejecutar experimentos de temperature (son muchas llamadas)
    print("\n" + "="*60)
    respuesta = input("\n¿Deseas ejecutar los experimentos con temperature? (s/n): ")
    if respuesta.lower() in ['s', 'si', 'y', 'yes']:
        experimentar_temperature()
    
    # Mostrar observaciones
    analizar_observaciones()
    
    print("\n" + "="*60)
    print("EJERCICIO 1 COMPLETADO")
    print("="*60)
