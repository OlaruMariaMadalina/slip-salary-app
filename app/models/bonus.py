from dataclasses import fields
from sqlalchemy import Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from sqlalchemy import TIMESTAMP, func
from datetime import datetime

class Bonus(Base):
    __tablename__ = "bonuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bonus_amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    bonus_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee = relationship("Employee", back_populates="bonuses")

