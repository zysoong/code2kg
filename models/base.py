import networkx as nx
from pydantic import BaseModel, Field


class BaseGraphModel(BaseModel):
    graph: nx.DiGraph = Field(default_factory=nx.DiGraph)
