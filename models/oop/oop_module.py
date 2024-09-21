from pydantic import BaseModel, Field


class OOPModule(BaseModel):
    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    type: str = Field(default="oop_module")
