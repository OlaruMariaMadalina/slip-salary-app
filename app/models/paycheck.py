from sqlalchemy import String, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.employee import Employee
from sqlalchemy import TIMESTAMP, func
from datetime import datetime
    
class Paycheck(Base):
    __tablename__ = "paychecks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pay_month: Mapped[Date] = mapped_column(Date, nullable=False)
    department_description: Mapped[str] = mapped_column(String, nullable=False)
    sent_to_employee: Mapped[bool] = mapped_column(nullable=False, default=True)
    sent_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee: Mapped["Employee"] = relationship("Employee", back_populates="paychecks")
    
    __table_args__ = (
        UniqueConstraint("employee_id", "pay_month", name="uq_paycheck_per_pay_month"),
    )
