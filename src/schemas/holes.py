"""
Schema for the Hole model.
"""

from pydantic import BaseModel
from typing import Optional


class HoleBase(BaseModel):
    hole_number: int
    par: int
    distance: Optional[int] = None


class HoleCreate(HoleBase):
    layout_id: int


class HoleUpdate(HoleBase):
    pass


class HoleInDBBase(HoleBase):
    id: int
    layout_id: int

    class Config:
        orm_mode = True


class Hole(HoleInDBBase):
    pass


class HoleInDB(HoleInDBBase):
    pass
