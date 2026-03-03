"""
Ejercicio 4: Extraccion Estructurada
Objetivo: Extraer datos estructurados en formato JSON desde texto libre
"""

import os
import json
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

# Paso 1: System prompt para extraccion
SYSTEM_PROMPT = """Eres un sistema de extraccion de informacion. Tu tarea es extraer datos
estructurados de textos no estructurados y devolver UNICAMENTE un JSON valido.

Reglas:
- Responde SOLO con el JSON, sin texto adicional, sin bloques de codigo markdown.
- Si un campo no se encuentra en el texto, usa el valor "No especificado".
- Los valores numericos deben ser numeros, no strings.
- Las fechas deben estar en formato YYYY-MM-DD cuando sea posible.
"""

# Paso 2: Textos de entrada y esquemas

# Texto 1 - Oferta de empleo
texto_empleo = """
Unete a nuestro equipo! Buscamos Desarrollador Senior Python para nuestra
oficina en Madrid. Ofrecemos salario de 45.000-55.000 euros brutos anuales,
teletrabajo 3 dias por semana y seguro medico privado. Requisitos: 5 anos
de experiencia, conocimientos en Django y PostgreSQL. Incorporacion inmediata.
Enviar CV a empleo@techcorp.es antes del 15 de marzo de 2025.
"""

esquema_empleo = """
{
    "puesto": "string",
    "empresa": "string (si se menciona)",
    "ubicacion": "string",
    "salario_min": "number",
    "salario_max": "number",
    "modalidad": "string",
    "requisitos": ["string"],
    "beneficios": ["string"],
    "contacto": "string",
    "fecha_limite": "string (YYYY-MM-DD)"
}
"""

# Texto 2 - Resena de producto
texto_resena = """
Compre el portatil UltraBook X15 hace 2 semanas. La pantalla de 15 pulgadas
es espectacular y la bateria dura unas 10 horas reales. Sin embargo, el
teclado es un poco incomodo para escribir largo rato y se calienta bastante
con tareas pesadas. Por el precio de 1.299 euros creo que esta bien, pero no es
perfecto. Le doy un 7 de 10. Lo compre en Amazon el 20 de enero de 2025.
"""

esquema_resena = """
{
    "producto": "string",
    "puntos_positivos": ["string"],
    "puntos_negativos": ["string"],
    "precio": "number",
    "moneda": "string",
    "puntuacion": "number (sobre 10)",
    "donde_compro": "string",
    "fecha_compra": "string (YYYY-MM-DD)",
    "recomendacion_general": "string (positiva/neutra/negativa)"
}
"""

# Texto 3 - Noticia
texto_noticia = """
La empresa espanola de inteligencia artificial, NovaTech, anuncio hoy una
ronda de financiacion Serie B por valor de 30 millones de euros, liderada
por el fondo Sequoia Capital con participacion de Telefonica Ventures.
La compania, fundada en 2021 por Maria Garcia y Carlos Lopez, planea usar
los fondos para expandirse a Latinoamerica y contratar a 50 ingenieros
antes de fin de ano. NovaTech ha desarrollado un modelo de lenguaje
especializado en el sector legal.
"""

esquema_noticia = """
{
    "empresa": "string",
    "tipo_evento": "string",
    "monto": "number",
    "moneda": "string",
    "inversores": ["string"],
    "fundadores": ["string"],
    "ano_fundacion": "number",
    "sector": "string",
    "planes": ["string"]
}
"""


def extract_json(text, schema_description, max_retries=3):
    """
    Extrae informacion estructurada de un texto y la devuelve como JSON.
    
    Args:
        text: Texto del que extraer informacion
        schema_description: Descripcion del esquema JSON esperado
        max_retries: Numero maximo de reintentos si el JSON es invalido
    
    Returns:
        dict: Datos extraidos como diccionario Python
    """
    user_prompt = f"""Extrae la informacion del siguiente texto y devuelve un JSON
con este esquema:

{schema_description}

Texto:
\"\"\"
{text}
\"\"\"
"""
    
    for intento in range(1, max_retries + 1):
        try:
            # Llamar a la API
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0  # Temperatura 0 para respuestas consistentes
            )
            
            respuesta_texto = response.choices[0].message.content.strip()
            
            # Limpiar posibles marcas de markdown
            if respuesta_texto.startswith("```json"):
                respuesta_texto = respuesta_texto[7:]
            if respuesta_texto.startswith("```"):
                respuesta_texto = respuesta_texto[3:]
            if respuesta_texto.endswith("```"):
                respuesta_texto = respuesta_texto[:-3]
            respuesta_texto = respuesta_texto.strip()
            
            # Intentar parsear el JSON
            datos = json.loads(respuesta_texto)
            
            print(f"  [Exito en intento {intento}]")
            return datos
            
        except json.JSONDecodeError as e:
            print(f"  [Intento {intento}/{max_retries}] Error al parsear JSON: {str(e)}")
            if intento == max_retries:
                print(f"  [ERROR] No se pudo obtener JSON valido despues de {max_retries} intentos")
                print(f"  Respuesta recibida: {respuesta_texto[:200]}...")
                return None
        
        except Exception as e:
            print(f"  [ERROR] Error en la llamada a la API: {str(e)}")
            return None
    
    return None


def ejecutar_extracciones():
    """Paso 3: Ejecutar las extracciones para los tres textos"""
    print("="*60)
    print("EXTRACCION ESTRUCTURADA DE DATOS")
    print("="*60)
    
    textos = {
        "Oferta de empleo": (texto_empleo, esquema_empleo),
        "Resena de producto": (texto_resena, esquema_resena),
        "Noticia": (texto_noticia, esquema_noticia)
    }
    
    resultados = {}
    
    for nombre, (texto, esquema) in textos.items():
        print(f"\n{'='*60}")
        print(f"Extrayendo: {nombre}")
        print('='*60)
        print(f"\nTexto original:")
        print(texto.strip())
        print(f"\nEsquema esperado:")
        print(esquema.strip())
        print(f"\nExtrayendo...")
        
        datos = extract_json(texto, esquema)
        
        if datos:
            print(f"\nJSON extraido:")
            print(json.dumps(datos, indent=2, ensure_ascii=False))
            resultados[nombre] = datos
        else:
            print(f"\n[ERROR] No se pudo extraer datos para {nombre}")
            resultados[nombre] = None
    
    return resultados


def analizar_resultados(resultados):
    """Paso 4: Analisis de los resultados"""
    print("\n" + "="*60)
    print("ANALISIS DE RESULTADOS")
    print("="*60)
    
    print("\n1. ¿En cuantos intentos logro generar JSON valido para cada texto?")
    print("   - Observar los mensajes '[Exito en intento X]' de arriba")
    print("   - Con temperature=0, deberia ser exitoso en el primer intento")
    
    print("\n2. ¿Hubo campos con valor 'No especificado'? ¿Era correcto?")
    for nombre, datos in resultados.items():
        if datos:
            campos_no_especificados = [k for k, v in datos.items() if v == "No especificado"]
            if campos_no_especificados:
                print(f"   - {nombre}: {', '.join(campos_no_especificados)}")
            else:
                print(f"   - {nombre}: Todos los campos fueron especificados")
    
    print("\n3. ¿Los valores numericos fueron numeros o strings?")
    for nombre, datos in resultados.items():
        if datos:
            campos_numericos = {k: type(v).__name__ for k, v in datos.items() 
                               if isinstance(v, (int, float)) or (isinstance(v, str) and v.isdigit())}
            if campos_numericos:
                print(f"   - {nombre}:")
                for campo, tipo in campos_numericos.items():
                    print(f"     * {campo}: {tipo}")
    
    print("\n4. ¿Que pasaria si el texto de entrada estuviera en otro idioma?")
    print("""   - Los LLMs modernos son multilingues
   - Podrian extraer correctamente de textos en ingles, frances, etc.
   - El esquema JSON puede especificarse en cualquier idioma
   - Importante: ser consistente con el idioma del system prompt y esquema
    """)
    
    print("\nPREGUNTAS ADICIONALES DE REFLEXION:")
    print("""
    - ¿Como manejarias casos donde falta informacion critica?
    - ¿Que estrategias usarias para mejorar la precision de la extraccion?
    - ¿Seria util proporcionar ejemplos (few-shot learning) en el prompt?
    - ¿Como validarias que los datos extraidos son correctos?
    """)


if __name__ == "__main__":
    # Verificar API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: No se encontro OPENROUTER_API_KEY")
        print("Por favor configura tu archivo .env con tu API key de OpenRouter")
        print("Obten una gratis en: https://openrouter.ai/keys")
        exit(1)
    
    # Ejecutar extracciones
    resultados = ejecutar_extracciones()
    
    # Analizar resultados
    analizar_resultados(resultados)
    
    print("\n" + "="*60)
    print("EJERCICIO 4 COMPLETADO")
    print("="*60)
