from typing import Annotated

from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    name: Annotated[str, Field(max_length=64, min_length=3)]
    color: Annotated[str, Field(max_length=7, min_length=7)]
    icon: Annotated[str, Field(max_length=255)]