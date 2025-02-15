from ortools.linear_solver import pywraplp
import numpy as np

def vogel_approximation_method(supply, demand, cost):
    supply = supply.copy()
    demand = demand.copy()
    cost = np.array(cost, dtype=float)
    
    # Manejar el caso cuando la oferta no es igual a la demanda
    if sum(supply) != sum(demand):
        print("La oferta total no es igual a la demanda total. Se ajustará el problema con costos de transporte de 0.")
        if sum(supply) > sum(demand):
            # Añadir una columna de demanda ficticia
            demand.append(sum(supply) - sum(demand))
            cost = np.hstack((cost, np.zeros((cost.shape[0], 1))))
        else:
            # Añadir una fila de oferta ficticia
            supply.append(sum(demand) - sum(supply))
            cost = np.vstack((cost, np.zeros((1, cost.shape[1]))))

    allocation = np.zeros(cost.shape)
    
    while np.any(supply) and np.any(demand):
        row_diff = np.partition(cost, 1, axis=1)[:, 1] - np.partition(cost, 0, axis=1)[:, 0]
        col_diff = np.partition(cost, 1, axis=0)[1, :] - np.partition(cost, 0, axis=0)[0, :]

        max_row_diff = np.nanmax(row_diff)
        max_col_diff = np.nanmax(col_diff)
        
        if max_row_diff >= max_col_diff:
            row = np.nanargmax(row_diff)
            col = np.nanargmin(cost[row, :])
        else:
            col = np.nanargmax(col_diff)
            row = np.nanargmin(cost[:, col])
        
        allocation_amount = min(supply[row], demand[col])
        allocation[row, col] = allocation_amount
        supply[row] -= allocation_amount
        demand[col] -= allocation_amount

        cost[row, col] = np.inf
    
    return allocation

def solve_transportation_problem(supply, demand, cost):
    solver = pywraplp.Solver.CreateSolver('GLOP')

    x = {}
    for i in range(len(supply)):
        for j in range(len(demand)):
            x[i, j] = solver.NumVar(0, solver.infinity(), f'x[{i},{j}]')

    for i in range(len(supply)):
        solver.Add(sum(x[i, j] for j in range(len(demand))) <= supply[i])

    for j in range(len(demand)):
        solver.Add(sum(x[i, j] for i in range(len(supply))) >= demand[j])

    objective = solver.Objective()
    for i in range(len(supply)):
        for j in range(len(demand)):
            objective.SetCoefficient(x[i, j], cost[i][j])
    objective.SetMinimization()

    solver.SetTimeLimit(20000)  # Set a time limit of 20 seconds
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        allocation = np.zeros((len(supply), len(demand)))
        for i in range(len(supply)):
            for j in range(len(demand)):
                allocation[i, j] = x[i, j].solution_value()
        return allocation.tolist(), solver.Objective().Value()
    else:
        raise Exception('El problema no tiene una solución óptima.')
