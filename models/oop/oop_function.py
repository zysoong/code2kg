from typing import List

from pydantic import BaseModel, Field

from base.models import BaseGraphNodeModel
from models.oop import OOPClass, OOPModule


class OOPFunction(BaseGraphNodeModel):

    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    signature: str = Field(...)
    code: str = Field(default=None)
    summary: str = Field(default="")
    flat_function_calls: List["OOPFunction"] = Field(default=[])
    within: "OOPFunction" | OOPClass | OOPModule = Field(...)

    def node_id(self) -> str:
        return "qualified_name"

    def node_attr(self) -> list[str]:
        return ["signature", "code"]

    def outgoing_relations(self) -> list[str]:
        return ["flat_function_calls", "within"]

    def __init__(
            self,
            qualified_name: str,
            signature: str,
            code: str | None,
            within: "OOPFunction" | OOPClass | OOPModule
    ):
        if self == self.within:
            raise ValueError("Recursive function aggregation detected.")
        super().__init__(
            qualified_name=qualified_name,
            signature=signature,
            code=code,
            within=within
        )
