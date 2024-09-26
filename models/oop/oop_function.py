from typing import List

from pydantic import BaseModel, Field

from base.models import BaseGraphNodeModel
from models.oop import OOPClass, OOPModule


class OOPFunction(BaseGraphNodeModel):

    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    signature: str = Field(...)
    code: str = Field(...)
    summary: str = Field(default="")
    flat_function_calls: List["OOPFunction"] = Field(...)
    within: BaseGraphNodeModel = Field(...)

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
            code: str,
            flat_function_calls: list["OOPFunction"],
            within: BaseGraphNodeModel
    ):
        if self == within:
            raise ValueError("Recursive function aggregation detected.")
        if not isinstance(within, OOPFunction) and \
                not isinstance(within, OOPClass) and\
                not isinstance(within, OOPModule):
            raise ValueError(f"OOPFunction must within another OOPFunction, OOPClass or OOPModule. "
                             f"Found {within.__class__}")
        for call_element in flat_function_calls:
            if not isinstance(call_element, OOPFunction):
                raise ValueError(f"flat_function_calls can only contain OOPFunction. "
                                 f"Found {call_element.__class__}")

        super().__init__(
            qualified_name=qualified_name,
            signature=signature,
            code=code,
            flat_function_calls=flat_function_calls,
            within=within
        )
