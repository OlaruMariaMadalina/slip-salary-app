from sqlalchemy import Integer, ForeignKey, Date, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

from app.models.employee import Employee

class Vacation(Base):
    __tablename__ = "vacations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee: Mapped["Employee"] = relationship("Employee", back_populates="vacations")
    
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="check_valid_vacation_dates"),
        UniqueConstraint("employee_id", "start_date", "end_date", name="uq_vacation_per_employee_dates"),
    )

