from app.models.vacation import Vacation
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

async def count_vacation_days_by_employee_id(
    db: AsyncSession,
    employee_id: str,
    start_date: date,
    end_date: date
) -> int:

    res = await db.execute(
        select(Vacation.start_date, Vacation.end_date).where(
            Vacation.employee_id == employee_id,
            Vacation.end_date >= start_date,
            Vacation.start_date <= end_date
        )
    )
    vacations = res.all()
    total_days = 0
    for vac_start, vac_end in vacations:

        overlap_start = max(vac_start, start_date)
        overlap_end = min(vac_end, end_date)
        days = (overlap_end - overlap_start).days + 1
        if days > 0:
            total_days += days
    return total_days
