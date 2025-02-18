# Importación de bibliotecas necesarias
from ortools.linear_solver import pywraplp  # Importamos la librería OR-Tools para resolver problemas de programación lineal
import numpy as np  # Usamos numpy para operaciones con matrices y vectores

# Definimos la función para el Método de Aproximación de Vogel
def m_aproximacion_vogel(oferta, demanda, costos):
    oferta = oferta.copy()  # Hacemos una copia de la oferta para no modificar el original
    demanda = demanda.copy()  # Hacemos una copia de la demanda para no modificar el original
    costos = np.array(costos, dtype=float)  # Convertimos los costos a un array de tipo float para poder operar con ellos

    if sum(oferta) != sum(demanda):
        # Si la oferta total no es igual a la demanda total, ajustamos el problema
        print("Equilibramos la oferta y la demanda agregando ceros ficticios segun corresponda")
        
        if sum(oferta) > sum(demanda):
            # Si la oferta es mayor, añadimos una columna ficticia a la demanda
            demanda.append(sum(oferta) - sum(demanda))
            costos = np.hstack((costos, np.zeros((costos.shape[0], 1))))  # Añadimos una columna con costos 0
        else:
            # Si la demanda es mayor, añadimos una fila ficticia a la oferta
            oferta.append(sum(demanda) - sum(oferta))
            costos = np.vstack((costos, np.zeros((1, costos.shape[1]))))  # Añadimos una fila con costos 0

    matriz_asignacion = np.zeros(costos.shape)  # Inicializamos una matriz de asignación con ceros

    # Aquí comienza el proceso iterativo para la asignación de la oferta a la demanda usando el Método de Vogel
    while np.any(oferta) and np.any(demanda):
        # Calculamos las diferencias de costos mínimos por fila y columna
        dif_costos_fila = np.partition(costos, 1, axis=1)[:, 1] - np.partition(costos, 0, axis=1)[:, 0]
        dif_costos_columna = np.partition(costos, 1, axis=0)[1, :] - np.partition(costos, 0, axis=0)[0, :]

        # Encontramos la diferencia máxima entre filas y columnas
        max_row_diff = np.nanmax(dif_costos_fila)  # Máxima diferencia en las filas
        max_col_diff = np.nanmax(dif_costos_columna)  # Máxima diferencia en las columnas
        
        # Si la máxima diferencia de fila es mayor o igual a la de columna, asignamos en la fila
        if max_row_diff >= max_col_diff:
            fila = np.nanargmax(dif_costos_fila)  # Indice de la fila con la mayor diferencia
            columna = np.nanargmin(costos[fila, :])  # Columna con el costo mínimo en esa fila
        else:
            # Si la diferencia de columna es mayor, asignamos en la columna
            columna = np.nanargmax(dif_costos_columna)  # Indice de la columna con la mayor diferencia
            fila = np.nanargmin(costos[:, columna])  # Fila con el costo mínimo en esa columna

        # La cantidad que se puede asignar es la mínima entre la oferta y la demanda
        cantidad_asignada = min(oferta[fila], demanda[columna])  
        matriz_asignacion[fila, columna] = cantidad_asignada  # Asignamos esa cantidad en la matriz de asignación
        oferta[fila] -= cantidad_asignada  # Restamos esa cantidad de la oferta
        demanda[columna] -= cantidad_asignada  # Restamos esa cantidad de la demanda

        # Marcamos el costo de ese espacio como infinito para que no se vuelva a considerar
        costos[fila, columna] = np.inf
    
    return matriz_asignacion

# Función para resolver el problema de transporte usando programación lineal con OR-Tools
def m_resuelve_problema_transporte(oferta, demanda, costos):
    # Creamos el solver de programación lineal con el método GLOP (basado en el algoritmo de punto interior)
    resuelve_problem_transporte = pywraplp.Solver.CreateSolver('GLOP')

    # Creamos las variables de decisión, que representarán la cantidad de bienes transportados de cada origen a cada destino
    x = {}
    for i in range(len(oferta)):  # Iteramos sobre la oferta
        for j in range(len(demanda)):  # Iteramos sobre la demanda
            x[i, j] = resuelve_problem_transporte.NumVar(0, resuelve_problem_transporte.infinity(), f'x[{i},{j}]')  # Variable de decisión con límites entre 0 e infinito

    # Añadimos las restricciones de oferta: cada origen no puede enviar más de su oferta
    for i in range(len(oferta)):  # Iteramos sobre cada origen
        resuelve_problem_transporte.Add(sum(x[i, j] for j in range(len(demanda))) <= oferta[i])  # Restricción de oferta

    # Añadimos las restricciones de demanda
    for j in range(len(demanda)):  # Iteramos sobre cada destino
        resuelve_problem_transporte.Add(sum(x[i, j] for i in range(len(oferta))) >= demanda[j])  # Restricción de demanda

    # Definimos la función objetivo, que es minimizar los costos de transporte
    objective = resuelve_problem_transporte.Objective()
    for i in range(len(oferta)):  # Iteramos sobre la oferta
        for j in range(len(demanda)):  # Iteramos sobre la demanda
            objective.SetCoefficient(x[i, j], costos[i][j])  # Añadimos los coeficientes de los costos a la función objetivo
    objective.SetMinimization()  # Establecemos que queremos minimizar el costo

    # Establecemos un límite de tiempo para la solución (20 segundos)
    resuelve_problem_transporte.SetTimeLimit(20000)  # Limite de tiempo de 20 segundos

    # Resolvemos el problema
    status = resuelve_problem_transporte.Solve()

    # Si se encuentra una solución óptima, devolvemos la asignación y el valor de la función objetivo
    if status == pywraplp.Solver.OPTIMAL:
        matriz_asignacion = np.zeros((len(oferta), len(demanda)))  # Inicializamos la matriz de asignación
        for i in range(len(oferta)):  # Iteramos sobre la oferta
            for j in range(len(demanda)):  # Iteramos sobre la demanda
                matriz_asignacion[i, j] = x[i, j].solution_value()  # Asignamos el valor de la variable de decisión a la matriz de asignación
        return matriz_asignacion.tolist(), resuelve_problem_transporte.Objective().Value()  # Devolvemos la asignación y el valor de la función objetivo
    else:
        # Si no se encuentra una solución óptima, lanzamos una excepción
        raise Exception('No tiene una solucion optima.')
