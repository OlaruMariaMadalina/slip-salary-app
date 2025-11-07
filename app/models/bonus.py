from dataclasses import fields
from sqlalchemy import Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from sqlalchemy import TIMESTAMP, func
from datetime import datetime

class Bonus(Base):
    __tablename__ = "bonuses"
    """
    SQLAlchemy model for the 'bonuses' table.

    Attributes:
        id (int): Primary key for the bonus entry.
        bonus_amount (float): The amount of the bonus.
        bonus_date (datetime): The date and time when the bonus was granted.
        employee_id (int): Foreign key referencing the employee who received the bonus.
        employee (Employee): Relationship to the Employee model.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bonus_amount: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
    bonus_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee = relationship("Employee", back_populates="bonuses")

