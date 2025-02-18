import pulp
import re
from gpt import modulo_ia

class PrograLineal:
    @staticmethod
    def resolver_problema(funcion_objetivo, objetivo, restricciones):
        """
        Resuelve un problema de programación lineal utilizando PuLP con el método de la Gran M.

        :param funcion_objetivo: Cadena de texto que representa la función objetivo (e.g., "3*x + 4*y").
        :param objetivo: Tipo de objetivo ("Maximizar" o "Minimizar").
        :param restricciones: Lista de cadenas de texto que representan las restricciones (e.g., "2*x + y <= 5").
        :return: Diccionario con los resultados del problema resuelto.
        """
        # Extraer variables y coeficientes de la función objetivo
        variables = list(set(re.findall(r'[a-zA-Z]+', funcion_objetivo)))
        coeficientes = [int(coef) for coef in re.findall(r'[-+]?\d+', funcion_objetivo)]

        # Crear el problema de programación lineal
        problema = pulp.LpProblem("Problema_de_Programacion_Lineal",
                                  pulp.LpMaximize if objetivo == "Maximizar" else pulp.LpMinimize)

        # Definir las variables en PuLP
        lp_variables = {var: pulp.LpVariable(var, lowBound=0) for var in variables}
        artificios = []

        # Añadir la función objetivo a PuLP
        funcion_objetivo_expr = sum(coef * lp_variables[var] for coef, var in zip(coeficientes, variables))
        problema += funcion_objetivo_expr, "Función Objetivo"

        # Gran M para las variables de artificio
        M = 1e6

        # Añadir las restricciones a PuLP
        for i, restriccion in enumerate(restricciones):
            # Convertir la restricción en una expresión que PuLP pueda entender
            expr = restriccion
            expr = re.sub(r'([a-zA-Z]+)', lambda m: f'lp_variables["{m.group(1)}"]', expr)

            if '<=' in expr:
                # Restricción de tipo <=
                lhs, rhs = expr.split('<=')
                rhs = float(rhs.strip())
                lhs = lhs.strip()
                problema += (eval(lhs) <= rhs), f"Restricción_{i+1}"

            elif '>=' in expr:
                # Restricción de tipo >=
                lhs, rhs = expr.split('>=')
                rhs = float(rhs.strip())
                lhs = lhs.strip()

                # Añadir variable de artificio y penalizar en función objetivo
                artificial = pulp.LpVariable(f'artificial_{i+1}', lowBound=0)
                artificios.append(artificial)
                problema += (eval(lhs) - artificial >= rhs), f"Restricción_{i+1}"
                problema.setObjective(funcion_objetivo_expr + M * artificial)

            elif '=' in expr:
                # Restricción de tipo =
                lhs, rhs = expr.split('=')
                rhs = float(rhs.strip())
                lhs = lhs.strip()

                # Añadir variable de artificio y penalizar en función objetivo
                artificial = pulp.LpVariable(f'artificial_{i+1}', lowBound=0)
                artificios.append(artificial)
                problema += (eval(lhs) + artificial == rhs), f"Restricción_{i+1}"
                problema.setObjective(funcion_objetivo_expr + M * artificial)

        # Resolver el problema
        problema.solve()

        # Recoger los resultados
        resultado = {
            "Objetivo": objetivo,
            "Función": funcion_objetivo,
            "Variables": {var: var_value.varValue for var, var_value in lp_variables.items()},
            "Coeficientes": coeficientes,
            "Restricciones": restricciones,
            "Valor_Objetivo": pulp.value(problema.objective),
            "Holguras": {f"Restricción_{i+1}": max(0, problema.constraints[f"Restricción_{i+1}"].slack) for i in range(len(restricciones))},
            "Artificios": {f"artificial_{i+1}": artificio.varValue for i, artificio in enumerate(artificios)},
            "Costo_Reducido": {var: var_value.dj for var, var_value in lp_variables.items()},
            "Precios_Duales": {f"Restricción_{i+1}": problema.constraints[f"Restricción_{i+1}"].pi for i in range(len(restricciones))}
        }
        return resultado

if __name__ == "__main__":
    # Datos de prueba
    funcion_objetivo = "3*x + 4*y"
    objetivo = "Maximizar"
    restricciones = [
        "2*x + y <= 5",
        "x + 2*y >= 6",
        "x + y = 3"
    ]

    # Resolver el problema
    resultado = PrograLineal.resolver_problema(funcion_objetivo, objetivo, restricciones)

    # Imprimir resultados
    print("Resultados del Problema de Programación Lineal:")
    print(f"Función Objetivo: {resultado['Función']}")
    print(f"Tipo de Objetivo: {resultado['Objetivo']}")
    print(f"Variables y Valores: {resultado['Variables']}")
    print(f"Coeficientes: {resultado['Coeficientes']}")
    print(f"Restricciones: {resultado['Restricciones']}")
    print(f"Valor de la Función Objetivo: {resultado['Valor_Objetivo']}")
    print(f"Holguras: {resultado['Holguras']}")
    print(f"Artificios: {resultado['Artificios']}")
    print(f"Costo Reducido: {resultado['Costo_Reducido']}")
    print(f"Precios Dual: {resultado['Precios_Duales']}")
