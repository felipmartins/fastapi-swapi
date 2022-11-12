import json
from sqlmodel import SQLModel, create_engine
from .model import Planet

sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def populate_table_planets(session):
    with open("data/planets.json") as file:
        planets = json.load(file)

    for each_planet in planets:
        planet = Planet(
            id=each_planet["id"],
            name=each_planet["name"],
            rotation_period=each_planet["rotation_period"],
            orbital_period=each_planet["orbital_period"],
            diameter=each_planet["diameter"],
            climate=each_planet["climate"],
            gravity=each_planet["gravity"],
            terrain=each_planet["terrain"],
            surface_water=each_planet["surface_water"],
            population=each_planet["population"],
        )

        session.add(planet)
        session.commit()


def populate_all_tables(session):
    populate_table_planets(session)
