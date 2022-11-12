import json

from sqlmodel import create_engine, Session, SQLModel, select
from sqlmodel.pool import StaticPool
from swapi.db import populate_table_planets

from unittest.mock import patch, mock_open

import pytest

from swapi.model import Planet


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


def test_populate_table_planet(engine, fake_planets_data):
    with (
        patch(
            "builtins.open", mock_open(read_data=json.dumps(fake_planets_data))
        ),
        Session(engine) as session,
    ):
        populate_table_planets(session)

        planets = session.exec(select(Planet)).all()

        assert len(planets) == len(fake_planets_data)
