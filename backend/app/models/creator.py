from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Creator(Base):
    __tablename__ = "creators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    platform: Mapped[str] = mapped_column(String(30), nullable=False)

