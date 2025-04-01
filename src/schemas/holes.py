"""
This file contains the Pydantic models for the Hole model.
"""

from pydantic import BaseModel, ConfigDict


class HoleBase(BaseModel):
    hole_number: int
    par: int | None = None
    distance: int | None = None

    model_config = ConfigDict(extra="forbid")


class HoleCreate(HoleBase):
    pass


class HoleUpdate(HoleBase):
    pass


class HoleInDBBase(HoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None
    layout_id: int | None = None


class Hole(HoleInDBBase):
    pass


class HoleInDB(HoleInDBBase):
    pass
