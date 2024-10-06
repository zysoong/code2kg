from abc import ABC, abstractmethod
from typing import Any

import networkx as nx
from pydantic import BaseModel, Field, ConfigDict


class BaseGraphNodeModel(BaseModel, ABC):
    id: Any = Field(default=None)
    attributes: dict[str, Any] = Field(default_factory=dict)
    relations: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if self.node_id() is None:
            raise ValueError(f"id of BaseGraphNodeModel {self.__class__.__name__} not found. Please implement"
                             f" the node_id() function in {self.__class__.__name__} by returning the attribute name"
                             f" as string, which will be recognized as id of the graph node. ")
        self.id = getattr(self, self.node_id())
        node_attr: list = self.node_attr() if self.node_attr() is not None else []
        outgoing_relations: list = self.outgoing_relations() if self.outgoing_relations() is not None else []

        self.attributes = {attr_key: getattr(self, attr_key) for attr_key in node_attr}
        self.relations = {rel_key: getattr(self, rel_key) for rel_key in outgoing_relations}

        for _, rel in self.relations.items():
            for depends_on in _convert_relations_to_list(rel):
                if not isinstance(depends_on, BaseGraphNodeModel):
                    raise ValueError(f"Relation of a BaseGraphNodeModel must be a BaseGraphNodeModel, or a"
                                     f" list of BaseGraphNodeModel. {self.__class__.__name__} however has relation"
                                     f" to a {depends_on.__class__.__name__} which is not a BaseGraphNodeModel. ")

    @abstractmethod
    def node_id(self) -> str:
        pass

    @abstractmethod
    def node_attr(self) -> list[str]:
        pass

    @abstractmethod
    def outgoing_relations(self) -> list[str]:
        pass


class BaseGraphModel(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    nx_graph: nx.DiGraph = Field(default_factory=nx.DiGraph)
    base_nodes: dict[str, BaseGraphNodeModel] = Field(default={})

    def add_node(self, node: BaseGraphNodeModel):
        merged_node: BaseGraphNodeModel = self._merge_add_base_and_nx_node(node)
        for relation_key, relation_element_or_list in merged_node.relations.items():
            for depends_on_node in _convert_relations_to_list(relation_element_or_list):  # type: BaseGraphNodeModel
                if depends_on_node.id not in self.base_nodes:
                    self.base_nodes[depends_on_node.id] = depends_on_node
                    self.nx_graph.add_node(depends_on_node.id, **depends_on_node.attributes)
                else:
                    self._merge_add_base_and_nx_node(depends_on_node)
                self.nx_graph.add_edge(node.id, depends_on_node.id, type=relation_key)

    def get_base_node_from_nx_node(self, nx_node):
        node_id: str = self.nx_graph.nodes[nx_node].get("id")
        base_node: BaseGraphNodeModel = self.base_nodes[node_id]
        return base_node

    def _merge_add_base_and_nx_node(self, node: BaseGraphNodeModel) -> BaseGraphNodeModel:
        if node.id in self.base_nodes:
            merged_node: BaseGraphNodeModel = (
                _merge_base_node(self.base_nodes[node.id], node))
            self.nx_graph.add_node(merged_node.id, **merged_node.attributes)
            self.base_nodes[merged_node.id] = merged_node
            return merged_node
        else:
            self.nx_graph.add_node(node.id, **node.attributes)
            self.base_nodes[node.id] = node


def _merge_base_node(
        node_1: BaseGraphNodeModel,
        node_2: BaseGraphNodeModel
) -> BaseGraphNodeModel:
    if node_1.id is not node_2.id:
        raise ValueError("Graph nodes to be merged must have same id. ")
    merged_attrs = _merge_dicts(node_1.attributes, node_2.attributes)
    merged_relations = _merge_dicts(node_1.relations, node_2.relations)
    return BaseGraphNodeModel(
        id=node_1.id,
        attributes=merged_attrs,
        relations=merged_relations
    )


def _merge_nx_graph_node(
        node_1_id: Any,
        node_1_attr: dict[str, Any],
        node_2_id: Any,
        node_2_attr: dict[str, Any]
) -> (Any, dict[str, Any]):
    if node_1_id is not node_2_id:
        raise ValueError("Graph nodes to be merged must have same id. ")
    merged_node_attrs = _merge_dicts(node_1_attr, node_2_attr)
    return node_1_id, merged_node_attrs


def _merge_dicts(
        dict1: dict[str, Any],
        dict2: dict[str, Any],
) -> dict[str, Any]:
    merged_dict: dict[str, Any] = dict1.copy()
    for attr_key, attr_value in dict2.items():
        if attr_key in merged_dict and attr_value is not merged_dict[attr_key]:
            ValueError(f"Merge conflict on dict: Key {attr_key}. "
                       f"Values are {attr_value}, {merged_dict[attr_key]}")
        elif attr_key in merged_dict and attr_value is merged_dict[attr_key]:
            pass
        elif attr_key not in merged_dict:
            merged_dict[attr_key] = attr_value
    return merged_dict


def _convert_relations_to_list(value):
    if isinstance(value, list):
        return value
    elif isinstance(value, tuple):
        return list(value)
    else:
        return [value]
