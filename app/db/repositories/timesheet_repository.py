from app.models.timesheet import Timesheet
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

async def count_working_days_by_employee_id(
    db: AsyncSession,
    employee_id: str,
    start_date: date,
    end_date: date
) -> int:
    res = await db.execute(
        select(func.count()).where(
            Timesheet.employee_id == employee_id,
            Timesheet.work_date >= start_date,
            Timesheet.work_date <= end_date
        )
    )
    return res.scalar() or 0
