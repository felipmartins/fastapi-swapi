from typing import Optional
from sqlmodel import SQLModel, Field


class Planet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=100)

    rotation_period: str = Field(max_length=50)
    orbital_period: str = Field(max_length=50)
    diameter: str = Field(max_length=50)
    climate: str = Field(max_length=50)
    gravity: str = Field(max_length=50)
    terrain: str = Field(max_length=50)
    surface_water: str = Field(max_length=50)
    population: str = Field(max_length=50)
