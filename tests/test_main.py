from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool
from unittest.mock import patch
from swapi.main import app
from fastapi.testclient import TestClient
from swapi.db import populate_all_tables
import pytest

client = TestClient(app)


@pytest.fixture
def single_planet_mock():
    return {
            "name": "new_planet",
            "rotation_period": "14",
            "orbital_period": "34",
            "diameter": "1045",
            "climate": "tropic",
            "gravity": "1 standard",
            "terrain": "planains",
            "surface_water": "1",
            "population": "50000",
            }


@pytest.fixture
def single_people_mock():
    return {
            "name": "Not Luke",
            "height": "170",
            "mass": "72",
            "hair_color": "dark",
            "skin_color": "fair",
            "eye_color": "green",
            "birth_year": "19BBY",
            "gender": "male",
            "planet_id": "1",
            }


def get_session_override():

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    populate_all_tables(session)

    return session


def test_get_planets_route():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 60


def test_planet_search_route_with_no_query():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/search/")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 60


def test_planet_search_route_with_name_only():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/search?name=Hoth")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 1


def test_planet_search_route_with_gravity_only():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/search?gravity=unknown")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 15


def test_planet_search_route_with_name_and_gravity():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/search?name=Hoth&gravity=unknown")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 0


def test_get_planet_by_id_route():
    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/1")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == 1


def test_post_planet_route(single_planet_mock):
    with patch("swapi.main.get_session", get_session_override):

        res = client.post("/api/planets/", json=single_planet_mock)
        assert res.status_code == 201
        data = res.json()
        assert data["id"] == 61


def test_get_people_route():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/people/")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 83


def test_get_people_by_id_route():
    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/people/1")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == 1


def test_post_people_route(single_people_mock):
    with patch("swapi.main.get_session", get_session_override):

        res = client.post("/api/people/", json=single_people_mock)
        assert res.status_code == 201
        data = res.json()
        assert data["id"] == 84
