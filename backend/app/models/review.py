from sqlalchemy import DateTime, String,Text,ForeignKey,Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key = True,index = True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default = datetime.utcnow,onupdate = datetime.utcnow)
    feedback: Mapped[str] = mapped_column(
    Text,
    nullable=False,
)

    user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id"),
    nullable=False,
    index=True,
)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable = False
    )