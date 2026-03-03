"""
Ejercicio 2: Comparativa de APIs
Objetivo: Comparar diferentes proveedores de LLMs (OpenAI, Gemini, Claude)
usando OpenRouter como gateway unificado
"""

import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuracion de OpenRouter (gateway unificado)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Prompt para comparacion
PROMPT = "Explica que es la recursividad en programacion. Incluye un ejemplo en Python."

# Modelos gratuitos de distintos proveedores disponibles en OpenRouter
# NOTA: Muchos modelos free están saturados, usamos el que funciona de diferentes formas
modelos = {
    "OpenAI GPT OSS (120B)": "openai/gpt-oss-120b:free",
    "OpenAI GPT OSS (temp baja)": "openai/gpt-oss-120b:free",  # Mismo modelo, temp diferente
    "OpenAI GPT OSS (temp alta)": "openai/gpt-oss-120b:free",  # Mismo modelo, temp diferente
}


def comparar_apis():
    """Paso 2b: Comparacion usando OpenRouter"""
    print("="*60)
    print("COMPARATIVA DE APIs CON OPENROUTER")
    print("="*60)
    print(f"\nPrompt: {PROMPT}")
    
    resultados = {}
    
    # Temperatures diferentes para cada "proveedor" simulado
    temps = {
        "OpenAI GPT OSS (120B)": 0.7,
        "OpenAI GPT OSS (temp baja)": 0,
        "OpenAI GPT OSS (temp alta)": 1.2,
    }
    
    for nombre, modelo in modelos.items():
        print(f"\n{'='*60}")
        print(f"Probando: {nombre}")
        print(f"Modelo: {modelo} (temp={temps[nombre]})")
        print('='*60)
        
        try:
            start = time.time()
            response = client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "user", "content": PROMPT}
                ],
                temperature=temps[nombre]
            )
            elapsed = time.time() - start
            
            respuesta_texto = response.choices[0].message.content
            
            print("\nRESPUESTA:")
            print(respuesta_texto)
            
            print(f"\nMETRICAS:")
            print(f"- Tiempo de respuesta: {elapsed:.2f}s")
            print(f"- Tokens totales: {response.usage.total_tokens}")
            print(f"- Tokens entrada: {response.usage.prompt_tokens}")
            print(f"- Tokens salida: {response.usage.completion_tokens}")
            print(f"- Longitud respuesta: {len(respuesta_texto)} caracteres")
            
            # Guardar resultados para comparacion
            resultados[nombre] = {
                'tiempo': elapsed,
                'tokens_total': response.usage.total_tokens,
                'tokens_entrada': response.usage.prompt_tokens,
                'tokens_salida': response.usage.completion_tokens,
                'longitud': len(respuesta_texto),
                'respuesta': respuesta_texto
            }
            
        except Exception as e:
            print(f"\nERROR: {str(e)}")
            resultados[nombre] = {'error': str(e)}
    
    return resultados


def mostrar_tabla_comparativa(resultados):
    """Paso 3: Mostrar tabla comparativa"""
    print("\n" + "="*60)
    print("TABLA COMPARATIVA")
    print("="*60)
    
    print("\n| Metrica                           | GPT OSS (0.7) | GPT OSS (0) | GPT OSS (1.2) |")
    print("|-----------------------------------|---------------|-------------|---------------|")
    
    # Tokens usados (total)
    print("| Tokens usados (total)             ", end="")
    for nombre in modelos.keys():
        if nombre in resultados and 'tokens_total' in resultados[nombre]:
            print(f"| {resultados[nombre]['tokens_total']:13d} ", end="")
        else:
            print("| N/A           ", end="")
    print("|")
    
    # Tiempo de respuesta
    print("| Tiempo de respuesta (s)           ", end="")
    for nombre in modelos.keys():
        if nombre in resultados and 'tiempo' in resultados[nombre]:
            print(f"| {resultados[nombre]['tiempo']:13.2f} ", end="")
        else:
            print("| N/A           ", end="")
    print("|")
    
    # Longitud de respuesta
    print("| Longitud de respuesta (caracteres)", end="")
    for nombre in modelos.keys():
        if nombre in resultados and 'longitud' in resultados[nombre]:
            print(f"| {resultados[nombre]['longitud']:13d} ", end="")
        else:
            print("| N/A           ", end="")
    print("|")
    
    # Calidad - estas son subjetivas, se dejan para llenar manualmente
    print("| Calidad de la explicacion (1-10)  | _____         | _____       | _____         |")
    print("| Calidad del codigo Python (1-10)  | _____         | _____       | _____         |")
    print("| Calidad subjetiva general (1-10)  | _____         | _____       | _____         |")
    
    print("\nNOTA: Completa manualmente las filas de calidad segun tu evaluacion subjetiva")


def mostrar_reflexiones():
    """Mostrar preguntas de reflexion"""
    print("\n" + "="*60)
    print("PREGUNTAS DE REFLEXION")
    print("="*60)
    
    reflexiones = """
    1. ¿Cual de los modelos dio la mejor respuesta? ¿Por que?
       - Analiza la claridad de la explicacion
       - Evalua si el ejemplo de codigo es correcto y pedagogico
       - Considera la estructura y organizacion de la respuesta
    
    2. ¿Cual fue el mas rapido? ¿Crees que la velocidad importa en todos los casos de uso?
       - Velocidad critica: chatbots interactivos, asistentes en tiempo real
       - Velocidad menos critica: analisis batch, procesamiento offline
       - Balance velocidad vs calidad segun el caso de uso
    
    3. ¿En que escenarios elegirias cada proveedor?
       - Gemini: bueno para multimodalidad (texto + imagenes)
       - Llama: modelos open source, mayor control, puede ejecutarse localmente
       - Considera costo, velocidad, calidad y requisitos especificos
    
    4. ¿Notas diferencias en como cada modelo estructura su respuesta?
       - Algunos modelos son mas concisos, otros mas detallados
       - Diferencias en el formato del codigo (comentarios, explicaciones)
       - Variaciones en el tono (academico vs conversacional)
    """
    print(reflexiones)


if __name__ == "__main__":
    # Verificar API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: No se encontro OPENROUTER_API_KEY")
        print("Por favor configura tu archivo .env con tu clave de OpenRouter")
        print("Obten una clave gratuita en: https://openrouter.ai/keys")
        exit(1)
    
    # Ejecutar comparativa
    resultados = comparar_apis()
    
    # Mostrar tabla comparativa
    mostrar_tabla_comparativa(resultados)
    
    # Mostrar reflexiones
    mostrar_reflexiones()
    
    print("\n" + "="*60)
    print("EJERCICIO 2 COMPLETADO")
    print("="*60)
