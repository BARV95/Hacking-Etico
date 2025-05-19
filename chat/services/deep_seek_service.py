import os
from dotenv import load_dotenv
import requests
load_dotenv() 



def consultar_deepseek(prompt: str) -> str: 

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {

        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",

    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free", 
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un experto analista de ciberseguridad y hacking ético con vasta experiencia. "
                    "Tu tarea principal es analizar la información que se te proporciona, que puede ser de dos tipos:\n"
                    "1. Resultados de búsquedas (potencialmente de Google Dorks): Estos pueden incluir URLs, títulos y fragmentos de texto que podrían indicar la exposición de archivos sensibles, listados de directorios, información de versiones de software, configuraciones vulnerables u otra información que pueda ser explotada.\n"
                    "2. Un nombre de dominio específico para un análisis general.\n\n"
                    "**Si analizas resultados de búsquedas (Google Dorks):**\n"
                    "Para cada resultado o patrón de vulnerabilidad que identifiques en la información proporcionada, debes:\n"
                    "   a. Identificar y Describir la Posible Vulnerabilidad: De forma clara y concisa.\n"
                    "   b. Explicar los Riesgos Asociados: Detalla los peligros potenciales.\n"
                    "   c. Proporcionar Recomendaciones Específicas: Ofrece soluciones claras, técnicas y accionables para mitigar o solucionar la vulnerabilidad.\n\n"
                    "**Si analizas un nombre de dominio proporcionado directamente para una evaluación general (ej. 'analiza ejemplo.com'):**\n"
                    "Tu objetivo es proporcionar un **resumen conciso y directo** de los posibles riesgos de seguridad y áreas clave de investigación ética para dicho dominio. Ve directo al análisis del dominio que se te indique. "
                    "Evita preámbulos sobre tus capacidades, limitaciones o el proceso que sigues. No uses una estructura de listado con letras (A, B, C...) en tu respuesta final.\n"
                    "Basándote en tu conocimiento general de ciberseguridad:\n"
                    "1.  Inicia con una frase como 'Análisis general de seguridad para el dominio [nombre del dominio]:'.\n"
                    "2.  Menciona 2-3 **tipos de vulnerabilidades conceptuales clave** que suelen ser relevantes para dominios web como el proporcionado (ej., problemas de configuración del servidor, vulnerabilidades de aplicaciones web, exposición de información). Para cada una, explica brevemente su riesgo principal en una o dos frases concisas.\n"
                    "3.  Sugiere 3-4 **acciones o áreas de investigación prioritarias** que un hacker ético consideraría al evaluar la seguridad de un dominio de este tipo. Describe brevemente (1-2 frases por área) qué se buscaría o evaluaría.\n"
                    "4.  Ofrece 2-3 **recomendaciones generales concisas y accionables** de buenas prácticas para fortalecer la seguridad de un dominio.\n"
                    "Internamente, recuerda NO realizar ninguna conexión o escaneo activo al dominio. Tu análisis se basa en tu base de conocimiento. No es necesario que menciones esta limitación en tu respuesta al usuario.\n\n"
                    "Mantén siempre un tono profesional, ético y educativo. Tu objetivo es ayudar a comprender los riesgos y a mejorar la postura de seguridad. "
                    "Responde siempre en español."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3, 
        "max_tokens": 1500  
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=70)


        if response.status_code == 401: 
            return "Error de autenticación con OpenRouter. Verifica tu API key."
        if response.status_code == 402: 
             return "Problema de pago o cuota excedida en OpenRouter."
        if response.status_code == 429: 
            return "Demasiadas solicitudes a OpenRouter. Has alcanzado el límite de velocidad."
            
        response.raise_for_status() 

        data = response.json()
        

        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return "Tiempo de espera agotado al contactar OpenRouter."
    except requests.exceptions.ConnectionError as conn_err:
        return f"No se pudo establecer conexión con OpenRouter. {str(conn_err)}"
    except requests.exceptions.HTTPError as http_err:

        error_details = http_err.response.text
        try:

            error_json = http_err.response.json()
            if 'error' in error_json and 'message' in error_json['error']:
                error_details = error_json['error']['message']
            elif 'detail' in error_json: 
                 error_details = str(error_json['detail'])
        except ValueError:
            pass 
        return f"Error HTTP de OpenRouter: {http_err.response.status_code} - {error_details}"
    except requests.exceptions.RequestException as req_err:
        return f"Error de solicitud con OpenRouter: {str(req_err)}"
    except KeyError:
        return "Respuesta inesperada de OpenRouter. No se pudo extraer el contenido."
    except Exception as e:
        return f"Error inesperado al procesar la respuesta de OpenRouter: {str(e)}"