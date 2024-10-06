import pytest
from pydantic import Field, ConfigDict

from base.models import BaseGraphNodeModel, BaseGraphModel


class DummyClass:
    def __init__(self):
        self.dummy_variable = ""


class NodeWithoutId(BaseGraphNodeModel):
    dummy_name: str = Field(...)

    def node_id(self) -> str:
        pass

    def node_attr(self) -> list[str]:
        return []

    def outgoing_relations(self) -> list[str]:
        return []


class NodeWithoutAttrAndRelation(BaseGraphNodeModel):
    dummy_name: str = Field(...)

    def node_id(self) -> str:
        return "dummy_name"

    def node_attr(self) -> list[str]:
        pass

    def outgoing_relations(self) -> list[str]:
        pass


class NodeRelatedToDummyClass(BaseGraphNodeModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    dummy_name: str = Field(...)
    related_to: DummyClass = Field(...)

    def node_id(self) -> str:
        return "dummy_name"

    def node_attr(self) -> list[str]:
        return []

    def outgoing_relations(self) -> list[str]:
        return ["related_to"]


class SimpleNode(BaseGraphNodeModel):
    name: str = Field(...)
    related_to: list["SimpleNode"] = Field(..., default_factory=list)

    def node_id(self) -> str:
        return "name"

    def node_attr(self) -> list[str]:
        return []

    def outgoing_relations(self) -> list[str]:
        return ["related_to"]


def test_base_graph_node_without_id():
    with pytest.raises(ValueError, match="id of BaseGraphNodeModel NodeWithoutId not found."):
        NodeWithoutId(dummy_name="dummy_name")


def test_base_graph_node_without_attr_and_relations():
    node = NodeWithoutAttrAndRelation(dummy_name="dummy_name")
    assert node.attributes == {}
    assert node.relations == {}


def test_bash_graph_node_related_to_dummy_class():
    dummy_obj: DummyClass = DummyClass()
    with pytest.raises(ValueError, match="Relation of a BaseGraphNodeModel must be a BaseGraphNodeModel, "
                                         "or a list of BaseGraphNodeModel. NodeRelatedToDummyClass however "
                                         "has relation to a DummyClass which is not a BaseGraphNodeModel. "):
        NodeRelatedToDummyClass(dummy_name="dummy_name", related_to=dummy_obj)


def test_first_level_adding_to_graph_with_merging_and_branching_nodes():

    graph: BaseGraphModel = BaseGraphModel()

    n1: SimpleNode = SimpleNode(
        name="n1",
        related_to=[
            SimpleNode(name="n2"),
            SimpleNode(name="n3")
        ]
    )
    n2: SimpleNode = SimpleNode(
        name="n2",
        related_to=[
            SimpleNode(name="n5"),
        ]
    )
    n3: SimpleNode = SimpleNode(name="n3")
    n4: SimpleNode = SimpleNode(
        name="n4",
        related_to=[
            SimpleNode(name="n2"),
        ]
    )
    n5: SimpleNode = SimpleNode(name="n5")

    graph.add_node(n1)
    graph.add_node(n2)
    graph.add_node(n3)
    graph.add_node(n4)
    graph.add_node(n5)




