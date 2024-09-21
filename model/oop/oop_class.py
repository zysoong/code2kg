from typing import List
from pydantic import BaseModel, Field
from model.oop.oop_module import OOPModule


class OOPClass(BaseModel):
    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    code: str = Field(default=None)
    super_classes: List["OOPClass"] = Field(...)
    within: "OOPClass" | OOPModule = Field(...)

    def __init__(
            self,
            qualified_name: str,
            code: str | None,
            super_classes: List,
            within: "OOPClass" | OOPModule
    ):
        if self in super_classes:
            raise ValueError("Recursive class inherit detected.")
        if self == self.within:
            raise ValueError("Recursive class aggregation detected.")
        super().__init__(qualified_name=qualified_name, code=code, super_classes=super_classes, within=within)
