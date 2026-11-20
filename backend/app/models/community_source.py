from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database import Base

class CommunitySource(Base):
    __tablename__ = "community_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("creators.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

