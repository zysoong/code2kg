from typing import List

from pydantic import BaseModel, Field


class OOPModule(BaseModel):
    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
