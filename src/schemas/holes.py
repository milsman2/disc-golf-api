"""
This file contains the Pydantic models for the Hole model.
"""

from pydantic import BaseModel, ConfigDict


class HoleBase(BaseModel):
    hole_name: str
    par: int | None = None
    distance: int | None = None


class HoleCreate(HoleBase):
    pass


class HoleUpdate(HoleBase):
    pass


class HoleInDBBase(HoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    layout_id: int | None = None


class HolePublic(HoleInDBBase):
    pass
