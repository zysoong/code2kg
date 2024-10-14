import pytest
from pydantic import Field, ConfigDict

import base
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


class NodeRelatedToListOfDummyClass(BaseGraphNodeModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    dummy_name: str = Field(...)
    related_to: list[DummyClass] = Field(...)

    def node_id(self) -> str:
        return "dummy_name"

    def node_attr(self) -> list[str]:
        return []

    def outgoing_relations(self) -> list[str]:
        return ["related_to"]


class SimpleNode(BaseGraphNodeModel):
    name: str = Field(...)
    simple_attr_with_default: str | None = Field(default=None)
    related_to: list["SimpleNode"] = Field(..., default_factory=list)

    def node_id(self) -> str:
        return "name"

    def node_attr(self) -> list[str]:
        return ["simple_attr_with_default"]

    def outgoing_relations(self) -> list[str]:
        return ["related_to"]


def test_NodeWithoutId():
    with pytest.raises(ValueError, match="id of BaseGraphNodeModel NodeWithoutId not found."):
        NodeWithoutId(dummy_name="dummy_name")


def test_NodeWithoutAttrAndRelation():
    node = NodeWithoutAttrAndRelation(dummy_name="dummy_name")
    assert node.attributes == {}
    assert node.relations == {}


def test_NodeRelatedToListOfDummyClass_relate_to_dummy_class_obj():
    dummy_obj: DummyClass = DummyClass()
    with pytest.raises(ValueError, match="Input should be a valid list"):
        NodeRelatedToListOfDummyClass(dummy_name="dummy_name", related_to=dummy_obj)


def test_NodeRelatedToListOfDummyClass_relate_to_list_of_dummy_class_obj():
    with pytest.raises(ValueError, match="Relation of a BaseGraphNodeModel must be a list of BaseGraphNodeModel. "
                                         "NodeRelatedToListOfDummyClass however has relation to "
                                         "a DummyClass which is not a BaseGraphNodeModel. "):
        NodeRelatedToListOfDummyClass(dummy_name="dummy_name", related_to=[DummyClass()])


#TODO Add test cases to change graph node properties

def test_merge_node_attributes_no_conflict():
    n1: SimpleNode = SimpleNode(
        name="n1",
        simple_attr_with_default="attr_n1",
    )
    n1_simplified: SimpleNode = SimpleNode(
        name="n1"
    )
    n_merged = base.models._merge_base_node(n1, n1_simplified)
    assert n_merged.attributes["simple_attr_with_default"] is "attr_n1"


def test_merge_node_attributes_with_conflict():
    n1_1: SimpleNode = SimpleNode(
        name="n1",
        simple_attr_with_default="attr_n1",
    )
    n1_2: SimpleNode = SimpleNode(
        name="n1",
        simple_attr_with_default="attr_n2"
    )
    with pytest.raises(ValueError, match="Merge conflict on node : attributes key simple_attr_with_default. "
                                         "Values are attr_n1, attr_n2"):
        base.models._merge_base_node(n1_1, n1_2)


def test_merge_node_relations_no_conflict():
    n2_no_relation: SimpleNode = SimpleNode(
        name="n2",
        simple_attr_with_default="attr_n2",
    )
    n2: SimpleNode = SimpleNode(
        name="n2",
        simple_attr_with_default="attr_n2",
        related_to=[
            SimpleNode(name="n5")
        ]
    )
    n2_merged = base.models._merge_base_node(n2, n2_no_relation)


def test_merge_node_relations_with_conflict():
    n2_no_relation: SimpleNode = SimpleNode(
        name="n2",
        simple_attr_with_default="attr_n2",
        related_to=[
            SimpleNode(name="n4")
        ]
    )
    n2: SimpleNode = SimpleNode(
        name="n2",
        simple_attr_with_default="attr_n2",
        related_to=[
            SimpleNode(name="n5")
        ]
    )
    with pytest.raises(ValueError, match="Merge conflict on dict: Key related_to."):
        base.models._merge_base_node(n2, n2_no_relation)


def test_first_level_adding_to_graph_with_merging_and_branching_nodes():
    graph: BaseGraphModel = BaseGraphModel()

    n1: SimpleNode = SimpleNode(
        name="n1",
        simple_attr_with_default="attr_n1",
        related_to=[
            SimpleNode(name="n2"),
            SimpleNode(name="n3")
        ]
    )
    n2: SimpleNode = SimpleNode(
        name="n2",
        simple_attr_with_default="attr_n2",
        related_to=[
            SimpleNode(name="n5"),
        ]
    )
    n3: SimpleNode = SimpleNode(name="n3", simple_attr_with_default="attr_n3")
    n4: SimpleNode = SimpleNode(
        name="n4",
        simple_attr_with_default="attr_n4",
        related_to=[
            SimpleNode(name="n2"),
        ]
    )
    n5: SimpleNode = SimpleNode(name="n5", simple_attr_with_default="attr_n5")

    graph.add_node(n1)
    graph.add_node(n2)
    graph.add_node(n3)
    graph.add_node(n4)
    graph.add_node(n5)

    assert len(graph.base_nodes["n4"].relations) == 1
    assert graph.base_nodes["n4"].relations["related_to"] is n2
