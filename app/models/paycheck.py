from sqlalchemy import String, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from sqlalchemy import TIMESTAMP, func
from datetime import datetime
    
class Paycheck(Base):
    """
    SQLAlchemy model for the 'paychecks' table.

    Attributes:
        id (int): Primary key for the paycheck.
        pay_month (int): The month for which the paycheck is issued.
        pay_year (int): The year for which the paycheck is issued.
        sent_to_employee (bool): Indicates if the paycheck has been sent to the employee.
        sent_at (datetime): Timestamp when the paycheck was sent.
        employee_id (int): Foreign key referencing the employee who receives the paycheck.
        employee (Employee): Relationship to the Employee model.
    Table Constraints:
        UniqueConstraint on (employee_id, pay_month, pay_year): Ensures one paycheck per employee per month/year.
    """
    __tablename__ = "paychecks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pay_month: Mapped[Integer] = mapped_column(Integer, nullable=False)
    pay_year: Mapped[Integer] = mapped_column(Integer, nullable=False)
    sent_to_employee: Mapped[bool] = mapped_column(nullable=False, default=True)
    sent_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee = relationship("Employee", back_populates="paychecks")
    __table_args__ = (
        UniqueConstraint("employee_id", "pay_month", "pay_year", name="uq_paycheck_per_pay_month"),
    )
