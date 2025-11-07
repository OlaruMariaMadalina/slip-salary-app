from sqlalchemy import Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Timesheet(Base):
    """
    SQLAlchemy model for the 'timesheets' table.

    Attributes:
        id (int): Primary key for the timesheet entry.
        work_date (date): The date of the work entry.
        hours_worked (int): Number of hours worked on the given date.
        employee_id (int): Foreign key referencing the employee.
        employee (Employee): Relationship to the Employee model.

    Table Constraints:
        UniqueConstraint on (employee_id, work_date): Ensures one timesheet per employee per date.
    """
    __tablename__ = "timesheets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    work_date: Mapped[Date] = mapped_column(Date, nullable=False)
    hours_worked: Mapped[int] = mapped_column(Integer, nullable=False)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    employee = relationship("Employee", back_populates="timesheets")
    
    __table_args__ = (
        UniqueConstraint("employee_id", "work_date", name="uq_timesheet_per_employee_date"),
    )

