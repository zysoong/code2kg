from abc import ABC, abstractmethod
from typing import Any

import networkx as nx
from pydantic import BaseModel, Field


def _convert_to_list(value):
    if isinstance(value, list):
        return value
    elif isinstance(value, tuple):
        return list(value)
    else:
        return [value]


class BaseGraphNodeModel(BaseModel, ABC):
    id: Any = Field(default=None)
    attributes: dict[str, Any] = Field(default={})
    relations: dict[str, Any] = Field(default={})

    def __init__(self, **kwargs):

        self.id = self.model_fields[self.node_id()]
        self.attributes = {attr_key: self.model_fields[attr_key] for attr_key in self.node_attr()}
        self.relations = {rel_key: self.model_fields[rel_key] for rel_key in self.outgoing_relations()}

        if self.id is None:
            raise ValueError(f"Graph node id is None. ")

        for _, rel in self.relations.items():
            for depends_on in _convert_to_list(rel):
                if not isinstance(depends_on, BaseGraphNodeModel):
                    raise ValueError(f"Graph node depends on a {depends_on.__class__.__name}. "
                                     f"Expected {BaseGraphNodeModel.__name__}")

        super().__init__(**kwargs)

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
    graph: nx.DiGraph = Field(default_factory=nx.DiGraph)

    def add_node(self, node: BaseGraphNodeModel):

        self.graph.add_node(node.id, **node.attributes)

        for rel_key, rel in node.relations.items():
            for depends_on_node in _convert_to_list(rel):  # type: BaseGraphNodeModel
                if depends_on_node.id not in self.graph:
                    self.graph.add_node(depends_on_node.id, **depends_on_node.attributes)
                self.graph.add_edge(node.id, depends_on_node.id, type=rel_key)
