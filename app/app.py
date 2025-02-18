from flask import Flask, jsonify, render_template, request
import numpy as np
from gpt.GptAnaliser import GptAnaliser
from transporte.TransporteSolver import solve_transportation_problem, vogel_approximation_method
from lineal import LinearProgrammingSolver
from redes.redes_api import redes_bp  # ✅ Importar API de redes

app = Flask(__name__)

# ✅ Registrar el Blueprint de redes en la aplicación principal
app.register_blueprint(redes_bp)  # ✅ Registra el Blueprint de redes

@app.route('/redesb')
def redes():
    return render_template('redes.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/objective')
def objetivo():
    return render_template('objetivo.html')

@app.route('/linear', methods=['GET', 'POST'])
def linear():
    resultado = None
    if request.method == 'POST':
   
        funcion_objetivo = request.form.get('funcion_objetivo')
        objetivo = request.form.get('objetivo')
        restricciones_raw = request.form.get('restriccion')

    
        restricciones = [r.strip() for r in restricciones_raw.split('\n') if r.strip()]

    
        print(f"Función Objetivo: {funcion_objetivo}")
        print(f"Objetivo: {objetivo}")
        print(f"Restricciones: {restricciones}")

        if not funcion_objetivo or not objetivo or not restricciones:
            return "Faltan datos en el formulario.", 400

   
        resultado = LinearProgrammingSolver.resolver_problema(funcion_objetivo, objetivo, restricciones)
        analisi = GptAnaliser.interpretar_sensibilidad(resultado)

        if resultado:
            return render_template('resultado.html', resultado=resultado, analisi=analisi)


  
    return render_template('linear-programming.html')


@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    if request.method == 'POST':
        try:
            data = request.json
            num_sources = int(data['numSources'])
            num_destinations = int(data['numDestinations'])
            supply = [int(data[f'supply{i}']) for i in range(num_sources)]
            demand = [int(data[f'demand{j}']) for j in range(num_destinations)]
            cost = [[int(data[f'cost{i}{j}']) for j in range(num_destinations)] for i in range(num_sources)]
            cost_matrix = np.array(cost, dtype=float)


            if sum(supply) != sum(demand):
                if sum(supply) > sum(demand):
                    demand.append(sum(supply) - sum(demand))
                    cost_matrix = np.hstack((cost_matrix, np.zeros((cost_matrix.shape[0], 1))))
                else:
                    supply.append(sum(demand) - sum(supply))
                    cost_matrix = np.vstack((cost_matrix, np.zeros((1, cost_matrix.shape[1]))))

            vogel_allocation = vogel_approximation_method(supply, demand, cost_matrix.tolist())
            vogel_cost = np.sum(vogel_allocation * cost_matrix)
            simplex_allocation, simplex_cost = solve_transportation_problem(supply, demand, cost_matrix.tolist())

            return jsonify({
                'initial_matrix': cost_matrix.tolist(),
                'vogel': {'allocation': vogel_allocation.tolist(), 'cost': vogel_cost},
                'simplex': {'allocation': simplex_allocation, 'cost': simplex_cost}
            })
        except Exception as e:
            return jsonify({'error': str(e)})
    return render_template('transportation.html')


if __name__ == '__main__':
    app.run(debug=True)
