from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class GameEdition(Base):
    __tablename__ = "game_editions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    release_date: Mapped[date] = mapped_column(Date, nullable=False)