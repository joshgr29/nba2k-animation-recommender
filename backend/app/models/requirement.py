from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Requirement(Base):
    __tablename__ = ("requirements")

    id: Mapped[int] = mapped_column(primary_key=True)

    requirement_group_id: Mapped[int] = mapped_column(ForeignKey("requirement_groups.id"), nullable=False)

    attribute_id: Mapped[int] = mapped_column(ForeignKey("attributes.id"), nullable=False)

    operator: Mapped[str] = mapped_column(String(5), nullable=False)

    value: Mapped[int] = mapped_column(Integer, nullable=False)