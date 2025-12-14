from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base

class Mail(Base):
    __tablename__ = "mails"

    mail_id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    source: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime)
    subject: Mapped[str]
    body: Mapped[str] = mapped_column()

