from sqlalchemy import Integer, ForeignKey, Date, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

from app.models.employee import Employee

class Timesheet(Base):
    __tablename__ = "timesheets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    work_date: Mapped[Date] = mapped_column(Date, nullable=False)
    hours_worked: Mapped[int] = mapped_column(Integer, nullable=False)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee: Mapped["Employee"] = relationship("Employee", back_populates="timesheets")
    
    __table_args__ = (
        UniqueConstraint("employee_id", "work_date", name="uq_timesheet_per_employee_date"),
    )

