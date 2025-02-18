import networkx as nx 

def max_flow(nodes, edges, source, sink):
    """
    Calcula el flujo máximo en un grafo dirigido.

    :param nodes: Lista de nodos como string separados por ","
    :param edges: Lista de conexiones en formato "nodo1,nodo2,capacidad"
    :param source: Nodo de origen
    :param sink: Nodo de destino
    :return: Diccionario con el flujo máximo y el detalle de cada conexión
    """
    try:
        # Crear grafo dirigido
        G = nx.DiGraph()

        # Agregar nodos explícitamente
        node_list = [n.strip() for n in nodes.split(",")]
        G.add_nodes_from(node_list)

        # Agregar conexiones con capacidad
        for edge in edges.split(";"):
            try:
                n1, n2, capacity = edge.split(",")
                G.add_edge(n1.strip(), n2.strip(), capacity=int(capacity.strip()))
            except ValueError:
                return {"error": f"Error en la conexión: {edge} - Formato incorrecto"}

        # Validar que los nodos existan en el grafo
        if source not in G.nodes or sink not in G.nodes:
            return {"error": "Nodo de origen o destino no encontrado en el grafo"}

        # Calcular el flujo máximo
        flow_value, flow_dict = nx.maximum_flow(G, source, sink)

        return {"flow_value": flow_value, "flow_dict": flow_dict}

    except ValueError as e:
        return {"error": f"Error en la entrada de datos: {str(e)}"}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}

# Para probar el código directamente:
if __name__ == "__main__":
    # Datos de prueba
    nodes = "A,B,C,D"
    edges = "A,B,10; B,C,5; C,D,15; A,D,10"
    source = "A"
    sink = "D"

    resultado = max_flow(nodes, edges, source, sink)
    print("🔹 Resultado de prueba:")
    print(resultado)
