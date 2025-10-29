from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.employee import Employee
    
class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    department_name: Mapped[str] = mapped_column(String(64), nullable=False)
    department_description: Mapped[str] = mapped_column(String, nullable=False)

    manager_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL", use_alter=True),
        nullable=True
    )
    manager: Mapped["Employee"] = relationship("Employee", back_populates="managed_department")

    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="department")
