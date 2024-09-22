from typing import List

from pydantic import BaseModel, Field

from models.oop import OOPClass, OOPModule


class OOPFunction(BaseModel):
    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    signature: str = Field(...)
    node_type: str = Field(default="oop_function")
    code: str = Field(default=None)
    flat_function_calls: List["OOPFunction"] = Field(default=[])
    within: "OOPFunction" | OOPClass | OOPModule = Field(...)

    def __init__(
            self,
            qualified_name: str,
            signature: str,
            code: str | None,
            flat_function_calls: List,
            within: "OOPFunction" | OOPClass | OOPModule
    ):
        if self == self.within:
            raise ValueError("Recursive function aggregation detected.")
        super().__init__(
            qualified_name=qualified_name,
            signature=signature,
            code=code,
            flat_function_calls=flat_function_calls,
            within=within
        )
