from abc import ABC, abstractmethod
from typing import Any

import networkx as nx
import pydantic
from pydantic import BaseModel, Field, ConfigDict


def _convert_to_list(value):
    if isinstance(value, list):
        return value
    elif isinstance(value, tuple):
        return list(value)
    else:
        return [value]


def _convert_relations_to_list(value):
    if isinstance(value, list):
        return value
    elif isinstance(value, tuple):
        return list(value)
    else:
        return [value]


class BaseGraphNodeModel(BaseModel, ABC):
    id: Any = Field(default=None)
    attributes: dict[str, Any] = Field(default_factory=dict)
    relations: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.id = getattr(self, self.node_id())
        self.attributes = {attr_key: getattr(self, attr_key) for attr_key in self.node_attr()}
        self.relations = {rel_key: getattr(self, rel_key) for rel_key in self.outgoing_relations()}

        if self.id is None:
            raise ValueError(f"Graph node id is None. ")

        for _, rel in self.relations.items():
            for depends_on in _convert_relations_to_list(rel):
                if not isinstance(depends_on, BaseGraphNodeModel):
                    raise ValueError(f"Graph node depends on a {depends_on.__class__.__name}. "
                                     f"Expected {BaseGraphNodeModel.__name__}")

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
        self.nx_graph.add_node(node.id, **node.attributes)
        self.base_nodes[node.id] = node
        for rel_key, rel in node.relations.items():
            for depends_on_node in _convert_relations_to_list(rel):  # type: BaseGraphNodeModel
                if depends_on_node.id not in self.nx_graph:
                    self.nx_graph.add_node(depends_on_node.id, **depends_on_node.attributes)
                self.nx_graph.add_edge(node.id, depends_on_node.id, type=rel_key)

    def get_base_node_from_nx_node(self, nx_node):
        node_id: str = self.nx_graph.nodes[nx_node].get("id")
        base_node: BaseGraphNodeModel = self.base_nodes[node_id]
        return base_node
