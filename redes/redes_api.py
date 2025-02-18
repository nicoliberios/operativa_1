from flask import Blueprint, request, jsonify, render_template, url_for
import networkx as nx
import matplotlib.pyplot as plt
import os
from redes.network_solver import max_flow
from datetime import datetime

redes_bp = Blueprint('redes', __name__)

# 📌 Ruta para manejar las solicitudes de la calculadora de redes
@redes_bp.route('/redesb', methods=['GET', 'POST'])
def redes():
    if request.method == 'POST':
        nodes = request.form.get('nodes')
        edges = request.form.get('edges')
        source = request.form.get('source')
        sink = request.form.get('sink')
        operation = request.form.get('operation')

        # 📌 Crear el grafo
        G = nx.DiGraph() if operation == "max_flow" else nx.Graph()

        # Agregar nodos
        node_list = [n.strip() for n in nodes.split(",")]
        G.add_nodes_from(node_list)

        # Agregar conexiones
        for edge in edges.split(";"):
            try:
                n1, n2, weight = edge.split(",")
                G.add_edge(n1.strip(), n2.strip(), weight=int(weight.strip()))
            except ValueError:
                return "Error en el formato de conexiones.", 400

        # 📌 Generar el resultado según la operación seleccionada
        if operation == "max_flow":
            resultado = max_flow(nodes, edges, source, sink)
        elif operation == "shortest_path":
            try:
                path = nx.shortest_path(G, source=source, target=sink, weight="weight")
                length = nx.shortest_path_length(G, source=source, target=sink, weight="weight")
                resultado = {"path": path, "length": length}
            except nx.NetworkXNoPath:
                resultado = {"error": "No hay camino entre los nodos seleccionados."}
        elif operation == "mst":
            mst = nx.minimum_spanning_tree(G, weight="weight")
            resultado = {"mst_edges": list(mst.edges(data=True))}
        else:
            return "Operación no válida", 400

        # 📌 Generar y guardar el gráfico del grafo
        img_path = os.path.join("app", "static", "graphs", "network.png")
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        plt.figure(figsize=(6, 6))

        pos = nx.spring_layout(G)  # Posiciones de los nodos
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.savefig(img_path)
        plt.close()

        return render_template("resultado_redes.html", resultado=resultado, now=datetime.now())

    return render_template('redes.html')
