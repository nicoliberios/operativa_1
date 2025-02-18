from flask import Blueprint, request, render_template, jsonify
from redes.network_solver import max_flow

redes_bp = Blueprint('redes', __name__)

@redes_bp.route('/redesb', methods=['GET', 'POST'])
def redes():
    if request.method == 'POST':
        nodes = request.form.get('nodes')
        edges = request.form.get('edges')
        source = request.form.get('source')
        sink = request.form.get('sink')

        if not nodes or not edges or not source or not sink:
            return "Faltan datos en el formulario.", 400

        resultado = max_flow(nodes, edges, source, sink)

        return render_template('resultado_redes.html', resultado=resultado)

    return render_template('redes.html')
