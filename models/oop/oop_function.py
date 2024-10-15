from typing import List, Union

from pydantic import Field

from base.models import BaseGraphNodeModel
from models.oop import OOPClass, OOPModule


class OOPFunction(BaseGraphNodeModel):

    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    signature: str = Field(...)
    code: str = Field(...)
    summary: str = Field(default="")
    flat_function_calls: List["OOPFunction"] = Field(..., default_factory=list)
    within: List[Union["OOPFunction", OOPModule, OOPClass]] = Field(..., default_factory=list)

    def node_id(self) -> str:
        return "qualified_name"

    def node_attr(self) -> list[str]:
        return ["signature", "code"]

    def outgoing_relations(self) -> list[str]:
        return ["flat_function_calls", "within"]

    # TODO construct with flexible parameters
    def __init__(
            self,
            qualified_name: str,
            signature: str,
            code: str,
            flat_function_calls: list,
            within: list
    ):
        if self == within:
            raise ValueError("Recursive function aggregation detected.")

        super().__init__(
            qualified_name=qualified_name,
            signature=signature,
            code=code,
            flat_function_calls=flat_function_calls,
            within=within
        )
