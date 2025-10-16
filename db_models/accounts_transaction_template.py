from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db_models.base import Base


class AccountTransactionTemplate(Base):
    __tablename__ = 'accounts_transaction_template'
    user: Mapped[str] = mapped_column(String(255), primary_key=True)
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
