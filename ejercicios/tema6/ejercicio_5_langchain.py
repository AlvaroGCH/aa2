"""
Ejercicio 5: Introduccion a LangChain
Objetivo: Usar LangChain para simplificar la construccion de aplicaciones con LLMs
"""

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Configuracion del modelo con OpenRouter
model = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    temperature=0,
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
)

# NOTA: Los modelos gratuitos pueden cambiar. Si este no funciona, consulta:
# https://openrouter.ai/models?q=free
# y actualiza el parametro model con un modelo disponible

# Si prefieres usar OpenAI directo (de pago), descomenta:
# model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Paso 2: Template del prompt para extraccion estructurada
prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres un sistema de extraccion de informacion. Tu tarea es extraer datos
estructurados de textos no estructurados y devolver UNICAMENTE un JSON valido.

Reglas:
- Responde SOLO con el JSON, sin texto adicional, sin bloques de codigo markdown.
- Si un campo no se encuentra en el texto, usa el valor "No especificado".
- Los valores numericos deben ser numeros, no strings.
- Las fechas deben estar en formato YYYY-MM-DD cuando sea posible."""),
    ("user", """Extrae la informacion del siguiente texto y devuelve un JSON
con este esquema: {schema}

Texto:
\"\"\"
{text}
\"\"\"
""")
])

# Parser de salida
output_parser = StrOutputParser()

# Paso 2: Crear la chain con el operador pipe
chain = prompt | model | output_parser


def ejemplo_simple():
    """Paso 2: Ejemplo simple usando la chain"""
    print("="*60)
    print("EJEMPLO SIMPLE CON LANGCHAIN")
    print("="*60)
    
    texto_empleo = """
    Unete a nuestro equipo! Buscamos Desarrollador Senior Python para nuestra
    oficina en Madrid. Ofrecemos salario de 45.000-55.000 euros brutos anuales,
    teletrabajo 3 dias por semana y seguro medico privado. Requisitos: 5 anos
    de experiencia, conocimientos en Django y PostgreSQL. Incorporacion inmediata.
    Enviar CV a empleo@techcorp.es antes del 15 de marzo de 2025.
    """
    
    esquema = "puesto, empresa, ubicacion, salario_min, salario_max, modalidad, requisitos (lista), beneficios (lista), contacto, fecha_limite"
    
    print("\nTexto a procesar:")
    print(texto_empleo.strip())
    
    print("\nEsquema solicitado:")
    print(esquema)
    
    print("\nInvocando la chain...\n")
    
    # Invocar la chain
    result = chain.invoke({
        "text": texto_empleo,
        "schema": esquema
    })
    
    print("Resultado:")
    print(result)
    
    # Intentar parsear como JSON
    try:
        # Limpiar markdown si existe
        result_clean = result.strip()
        if result_clean.startswith("```json"):
            result_clean = result_clean[7:]
        if result_clean.startswith("```"):
            result_clean = result_clean[3:]
        if result_clean.endswith("```"):
            result_clean = result_clean[:-3]
        result_clean = result_clean.strip()
        
        datos = json.loads(result_clean)
        print("\nJSON parseado exitosamente:")
        print(json.dumps(datos, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"\nAdvertencia: No se pudo parsear como JSON: {e}")


def procesar_multiples_textos():
    """Paso 3: Procesar los tres textos del Ejercicio 4"""
    print("\n" + "="*60)
    print("PROCESANDO MULTIPLES TEXTOS CON LANGCHAIN")
    print("="*60)
    
    textos = {
        "Oferta de empleo": {
            "text": """
            Unete a nuestro equipo! Buscamos Desarrollador Senior Python para nuestra
            oficina en Madrid. Ofrecemos salario de 45.000-55.000 euros brutos anuales,
            teletrabajo 3 dias por semana y seguro medico privado. Requisitos: 5 anos
            de experiencia, conocimientos en Django y PostgreSQL. Incorporacion inmediata.
            Enviar CV a empleo@techcorp.es antes del 15 de marzo de 2025.
            """,
            "schema": "puesto, empresa, ubicacion, salario_min, salario_max, modalidad, requisitos (lista), beneficios (lista), contacto, fecha_limite"
        },
        "Resena de producto": {
            "text": """
            Compre el portatil UltraBook X15 hace 2 semanas. La pantalla de 15 pulgadas
            es espectacular y la bateria dura unas 10 horas reales. Sin embargo, el
            teclado es un poco incomodo para escribir largo rato y se calienta bastante
            con tareas pesadas. Por el precio de 1.299 euros creo que esta bien, pero no es
            perfecto. Le doy un 7 de 10. Lo compre en Amazon el 20 de enero de 2025.
            """,
            "schema": "producto, puntos_positivos (lista), puntos_negativos (lista), precio, moneda, puntuacion, donde_compro, fecha_compra, recomendacion_general"
        },
        "Noticia": {
            "text": """
            La empresa espanola de inteligencia artificial, NovaTech, anuncio hoy una
            ronda de financiacion Serie B por valor de 30 millones de euros, liderada
            por el fondo Sequoia Capital con participacion de Telefonica Ventures.
            La compania, fundada en 2021 por Maria Garcia y Carlos Lopez, planea usar
            los fondos para expandirse a Latinoamerica y contratar a 50 ingenieros
            antes de fin de ano. NovaTech ha desarrollado un modelo de lenguaje
            especializado en el sector legal.
            """,
            "schema": "empresa, tipo_evento, monto, moneda, inversores (lista), fundadores (lista), ano_fundacion, sector, planes (lista)"
        }
    }
    
    resultados = {}
    
    for nombre, inputs in textos.items():
        print(f"\n{'='*60}")
        print(f"Procesando: {nombre}")
        print('='*60)
        
        try:
            # Invocar la chain
            result = chain.invoke(inputs)
            
            print(f"\nResultado:")
            print(result)
            
            # Intentar parsear como JSON
            result_clean = result.strip()
            if result_clean.startswith("```json"):
                result_clean = result_clean[7:]
            if result_clean.startswith("```"):
                result_clean = result_clean[3:]
            if result_clean.endswith("```"):
                result_clean = result_clean[:-3]
            result_clean = result_clean.strip()
            
            datos = json.loads(result_clean)
            print(f"\nJSON parseado:")
            print(json.dumps(datos, indent=2, ensure_ascii=False))
            
            resultados[nombre] = {
                "exito": True,
                "datos": datos
            }
            
        except json.JSONDecodeError as e:
            print(f"\nError al parsear JSON: {e}")
            resultados[nombre] = {
                "exito": False,
                "error": str(e)
            }
        except Exception as e:
            print(f"\nError: {e}")
            resultados[nombre] = {
                "exito": False,
                "error": str(e)
            }
    
    return resultados


def comparacion_codigo():
    """Mostrar comparacion entre codigo nativo y LangChain"""
    print("\n" + "="*60)
    print("COMPARACION: CODIGO NATIVO VS LANGCHAIN")
    print("="*60)
    
    comparacion = """
    CODIGO NATIVO (OpenAI directo):
    --------------------------------
    from openai import OpenAI
    
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    result = response.choices[0].message.content
    
    
    CODIGO CON LANGCHAIN:
    ---------------------
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])
    chain = prompt | model | StrOutputParser()
    result = chain.invoke({"variable1": value1, "variable2": value2})
    
    
    VENTAJAS DE LANGCHAIN:
    ----------------------
    1. Sintaxis mas declarativa y legible (operador pipe |)
    2. Reutilizacion de componentes (prompts, models, parsers)
    3. Facilita el encadenamiento de operaciones complejas
    4. Abstraccion de diferencias entre proveedores
    5. Ecosistema rico de integraciones (bases de datos, herramientas, etc.)
    
    CUANDO USAR CADA ENFOQUE:
    -------------------------
    - Codigo nativo: Casos simples, maxima control, aprendizaje inicial
    - LangChain: Aplicaciones complejas, multiples pasos, produccion
    
    COMPARACION DE COMPLEJIDAD:
    ---------------------------
    - Llamada simple: Similar en ambos casos
    - Multiples pasos: LangChain mucho mas simple
    - Mantenimiento: LangChain mas facil de modificar y escalar
    """
    print(comparacion)


def reflexiones_finales():
    """Preguntas de reflexion finales"""
    print("\n" + "="*60)
    print("REFLEXIONES FINALES")
    print("="*60)
    
    reflexiones = """
    1. ¿Cuando preferirías usar LangChain vs. acceso directo a la API?
       - LangChain: Aplicaciones complejas con multiples pasos
       - API directa: Casos simples, necesidad de control fino
    
    2. ¿Que componentes de LangChain te parecen mas utiles?
       - ChatPromptTemplate: Templates reutilizables con variables
       - Chains: Composicion de operaciones con el operador pipe
       - Output parsers: Parseo automatico de respuestas
    
    3. ¿Como cambia la legibilidad del codigo?
       - LangChain: Mas declarativo, enfoque en "que" no en "como"
       - Codigo nativo: Mas imperativo, mas explicito
    
    4. ¿Que otras aplicaciones podrias construir con estos conceptos?
       - Sistemas de preguntas y respuestas sobre documentos
       - Agentes que usan herramientas externas
       - Pipelines de procesamiento de texto complejos
       - Chatbots con memoria a largo plazo
       - Sistemas de recomendacion personalizados
    """
    print(reflexiones)


if __name__ == "__main__":
    # Verificar API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: No se encontro OPENROUTER_API_KEY")
        print("Por favor configura tu archivo .env con tu API key de OpenRouter")
        print("Obten una gratis en: https://openrouter.ai/keys")
        exit(1)
    
    # Ejecutar las partes del ejercicio
    ejemplo_simple()
    
    print("\n" + "="*60)
    respuesta = input("\n¿Deseas procesar los tres textos adicionales? (s/n): ")
    if respuesta.lower() in ['s', 'si', 'y', 'yes']:
        procesar_multiples_textos()
    
    comparacion_codigo()
    reflexiones_finales()
    
    print("\n" + "="*60)
    print("EJERCICIO 5 COMPLETADO")
    print("="*60)
    print("\nHas completado todos los ejercicios de la sesion!")
    print("Para ejecutar cualquier ejercicio, usa: python ejercicio_X_nombre.py")
