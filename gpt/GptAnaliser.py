import openai
from dotenv import load_dotenv
import os

class GptAnaliser:
    @staticmethod
    def interpretar_sensibilidad(resultados):
        """
        Obeten, analiza e interpreta los resultados de sensibilidad.

        :param resultados: Diccionario con los resultados del problema resuelto.
        :return: Interpretación detallada del análisis de sensibilidad en formato legible.
        """
        # Configurar la clave de API de OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Construir el prompt para GPT
        prompt = (
            "Se presenta un problema de programación lineal resuelto. Analiza los resultados obtenidos, "
            "incluyendo el valor de la función objetivo, los valores de las variables, las holguras y las variables de artificio. "
            "Además, realiza un análisis de sensibilidad considerando los cambios potenciales en los coeficientes de la función objetivo "
            "y las restricciones. Proporciona una interpretación detallada de cómo estos cambios pueden afectar la solución óptima.\n\n"

            "Resultados del Problema de Programación Lineal:\n"
            f"Función Objetivo: {resultados['Función']}\n"
            f"Tipo de Objetivo: {resultados['Objetivo']}\n"
            f"Variables y Valores: {resultados['Variables']}\n"
            f"Coeficientes: {resultados['Coeficientes']}\n"
            f"Restricciones: {resultados['Restricciones']}\n"
            f"Valor de la Función Objetivo: {resultados['Valor_Objetivo']}\n"
            f"Holguras: {resultados['Holguras']}\n"
            f"Artificios: {resultados['Artificios']}\n\n"

            "Proporciona un análisis de sensibilidad considerando los siguientes aspectos:\n"
            "1. Cambios en los coeficientes de la función objetivo: Si el coeficiente del término 'x' aumenta de 3 a 5, "
            "¿cómo afectaría esto a la solución óptima y al valor de la función objetivo?\n"
            "2. Modificaciones en las restricciones: Por ejemplo, si el límite superior de la primera restricción cambia de 5 a 6, "
            "¿cómo se vería alterada la solución óptima?\n"
            "3. Impacto de las variables de holgura y de artificio: Explica cómo estas variables influyen en la interpretación de la solución.\n\n"
            "4. Recomendaciones Prácticas: Menciona sugerencias para mejorar la solución.\n\n"
            
            "Proporciona una interpretación detallada de los resultados obtenidos y de los cambios hipotéticos mencionados."
        )

        # Realizar la solicitud a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Eres un asistente experto en programación lineal y análisis de sensibilidad."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450
        )

        # Obtener la respuesta
        informacion = response.choices[0]['message']['content'].strip()
        return informacion

