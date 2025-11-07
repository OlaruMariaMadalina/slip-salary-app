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
    """
    Calculate the total bonus amount for a given employee within a date range.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        employee_id (str): The ID of the employee.
        start_date (date): The start date of the period.
        end_date (date): The end date of the period.

    Returns:
        float: The sum of bonuses for the employee in the specified period. Returns 0.0 if no bonuses are found.
    """
    res = await db.execute(
        select(func.sum(Bonus.bonus_amount)).where(
            Bonus.employee_id == employee_id,
            Bonus.bonus_date >= start_date,
            Bonus.bonus_date <= end_date
        )
    )
    return res.scalar() or 0.0