from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from swapi.db import create_db_and_tables, engine
from swapi.db_populate import populate_empty_tables
from swapi.model import Planet, PlanetCreate, PlanetRead

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5000",
    "http://rodrigo.com.br"
    
    # "*",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    return Session(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    with get_session() as session:
        populate_empty_tables(session)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def create_response(result):
    return {
        "count": len(result),
        "next": None,
        "previous": None,
        "results": result,
    }


@app.get("/api/planets/", tags=["planets"])
async def list_planets():
    with get_session() as session:
        planets = session.exec(select(Planet)).all()

        return create_response(planets)


@app.post("/api/planets/",  tags=["planets"], status_code=201)
async def create_planet(planet: PlanetCreate):
    with get_session() as session:
        db_planet = Planet.from_orm(planet)
        session.add(db_planet)
        session.commit()
        session.refresh(db_planet)
        return db_planet


@app.get("/api/planets/{id}", tags=["planets"], response_model=PlanetRead)
async def get_planet_by_id(id: int, session: Session = Depends(get_session)):
    return session.exec(select(Planet).where(Planet.id == id)).one()