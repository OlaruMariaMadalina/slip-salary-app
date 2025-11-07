from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee
from app.models.department import Department

async def get_employee_by_email(db: AsyncSession, email: str) -> Employee | None:
    """
    Retrieve an employee by their email address.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        email (str): The email address of the employee.

    Returns:
        Employee | None: The Employee object if found, otherwise None.
    """
    res = await db.execute(select(Employee).where(Employee.email == email))
    return res.scalars().first()

async def get_employee_by_id(db: AsyncSession, employee_id: int) -> Employee | None:
    """
    Retrieve an employee by their ID.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        employee_id (int): The ID of the employee.

    Returns:
        Employee | None: The Employee object if found, otherwise None.
    """
    res = await db.execute(select(Employee).where(Employee.id == employee_id))
    return res.scalars().first()

async def is_department_manager(db: AsyncSession, employee_id: int) -> bool:
    """
    Check if an employee is a manager of any department.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        employee_id (int): The ID of the employee.

    Returns:
        bool: True if the employee is a department manager, False otherwise.
    """
    res = await db.execute(select(exists().where(Department.manager_id == employee_id)))
    return bool(res.scalar())

async def get_employees_by_department_id(db: AsyncSession, department_id: str) -> list[Employee]:
    """
    Retrieve all employees belonging to a specific department.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        department_id (str): The ID of the department.

    Returns:
        list[Employee]: A list of Employee objects belonging to the department.
    """
    res = await db.execute(select(Employee).where(Employee.department_id == department_id))
    return res.scalars().all()
