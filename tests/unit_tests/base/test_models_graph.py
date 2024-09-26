from pydantic import Field, ConfigDict

from base.models import BaseGraphNodeModel


class DummyNode(BaseGraphNodeModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = Field(...)
    relate_to: list[BaseGraphNodeModel] | BaseGraphNodeModel = Field(...)

    def node_id(self) -> str:
        return "name"

    def node_attr(self) -> list[str]:
        return []

    def outgoing_relations(self) -> list[str]:
        return ["relate_to"]
