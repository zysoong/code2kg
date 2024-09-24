from typing import List
from pydantic import BaseModel, Field

from base.models import BaseGraphNodeModel
from models.oop import OOPModule


class OOPClass(BaseGraphNodeModel):
    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    name: str = Field(...)
    code: str = Field(default=None)
    super_classes: List["OOPClass"] = Field(...)
    within: "OOPClass" | OOPModule = Field(...)

    def node_id(self) -> str:
        return "qualified_name"

    def node_attr(self) -> list[str]:
        return ["name", "code"]

    def outgoing_relations(self) -> list[str]:
        return ["super_classes", "within"]

    def __init__(
            self,
            qualified_name: str,
            class_name: str,
            code: str | None,
            super_classes: List,
            within: "OOPClass" | OOPModule
    ):
        if self in super_classes:
            raise ValueError("Recursive class inherit detected.")
        if self == self.within:
            raise ValueError("Recursive class aggregation detected.")
        super().__init__(qualified_name=qualified_name, class_name=class_name,
                         code=code, super_classes=super_classes, within=within)
