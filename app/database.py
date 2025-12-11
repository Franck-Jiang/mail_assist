import os
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from sqlalchemy import create_engine

DB_CONNECTION = os.getenv("db_connection")
DB_NAME = os.getenv("db_name")
DB_USER = os.getenv("db_user")
DB_SYS = os.getenv("db_sys")

class Base(DeclarativeBase):
    pass

engine = create_engine(f"{DB_SYS}://{DB_USER}@{DB_CONNECTION}/{DB_NAME}", echo=True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

