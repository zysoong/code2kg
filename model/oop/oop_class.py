from typing import List, Any

from pydantic import BaseModel, Field, model_validator


class OOPClass(BaseModel):
    qualified_name: str = Field(..., pattern=r"^[\w.]+(?:\.[\w]+)?$")
    summary: str = Field(default=None)
    code: str = Field(default=None)
    extends: List = Field(...)

    def __init__(
            self,
            qualified_name: str,
            summary: str | None, code: str | None,
            extends: List
    ):
        if self in extends:
            raise ValueError("Recursive class inherit detected.")
        super().__init__(qualified_name=qualified_name, summary=summary, code=code, extends=extends)
