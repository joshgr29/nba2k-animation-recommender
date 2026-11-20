from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class AnimationReview(Base):
    __tablename__ = "animation_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("community_sources.id"), nullable=False)
    animation_id: Mapped[int] = mapped_column(ForeignKey("animations.id"), nullable=False)
    opinion: Mapped[str] = mapped_column(String(20), nullable=False)

    