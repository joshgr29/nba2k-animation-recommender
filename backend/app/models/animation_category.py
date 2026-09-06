from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AnimationCategory(Base):
    __tablename__ = "animation_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    