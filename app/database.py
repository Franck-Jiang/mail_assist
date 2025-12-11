import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

DB_CONNECTION = os.getenv("db_conneciton")
DB_NAME = os.getenv("db_name")
DB_USER = os.getenv("db_user")
DB_SYS = os.getenv("db_sys")

class Base(DeclarativeBase):
    pass

engine = create_engine(f"{DB_SYS}://{DB_USER}@{DB_CONNECTION}/{DB_NAME}", echo=True)
Base.metadata.create_all(engine)