from datetime import datetime
from typing import Dict, Any

from sqlalchemy import Integer, String, DateTime, Boolean, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column

from constants.locarions import Locations
from db_models.base import Base


class MovieDBModel(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    location: Mapped[Locations] = mapped_column(Enum(Locations))
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    rating: Mapped[float] = mapped_column(Float)
    genre_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=lambda: datetime.now())

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "location": self.location,
            "published": self.published,
            "rating": self.rating,
            "genre_id": self.genre_id,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Movie(id='{self.id}', name='{self.name}', price='{self.price}'>"
