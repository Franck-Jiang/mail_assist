from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base

class Credentials(Base):
    __tablename__ = "credentials"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True)
    credentials_json: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<Credentials id={self.name} email={self.credentials_json}>"