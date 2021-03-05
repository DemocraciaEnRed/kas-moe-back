import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


DB_URL = "sqlite:///./app.db"

engine = create_engine(
    DB_URL, connect_args={"check_same_thread": False},
)

database = databases.Database(DB_URL)

Base: DeclarativeMeta = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)
