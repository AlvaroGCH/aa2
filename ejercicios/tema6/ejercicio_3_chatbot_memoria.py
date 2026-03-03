"""
Ejercicio 3: Chatbot con Memoria
Objetivo: Implementar un chatbot que mantiene el contexto de la conversacion
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuracion con OpenRouter
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

# System prompt que define la personalidad del chatbot
SYSTEM_PROMPT = """Eres un tutor de Python amigable y paciente. Tu objetivo es ayudar a 
estudiantes a aprender programacion en Python de forma clara y pedagogica.

Caracteristicas:
- Presentate brevemente en tu primera respuesta
- Se paciente y alentador
- Da ejemplos de codigo claros y bien comentados
- Explica conceptos de forma simple, paso a paso
- Relaciona nuevos conceptos con conocimientos previos del estudiante
- Usa analogias cuando sea util para la comprension"""

# Limite maximo de mensajes en el historial (sin contar el system prompt)
MAX_MESSAGES = 10


def create_initial_messages():
    """Crea la lista inicial de mensajes con el system prompt."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]


def trim_history(messages):
    """
    Mantiene el historial dentro del limite MAX_MESSAGES.
    
    Estrategia:
    - El primer mensaje siempre es el system prompt (se mantiene)
    - Se mantienen los ultimos MAX_MESSAGES mensajes de user/assistant
    - Se eliminan los mensajes mas antiguos cuando se supera el limite
    
    Args:
        messages: Lista de mensajes
    
    Returns:
        Lista de mensajes recortada
    """
    # El system prompt siempre esta en la posicion 0
    system_msg = messages[0]
    conversation_msgs = messages[1:]
    
    # Si no superamos el limite, retornar todo
    if len(conversation_msgs) <= MAX_MESSAGES:
        return messages
    
    # Mantener solo los ultimos MAX_MESSAGES mensajes
    trimmed_conversation = conversation_msgs[-MAX_MESSAGES:]
    
    return [system_msg] + trimmed_conversation


def get_response(messages):
    """Envia los mensajes a la API y retorna la respuesta."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7
    )
    return response


def chat():
    """Bucle principal del chatbot."""
    print("="*60)
    print("CHATBOT CON MEMORIA - TUTOR DE PYTHON")
    print("="*60)
    print(f"Limite de historial: {MAX_MESSAGES} mensajes")
    print("Comandos especiales:")
    print("  - 'salir' o 'exit': terminar")
    print("  - 'historial': ver mensajes en memoria")
    print("  - 'tokens': ver uso de tokens")
    print("="*60 + "\n")
    
    # Inicializar el historial con el system prompt
    messages = create_initial_messages()
    
    while True:
        # Solicitar entrada del usuario
        user_input = input("Tu: ").strip()
        
        # Comandos especiales
        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("\nHasta luego!")
            break
        
        if user_input.lower() == 'historial':
            print(f"\nMensajes en memoria: {len(messages) - 1} (sin contar system prompt)")
            for i, msg in enumerate(messages[1:], 1):  # Omitir system prompt
                role = msg['role']
                content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
                print(f"  {i}. [{role}] {content}")
            print()
            continue
        
        if user_input.lower() == 'tokens':
            # Hacer una llamada dummy para ver tokens
            dummy_response = get_response(messages + [{"role": "user", "content": "hola"}])
            print(f"\nTokens aproximados en el historial actual:")
            print(f"  - Prompt tokens: {dummy_response.usage.prompt_tokens}")
            print(f"  - Total tokens: {dummy_response.usage.total_tokens}")
            print()
            continue
        
        if not user_input:
            continue
        
        # Agregar mensaje del usuario
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Recortar historial si es necesario
        messages = trim_history(messages)
        
        # Obtener respuesta del assistant
        try:
            response = get_response(messages)
            assistant_message = response.choices[0].message.content
            
            # Agregar respuesta del assistant al historial
            messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Mostrar respuesta
            print(f"\nAsistente: {assistant_message}\n")
            
            # Mostrar informacion de tokens y mensajes en memoria
            msgs_count = len(messages) - 1  # Sin contar system prompt
            print(f"[Mensajes en memoria: {msgs_count}/{MAX_MESSAGES} | Tokens usados: {response.usage.total_tokens}]")
            print()
            
        except Exception as e:
            print(f"\nError: {str(e)}\n")


def prueba_automatica():
    """Paso 2: Prueba de memoria con secuencia predefinida"""
    print("="*60)
    print("PRUEBA AUTOMATICA DE MEMORIA")
    print("="*60 + "\n")
    
    messages = create_initial_messages()
    
    # Secuencia de preguntas para probar la memoria
    preguntas = [
        "¿Que son las variables en Python?",
        "Dame un ejemplo de lo anterior",
        "Ahora muestrame como usar listas",
        "¿Cual es la diferencia entre lo primero que me explicaste y esto?"
    ]
    
    for i, pregunta in enumerate(preguntas, 1):
        print(f"Pregunta {i}: {pregunta}")
        
        messages.append({"role": "user", "content": pregunta})
        messages = trim_history(messages)
        
        try:
            response = get_response(messages)
            respuesta = response.choices[0].message.content
            
            messages.append({"role": "assistant", "content": respuesta})
            
            print(f"Respuesta: {respuesta}\n")
            print("-"*60 + "\n")
            
        except Exception as e:
            print(f"Error: {str(e)}\n")
    
    print("VERIFICACION:")
    print("- En la pregunta 2, el bot debe entender que 'lo anterior' se refiere a variables")
    print("- En la pregunta 4, el bot debe comparar variables (pregunta 1) con listas (pregunta 3)")
    print("- Esto demuestra que el chatbot mantiene el contexto correctamente")


def prueba_limite_historial():
    """Paso 3: Probar el limite de historial"""
    print("\n" + "="*60)
    print("PRUEBA DE LIMITE DE HISTORIAL")
    print("="*60)
    print(f"\nNOTA: Para esta prueba, MAX_MESSAGES esta configurado en {MAX_MESSAGES}")
    print("Modificalo a 4 en el codigo para ver como olvida mensajes antiguos\n")
    
    messages = create_initial_messages()
    
    # Simular conversacion larga
    temas = [
        "Explicame que son las variables",
        "Explicame que son las funciones",
        "Explicame que son las clases",
        "Explicame que son los decoradores",
        "Explicame que son los generadores",
        "Explicame que son los context managers",
        "¿Recuerdas el primer tema que te pregunte?"  # Esta pregunta prueba la memoria
    ]
    
    for i, tema in enumerate(temas, 1):
        print(f"\nPregunta {i}: {tema}")
        
        messages.append({"role": "user", "content": tema})
        messages = trim_history(messages)
        
        try:
            response = get_response(messages)
            respuesta = response.choices[0].message.content
            
            messages.append({"role": "assistant", "content": respuesta})
            
            print(f"Respuesta: {respuesta[:200]}...")  # Solo primeros 200 caracteres
            print(f"\n[Mensajes en memoria: {len(messages) - 1}]")
            
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n" + "="*60)
    print("OBSERVACIONES:")
    print("""
    - Si MAX_MESSAGES es suficientemente grande (ej: 10), el bot recordara las variables
    - Si MAX_MESSAGES es pequeno (ej: 4), el bot habra olvidado la primera pregunta
    - Cuando el historial se recorta, se pierden los mensajes mas antiguos
    - Esto afecta la coherencia en conversaciones muy largas
    - En el ultimo mensaje, observa si el bot recuerda que el primer tema fueron las variables
    """)


if __name__ == "__main__":
    # Verificar API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: No se encontro OPENROUTER_API_KEY")
        print("Por favor configura tu archivo .env con tu API key de OpenRouter")
        print("Obten una gratis en: https://openrouter.ai/keys")
        exit(1)
    
    print("="*60)
    print("EJERCICIO 3: CHATBOT CON MEMORIA")
    print("="*60)
    print("\nSelecciona una opcion:")
    print("1. Chat interactivo (Paso 1)")
    print("2. Prueba automatica de memoria (Paso 2)")
    print("3. Prueba de limite de historial (Paso 3)")
    print("4. Ejecutar todas las pruebas")
    
    opcion = input("\nOpcion (1-4): ").strip()
    
    if opcion == "1":
        chat()
    elif opcion == "2":
        prueba_automatica()
    elif opcion == "3":
        prueba_limite_historial()
    elif opcion == "4":
        prueba_automatica()
        prueba_limite_historial()
        print("\n¿Deseas probar el chat interactivo? (s/n): ", end="")
        if input().lower() in ['s', 'si', 'y', 'yes']:
            chat()
    else:
        print("Opcion invalida")
    
    print("\n" + "="*60)
    print("EJERCICIO 3 COMPLETADO (sin bonus)")
    print("="*60)
