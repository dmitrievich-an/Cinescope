from datetime import datetime
from typing import Dict, Any

from sqlalchemy import String, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from constants.roles import Roles
from db_models.base import Base


class UserDBModel(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    banned: Mapped[bool] = mapped_column(Boolean, default=False)
    roles: Mapped[list[Roles]] = mapped_column(
        ARRAY(Enum(Roles, name="Role", create_type=False)),  # <-- ВАЖНО
        default=[Roles.USER]
    )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "verified": self.verified,
            "banned": self.banned,
            "roles": self.roles
        }

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}'>"
