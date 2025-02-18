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

def shortest_path(nodes, edges, source, target):
    """
    Calcula la ruta más corta entre dos nodos usando Dijkstra.

    :param nodes: Lista de nodos como string separados por ","
    :param edges: Lista de conexiones en formato "nodo1,nodo2,peso"
    :param source: Nodo de origen
    :param target: Nodo de destino
    :return: Diccionario con la ruta más corta y su longitud
    """
    try:
        G = nx.Graph()
        node_list = [n.strip() for n in nodes.split(",")]
        G.add_nodes_from(node_list)

        for edge in edges.split(";"):
            try:
                n1, n2, weight = edge.split(",")
                G.add_edge(n1.strip(), n2.strip(), weight=int(weight.strip()))
            except ValueError:
                return {"error": f"Error en la conexión: {edge} - Formato incorrecto"}

        if source not in G.nodes or target not in G.nodes:
            return {"error": "Nodo de origen o destino no encontrado en el grafo"}

        path = nx.dijkstra_path(G, source, target, weight="weight")
        length = nx.dijkstra_path_length(G, source, target, weight="weight")

        return {"path": path, "length": length}

    except nx.NetworkXNoPath:
        return {"error": "No hay camino entre los nodos"}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}

def minimum_spanning_tree(nodes, edges):
    """
    Calcula el Árbol de Expansión Mínima (MST) con el algoritmo de Kruskal.

    :param nodes: Lista de nodos como string separados por ","
    :param edges: Lista de conexiones en formato "nodo1,nodo2,peso"
    :return: Diccionario con las aristas del MST
    """
    try:
        G = nx.Graph()
        node_list = [n.strip() for n in nodes.split(",")]
        G.add_nodes_from(node_list)

        for edge in edges.split(";"):
            try:
                n1, n2, weight = edge.split(",")
                G.add_edge(n1.strip(), n2.strip(), weight=int(weight.strip()))
            except ValueError:
                return {"error": f"Error en la conexión: {edge} - Formato incorrecto"}

        mst = nx.minimum_spanning_tree(G, weight="weight")
        mst_edges = [(u, v, d["weight"]) for u, v, d in mst.edges(data=True)]

        return {"mst_edges": mst_edges}

    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}

# Prueba las funciones localmente
if __name__ == "__main__":
    nodes = "A,B,C,D,E"
    edges = "A,B,10; B,C,5; C,D,15; A,D,10; B,E,7; D,E,8"

    print("🔹 Prueba de Flujo Máximo:")
    print(max_flow(nodes, edges, "A", "E"))

    print("\n🔹 Prueba de Ruta Mínima:")
    print(shortest_path(nodes, edges, "A", "E"))

    print("\n🔹 Prueba de Árbol de Expansión Mínima:")
    print(minimum_spanning_tree(nodes, edges))
