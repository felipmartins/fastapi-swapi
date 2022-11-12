import os

from fastapi import FastAPI
from sqlmodel import Session, select
from .db import create_db_and_tables, engine, populate_all_tables

from swapi.model import Planet

app = FastAPI()


@app.on_event("startup")
def on_startup():
    if not os.path.exists("database.sqlite"):
        create_db_and_tables()
        with Session(engine) as session:
            populate_all_tables(session)
    else:
        create_db_and_tables


def create_response(result):
    return {
        "count": len(result),
        "next": None,
        "previous": None,
        "results": result,
    }


@app.get("/api/planets/")
async def list_planets():
    with Session(engine) as session:
        planets = session.exec(select(Planet)).all()

    return create_response(planets)
