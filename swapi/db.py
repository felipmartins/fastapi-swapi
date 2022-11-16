import json
from sqlmodel import SQLModel, create_engine
from .model import Planet, People

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


def populate_table_people(session):
    with open("data/people.json") as file:
        people = json.load(file)

    for each_person in people:
        person = People(
            id=each_person["id"],
            name=each_person["name"],
            height=each_person["height"],
            mass=each_person["mass"],
            hair_color=each_person["hair_color"],
            skin_color=each_person["skin_color"],
            eye_color=each_person["eye_color"],
            birth_year=each_person["birth_year"],
            gender=each_person["gender"],
            planet_id=each_person["planet_id"],
        )

        session.add(person)
        session.commit()


def populate_all_tables(session):
    populate_table_planets(session)
    populate_table_people(session)
