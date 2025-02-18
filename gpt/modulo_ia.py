import openai
from dotenv import load_dotenv
import os

class AnalisisIA:
    @staticmethod
    def interpretar_sensibilidad(resultados):

        openai.api_key = os.getenv('OPENAI_API_KEY')

        prompt = (
            "Se te presenta un problema de programación lineal que ya esta resuelto. Analiza los resultados obtenidos, "
            "incluyendo el valor de la función objetivo y los valores de las variables. "
            "Tambien, has un análisis de sensibilidad considerando los cambios en los coeficientes de la función objetivo "
            "y tambien en las restricciones. Genera una interpretación detallada de cómo estos cambios pueden afectar la solución óptima.\n\n"

            "Resultados del Problema de Programación Lineal:\n"
            f"Función Objetivo: {resultados['Función']}\n"
            f"Objetivo: {resultados['Objetivo']}\n"
            f"Variables y Valores: {resultados['Variables']}\n"
            f"Coeficientes: {resultados['Coeficientes']}\n"
            f"Restricciones: {resultados['Restricciones']}\n"
            f"Valor de la Función Objetivo: {resultados['Valor_Objetivo']}\n"
            f"Holguras: {resultados['Holguras']}\n"

            "Crea un análisis de sensibilidad considerando los siguientes aspectos:\n"
            f"1. Cambios en los coeficientes de la función objetivo: Si el coeficiente del término 'x' aumenta en 3 unidades, "
            f"según el valor actual de 'x' que es  {resultados['Variables']}, ¿cómo afectaría esto a la solución óptima y al valor de la función objetivo?\n"
            "¿cómo afectaría esto a la solución óptima y al valor de la función objetivo?\n"
            f"2. Modificaciones en las restricciones: Si el límite superior de la segunda restricción que sale de que es  {resultados['Restricciones']}, cambia en 2 unidades"
            "¿cómo se vería alterada la solución óptima?\n"
            "3. Recomendaciones Prácticas: Menciona sugerencias para mejorar la solución.\n\n"
            
            "Proporciona una interpretación detallada de los resultados obtenidos y de los cambios hipotéticos mencionados."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Eres un asistente experto en programación lineal y análisis de sensibilidad."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450
        )

        informacion = response.choices[0]['message']['content'].strip()
        return informacion

