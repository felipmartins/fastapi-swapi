from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class PlanetBase(SQLModel):
    name: str = Field(max_length=100)
    rotation_period: str = Field(max_length=50)
    orbital_period: str = Field(max_length=50)
    diameter: str = Field(max_length=50)
    climate: str = Field(max_length=50)
    gravity: str = Field(max_length=50)
    terrain: str = Field(max_length=50)
    surface_water: str = Field(max_length=50)
    population: str = Field(max_length=50)
    residents: List["People"] = Relationship(back_populates="homeworld")


class Planet(PlanetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PlanetCreate(PlanetBase):
    pass


class PlanetRead(PlanetBase):
    id: int


class PeopleBase(SQLModel):
    name: str = Field(max_length=100)
    height: str = Field(max_length=50)
    mass: str = Field(max_length=50)
    hair_color: str = Field(max_length=50)
    skin_color: str = Field(max_length=50)
    eye_color: str = Field(max_length=50)
    birth_year: str = Field(max_length=50)
    gender: str = Field(max_length=50)
    planet_id: int = Field(default=None, foreign_key="planet.id")
    homeworld: Planet = Relationship(back_populates="residents")


class People(PeopleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    

class PeopleCreate(PeopleBase):
    pass


class PeopleRead(PeopleBase):
    id: int
