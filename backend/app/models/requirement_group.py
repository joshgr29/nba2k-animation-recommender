from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class RequirementGroup(Base):
    __tablename__ = "requirement_groups"

    id: Mapped[int] = mapped_column(primary_key=True)

    animation_id: Mapped[int] = mapped_column(
        ForeignKey("animations.id"),
        nullable=False,
    )

    logical_operator: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

