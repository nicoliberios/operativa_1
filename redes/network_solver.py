import networkx as nx

def max_flow(nodes, edges, source, sink):
    G = nx.DiGraph()

    # Agregar nodos
    node_list = nodes.split(",")

    # Agregar conexiones
    for edge in edges.split(";"):
        try:
            n1, n2, capacity = edge.split(",")
            G.add_edge(n1.strip(), n2.strip(), capacity=int(capacity.strip()))
        except ValueError:
            return {"error": f"Error en la conexión: {edge}"}

    # Validar que los nodos existan en el grafo
    if source not in G or sink not in G:
        return {"error": "Nodo de origen o destino no encontrado"}

    # Calcular el flujo máximo
    flow_value, flow_dict = nx.maximum_flow(G, source, sink)

    return {"flow_value": flow_value, "flow_dict": flow_dict}
