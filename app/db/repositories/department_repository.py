from app.models.department import Department
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_department_by_employee_id(db: AsyncSession, employee_id: str) -> Department | None:
    res = await db.execute(select(Department).where(Department.manager_id == employee_id))
    return res.scalars().first()
