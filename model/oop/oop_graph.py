from pydantic import BaseModel, Field
import networkx as nx
from oop_class import OOPClass
from oop_file import OOPFile
from oop_function import OOPFunction


class OOPGraph(BaseModel):
    graph: nx.Graph = Field(default_factory=nx.Graph)
    _type_to_nodes: dict = Field(default_factory=dict)

    def add_file(self, file: OOPFile):
        self.graph.add_node()
