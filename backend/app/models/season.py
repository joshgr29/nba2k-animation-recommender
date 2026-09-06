from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)

    game_edition_id: Mapped[int] = mapped_column(
        ForeignKey("game_editions.id"),
        nullable=False,
    )

    number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
