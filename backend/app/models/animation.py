from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Animation(Base):
    __tablename__ = "animations"

    id: Mapped[int] = mapped_column(primary_key=True)

    game_edition_id: Mapped[int] = mapped_column(
        ForeignKey("game_editions.id"),
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("animation_categories.id"),
        nullable=False,
    )

    introduced_season_id: Mapped[int | None] = mapped_column(
        ForeignKey("seasons.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)