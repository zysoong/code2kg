from pydantic import BaseModel, Field
import networkx as nx

import utils.object_mapping
from models.oop import OOPModule, OOPClass, OOPFunction


class OOPGraph(BaseModel):
    graph: nx.Graph = Field(default_factory=nx.Graph)
    _type_to_nodes: dict = Field(default_factory=dict)

    def add_module(self, oop_module: OOPModule):
        self.graph.add_node(oop_module.qualified_name)

    def add_class(self, oop_class: OOPClass):
        self.graph.add_node(oop_class.qualified_name, code=oop_class.code)

        class_mapping = {
            "type": "type",
            "code": "code"
        }

        if oop_class.within.qualified_name not in self.graph:
            within_attr = utils.object_mapping.map_object_attributes(oop_class.within, class_mapping)
            self.graph.add_node(oop_class.within.qualified_name, **within_attr)
        self.graph.add_edge(oop_class, oop_class.within, type="within")

        for super_class in oop_class.super_classes:
            if super_class.qualified_name not in self.graph:
                super_class_attr = utils.object_mapping.map_object_attributes(super_class, class_mapping)
                self.graph.add_node(super_class.qualified_name, **super_class_attr)
            self.graph.add_edge(oop_class, super_class, type="extends")

    def add_function(self, oop_function: OOPFunction):
        self.graph.add_node(oop_function.qualified_name, code=oop_function.code)

        function_mapping = {
            "type": "type",
            "code": "code"
        }

        if oop_function.within.qualified_name not in self.graph:
            within_attr = utils.object_mapping.map_object_attributes(oop_function.within, function_mapping)
            self.graph.add_node(oop_function.within.qualified_name, **within_attr)
        self.graph.add_edge(oop_function, oop_function.within, type="within")

        for func in oop_function.flat_function_calls:
            if func.qualified_name not in self.graph:
                super_class_attr = utils.object_mapping.map_object_attributes(func, function_mapping)
                self.graph.add_node(func.qualified_name, **super_class_attr)
            self.graph.add_edge(oop_function, func, type="calls")
