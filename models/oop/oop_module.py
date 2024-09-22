from pydantic import BaseModel, Field


class OOPModule(BaseModel):
    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    module_name: str = Field(...)
    node_type: str = Field(default="oop_module")
