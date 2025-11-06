from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee
from app.models.department import Department

async def get_employee_by_email(db: AsyncSession, email: str) -> Employee | None:
    res = await db.execute(select(Employee).where(Employee.email == email))
    return res.scalars().first()

async def get_employee_by_id(db: AsyncSession, employee_id: int) -> Employee | None:
    res = await db.execute(select(Employee).where(Employee.id == employee_id))
    return res.scalars().first()

async def is_department_manager(db: AsyncSession, employee_id: int) -> bool:
    res = await db.execute(select(exists().where(Department.manager_id == employee_id)))
    return bool(res.scalar())

async def get_employees_by_department_id(db: AsyncSession, department_id: str) -> list[Employee]:
    res = await db.execute(select(Employee).where(Employee.department_id == department_id))
    return res.scalars().all()
