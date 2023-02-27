from sqlmodel import SQLModel, create_engine

# Define filename and DB url
sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# We don't need check_same_thread because
# we'll use one session per request
connect_args = {"check_same_thread": False}

# Create the engine
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    # All models need to be loaded before
    # SQLModel is able to find them. So we
    # import the model module even though
    # we don't use it explicitly.
    from . import model  # noqa: F401

    # This code creates all tables from classes that
    # inherit from SQLModel and have table=true
    SQLModel.metadata.create_all(engine)