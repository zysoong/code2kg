from pydantic import BaseModel, Field


class OOPFunction(BaseModel):
    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    summary: str = Field(default=None)
    code: str = Field(default=None)
