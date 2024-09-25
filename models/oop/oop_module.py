from pydantic import Field

from base.models import BaseGraphNodeModel


class OOPModule(BaseGraphNodeModel):

    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")

    def node_id(self) -> str:
        return "qualified_name"

    def node_attr(self) -> list[str]:
        return []

    def outgoing_relations(self) -> list[str]:
        return []
