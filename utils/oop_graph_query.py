import networkx

from base.models import BaseGraphModel, BaseGraphNodeModel
from models.oop import OOPFunction, OOPClass


def get_relative_nodes(oop_graph: BaseGraphModel, oop_node: BaseGraphNodeModel) -> list[BaseGraphNodeModel]:
    rel_nodes: list = []
    nx_node = oop_graph.nx_graph[oop_node.id]

    if isinstance(oop_node, OOPFunction):
        incoming_within_edges = [(u, v) for u, v, data
                                 in oop_graph.nx_graph.in_edges(nx_node, data=True) if data.get('type') == 'within']
        outgoing_call_edges = [(u, v) for u, v, data
                               in oop_graph.out_edges(nx_node, data=True) if data.get('type') == 'calls']

        for u, _ in incoming_within_edges:
            u_base_node: BaseGraphNodeModel = oop_graph.get_base_node_from_nx_node(u)
            if isinstance(u_base_node, OOPFunction):
                rel_nodes.append(u_base_node)

        for _, v in outgoing_call_edges:
            v_base_node: BaseGraphNodeModel = oop_graph.get_base_node_from_nx_node(v)
            if isinstance(v_base_node, OOPFunction):
                rel_nodes.append(v_base_node)

    elif isinstance(oop_node, OOPClass):
        incoming_within_edges = [(u, v) for u, v, data
                                 in oop_graph.in_edges(nx_node, data=True) if data.get('type') == 'within']

        for u, _ in incoming_within_edges:
            u_base_node: BaseGraphNodeModel = oop_graph.get_base_node_from_nx_node(u)
            if isinstance(u_base_node, OOPFunction) or isinstance(u_base_node, OOPClass):
                rel_nodes.append(u_base_node)

    return rel_nodes
