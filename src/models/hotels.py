from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint

from src.database import Base


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(CITEXT)
    location: Mapped[str] = mapped_column(CITEXT)

    __table_args__ = (
        UniqueConstraint("title", "location", name="uix_title_location"),
    )