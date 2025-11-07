from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.employee import Employee
    
class Department(Base):
    """
    SQLAlchemy model for the 'departments' table.

    Attributes:
        id (int): Primary key for the department.
        department_name (str): Unique name of the department.
        department_description (str): Description of the department.
        manager_id (int): Foreign key referencing the manager (employee) of the department.
        manager (Employee): Relationship to the Employee model for the manager.
        employees (list[Employee]): List of employees belonging to the department.
    """
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    department_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    department_description: Mapped[str] = mapped_column(String, nullable=False)

    manager_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL", use_alter=True),
        nullable=True, 
        unique=True
    )
    manager: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="managed_department",
        foreign_keys=[manager_id],
        uselist=False,
    )

    employees: Mapped[list["Employee"]] = relationship(
        "Employee", 
        back_populates="department",
        foreign_keys="Employee.department_id",
    )