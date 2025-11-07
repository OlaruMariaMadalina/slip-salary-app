from app.models.department import Department
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_department_by_employee_id(db: AsyncSession, employee_id: str) -> Department | None:
    """
    Retrieve the department managed by a specific employee.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        employee_id (str): The ID of the employee (manager).

    Returns:
        Department | None: The Department object if found, otherwise None.
    """    
    res = await db.execute(select(Department).where(Department.manager_id == employee_id))
    return res.scalars().first()
