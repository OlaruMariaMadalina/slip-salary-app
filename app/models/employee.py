from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Date, DECIMAL, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from sqlalchemy import TIMESTAMP, func
from datetime import date, datetime

if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.user_account import UserAccount
    from app.models.bonus import Bonus
    from app.models.paycheck import Paycheck
    from app.models.timesheet import Timesheet
    from app.models.vacation import Vacation
    
class Employee(Base):
    """
    SQLAlchemy model for the 'employees' table.

    Attributes:
        id (int): Primary key for the employee.
        first_name (str): First name of the employee.
        last_name (str): Last name of the employee.
        personal_identification_number (str): Unique personal identification number.
        email (str): Unique email address of the employee.
        job_title (str): Job title of the employee.
        hire_date (date): Date when the employee was hired.
        active (bool): Indicates if the employee is currently active.
        base_salary (Decimal): Base salary of the employee.
        created_at (datetime): Timestamp when the employee record was created.
        department_id (int|None): Foreign key referencing the department.
        department (Department): Relationship to the Department model.
        user_account (UserAccount): Relationship to the UserAccount model.
        managed_department (Department): Relationship to the Department managed by this employee.
        bonuses (list[Bonus]): List of bonuses received by the employee.
        vacations (list[Vacation]): List of vacations taken by the employee.
        paychecks (list[Paycheck]): List of paychecks for the employee.
        timesheets (list[Timesheet]): List of timesheets for the employee.
    """
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    personal_identification_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    job_title: Mapped[str] = mapped_column(String(64), nullable=False)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False, default=True)
    base_salary: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    department_id: Mapped[int|None] = mapped_column(ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
    user_account: Mapped["UserAccount"] = relationship("UserAccount", back_populates="employee", uselist=False)
    
    managed_department: Mapped["Department"] = relationship(
        "Department",
        back_populates="manager",
        uselist=False,
        foreign_keys="Department.manager_id",
    )
    
    bonuses: Mapped[list["Bonus"]] = relationship("Bonus", back_populates="employee")
    vacations: Mapped[list["Vacation"]] = relationship("Vacation", back_populates="employee")
    paychecks: Mapped[list["Paycheck"]] = relationship("Paycheck", back_populates="employee")
    timesheets: Mapped[list["Timesheet"]] = relationship("Timesheet", back_populates="employee")