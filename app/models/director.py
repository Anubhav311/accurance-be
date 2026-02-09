from pydantic import BaseModel, Field
from typing import Literal
# from .common import Address

class Director(BaseModel):
    name: str = Field(..., min_length=2)
    din: str = Field(..., pattern=r"^\d{8}$")
    designation: Literal[
        "Director",
        "Manager",
        "Whole Time Director",
        "Managing Director",
    ]
    address: str = Field(..., min_length=10)
