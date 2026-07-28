from __future__ import annotations
from sqlalchemy import DateTime, String,Text,ForeignKey,Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime


from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

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
    
    user: Mapped["User"] = relationship(
    back_populates="reviews"
)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable = False
    )