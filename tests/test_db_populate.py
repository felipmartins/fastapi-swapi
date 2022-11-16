import json
import pytest
from unittest.mock import patch, mock_open
from sqlmodel import create_engine, Session, SQLModel, select
from sqlmodel.pool import StaticPool
from swapi.db import populate_table_planets, populate_table_people
from swapi.model import Planet, People


@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    return engine


@pytest.fixture
def fake_planets_data():
    return [
        {
            "id": 1,
            "name": "Tatooine",
            "rotation_period": "23",
            "orbital_period": "304",
            "diameter": "10465",
            "climate": "arid",
            "gravity": "1 standard",
            "terrain": "desert",
            "surface_water": "1",
            "population": "200000",
        },
        {
            "id": 2,
            "name": "Alderaan",
            "rotation_period": "24",
            "orbital_period": "364",
            "diameter": "12500",
            "climate": "temperate",
            "gravity": "1 standard",
            "terrain": "grasslands, mountains",
            "surface_water": "40",
            "population": "2000000000",
        },
    ]


@pytest.fixture
def fake_people_data():
    return [
        {
            "id": 1,
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "skin_color": "fair",
            "eye_color": "blue",
            "birth_year": "19BBY",
            "gender": "male",
            "planet_id": "1",
        },
        {
            "id": 2,
            "name": "C-3PO",
            "height": "167",
            "mass": "75",
            "hair_color": "n/a",
            "skin_color": "gold",
            "eye_color": "yellow",
            "birth_year": "112BBY",
            "gender": "n/a",
            "planet_id": "1",
        },
    ]


def test_populate_table_planet(engine, fake_planets_data):
    with (
        patch("builtins.open", mock_open(read_data=json.dumps(fake_planets_data))),
        Session(engine) as session,
    ):
        populate_table_planets(session)

        planets = session.exec(select(Planet)).all()

        assert len(planets) == len(fake_planets_data)


def test_populate_table_people(engine, fake_people_data):
    with (
        patch("builtins.open", mock_open(read_data=json.dumps(fake_people_data))),
        Session(engine) as session,
    ):
        populate_table_people(session)

        people = session.exec(select(People)).all()

        assert len(people) == len(fake_people_data)
