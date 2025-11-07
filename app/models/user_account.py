from datetime import datetime

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime


from app.models.employee import Employee
from app.db.base import Base

class UserAccount(Base):
    """
    SQLAlchemy model for the 'user_accounts' table.

    Attributes:
        id (int): Primary key for the user account.
        username (str): Unique username or email for the user.
        hashed_password (str): Hashed password for authentication.
        role (str): Role of the user (e.g., 'user', 'admin').
        is_active (bool): Indicates if the user account is active.
        created_at (datetime): Timestamp when the account was created.
        updated_at (datetime): Timestamp when the account was last updated.
        employee_id (int): Foreign key referencing the associated employee.
        employee (Employee): Relationship to the Employee model.
    Table Constraints:
        UniqueConstraint on username and employee_id: Ensures unique user accounts per employee.
    """
    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="user")
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        unique=True, 
    )
    employee: Mapped["Employee"] = relationship("Employee", back_populates="user_account", uselist=False)