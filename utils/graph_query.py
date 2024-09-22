import networkx


def get_relative_nodes(graph: networkx.DiGraph, nx_node):

    rel_nodes: list = []

    if nx_node["node_type"] == "function":
        incoming_within_edges = [(u, v) for u, v, data
                                 in graph.in_edges(nx_node, data=True) if data.get('edge_type') == 'within']
        outgoing_call_edges = [(u, v) for u, v, data
                               in graph.out_edges(nx_node, data=True) if data.get('edge_type') == 'calls']

        for u, _ in incoming_within_edges:
            if graph.nodes[u].get("node_type") == "oop_function":
                rel_nodes.append(graph.nodes[u])
        for _, v in outgoing_call_edges:
            if graph.nodes[v].get("node_type") == "oop_function":
                rel_nodes.append(graph.nodes[v])

    elif nx_node["node_type"] == "class":
        incoming_within_edges = [(u, v) for u, v, data
                                 in graph.in_edges(nx_node, data=True) if data.get('edge_type') == 'within']
        for u, _ in incoming_within_edges:
            if (graph.nodes[u].get("node_type") == "oop_function" or
                    graph.nodes[u].get("node_type") == "oop_class"):
                rel_nodes.append(graph.nodes[u])

    return rel_nodes
