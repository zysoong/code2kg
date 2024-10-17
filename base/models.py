from abc import ABC, abstractmethod
from typing import Any

import networkx as nx
from pydantic import BaseModel, Field, ConfigDict, model_validator


class BaseGraphNodeModel(BaseModel, ABC):
    class Config:
        validate_assignment = True

    @property
    def id(self) -> Any:
        return getattr(self, self.node_id())

    @property
    def attributes(self) -> dict[str, Any]:
        node_attr: list[str] = self.node_attr() if self.node_attr() is not None else []
        return {attr_key: getattr(self, attr_key) for attr_key in node_attr}

    @property
    def relations(self) -> dict[str, list[Any]]:
        outgoing_relations: list[str] = self.outgoing_relations() if self.outgoing_relations() is not None else []
        relations_property = {rel_key: getattr(self, rel_key) for rel_key in outgoing_relations}
        return relations_property

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.node_id() is None:
            raise ValueError(f"id of BaseGraphNodeModel {self.__class__.__name__} not found. Please implement"
                             f" the node_id() function in {self.__class__.__name__} by returning the attribute name"
                             f" as string, which will be recognized as id of the graph node. ")
        for _, rel in self.relations.items():
            if not isinstance(rel, list):
                raise ValueError(f"Relation of a BaseGraphNodeModel must be a "
                                 f"list of BaseGraphNodeModel. Given relation is not a list. ")
            else:
                for depends_on in rel:
                    if not isinstance(depends_on, BaseGraphNodeModel):
                        raise ValueError(f"Relation of a BaseGraphNodeModel must be a "
                                         f"list of BaseGraphNodeModel. {self.__class__.__name__} however has relation"
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
    shallow_nodes: dict[str, BaseGraphNodeModel] = Field(default={})

    def add_node(self, node: BaseGraphNodeModel):
        merged_node: BaseGraphNodeModel = self._add_and_merge_base_and_nx_node(node)
        for relation_key, relation_element_or_list in merged_node.relations.items():
            for depends_on_node in _convert_relations_to_list(relation_element_or_list):  # type: BaseGraphNodeModel
                if depends_on_node.id not in self.shallow_nodes:
                    self.nx_graph.add_node(depends_on_node.id, **depends_on_node.attributes)
                else:
                    self._add_and_merge_base_and_nx_node(depends_on_node)
                self.nx_graph.add_edge(node.id, depends_on_node.id, type=relation_key)

    def _add_and_merge_base_and_nx_node(self, node: BaseGraphNodeModel) -> BaseGraphNodeModel:
        if node.id in self.shallow_nodes:
            merged_node: BaseGraphNodeModel = _merge_base_node(self.shallow_nodes[node.id], node)
            self.nx_graph.add_node(merged_node.id, **merged_node.attributes)
            self.shallow_nodes[merged_node.id] = merged_node
            return merged_node
        else:
            self.nx_graph.add_node(node.id, **node.attributes)
            self.shallow_nodes[node.id] = node
            return node


def _merge_base_node(
        node1: BaseGraphNodeModel,
        node2: BaseGraphNodeModel
) -> BaseGraphNodeModel:
    if node1.id is not node2.id:
        raise ValueError("Graph nodes to be merged must have same id. ")
    node1_merged_attr: BaseGraphNodeModel = _merge_base_node_dict(node1, node2, "attributes")
    node_merged: BaseGraphNodeModel = _merge_base_node_dict(node1_merged_attr, node2, "relations")
    return node_merged


def _merge_base_node_dict(base_node: BaseGraphNodeModel, merging_node: BaseGraphNodeModel, node_property: str) \
        -> BaseGraphNodeModel:
    base_node_dict: dict[str, Any] = getattr(base_node, node_property)
    merging_node_dict: dict[str, Any] = getattr(merging_node, node_property)

    if base_node_dict.keys() != merging_node_dict.keys():
        raise ValueError(f"BaseGraphNodeModel must have same {node_property} set on merging. "
                         f"The {node_property} sets of given nodes are {base_node_dict.keys()} "
                         f"and {merging_node_dict.keys()}. "
                         f"Please check if the fields of BaseGraphNodeModel {base_node.__class__.__name__} and "
                         f"{merging_node.__class__.__name__} are all initialized with 'default' or 'default_factory'. ")
    else:
        attrs_merged: dict[str, Any] = base_node_dict.copy()

        for property_key in attrs_merged:
            if base_node_dict[property_key] == merging_node_dict[property_key]:
                attrs_merged[property_key] = base_node_dict[property_key]

            elif (_is_node_attribute_initial(base_node, property_key) and
                  not _is_node_attribute_initial(merging_node, property_key)):
                attrs_merged[property_key] = merging_node_dict[property_key]

            elif (not _is_node_attribute_initial(base_node, property_key) and
                  _is_node_attribute_initial(merging_node, property_key)):
                attrs_merged[property_key] = base_node_dict[property_key]

            else:
                raise ValueError(f"Merge conflict on node : {node_property} key {property_key}. "
                                 f"Values are {base_node_dict[property_key]}, {merging_node_dict[property_key]}")

        return base_node.model_copy(update=attrs_merged, deep=True)


def _is_node_attribute_initial(
        node: BaseGraphNodeModel,
        attr_key: str
) -> bool:
    if node.model_fields[attr_key].default_factory is not None:
        if getattr(node, attr_key) == node.model_fields[attr_key].default_factory() or \
                getattr(node, attr_key) == node.model_fields[attr_key].default:
            return True
        else:
            return False
    else:
        if getattr(node, attr_key) == node.model_fields[attr_key].default:
            return True
        else:
            return False


def _convert_relations_to_list(value):
    if isinstance(value, list):
        return value
    elif isinstance(value, tuple):
        return list(value)
    else:
        return [value]
