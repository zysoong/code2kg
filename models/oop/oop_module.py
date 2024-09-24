from pydantic import BaseModel, Field

from base.models import BaseGraphNodeModel


class OOPModule(BaseGraphNodeModel):

    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    module_name: str = Field(...)

    def node_id(self) -> str:
        return "qualified_name"

    def node_attr(self) -> list[str]:
        return ["module_name"]

    def outgoing_relations(self) -> list[str]:
        return []
