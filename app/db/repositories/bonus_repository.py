from app.models.bonus import Bonus
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

async def sum_bonus_by_employee_id(
    db: AsyncSession,
    employee_id: str,
    start_date: date,
    end_date: date
) -> float:
    res = await db.execute(
        select(func.sum(Bonus.bonus_amount)).where(
            Bonus.employee_id == employee_id,
            Bonus.bonus_date >= start_date,
            Bonus.bonus_date <= end_date
        )
    )
    return res.scalar() or 0.0