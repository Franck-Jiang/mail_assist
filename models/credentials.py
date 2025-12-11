from sqlalchemy import Column, String, UUID
from app.database import Base

class Credentials(Base):
    __tablename__ = "credentials"

    id = Column(UUID, primary_key=True)
    credentials_json = Column(String)
