from typing import List

from pydantic import BaseModel, Field


class OOPFile(BaseModel):
    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    summary: str = Field(default=None)
    first_level_function_calls: List = Field(default=[])
