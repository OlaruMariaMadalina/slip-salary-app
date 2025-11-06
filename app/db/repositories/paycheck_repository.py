from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.paycheck import Paycheck


async def create_paycheck_for_employee(
    db: AsyncSession,
    employee_id: int,
    pay_month: int,
    pay_year: int,
) -> Paycheck:
    paycheck = Paycheck(
        employee_id=employee_id,
        pay_month=pay_month,
        pay_year=pay_year,
        sent_to_employee=True,
    )
    db.add(paycheck)
    await db.flush()
    await db.commit()
    return paycheck

async def get_paycheck_by_employee_and_month(
    db: AsyncSession,
    employee_id: int,
    pay_month: int,
    pay_year: int,
) -> Paycheck | None:
    result = await db.execute(select(Paycheck).where(
        Paycheck.employee_id == employee_id,
        Paycheck.pay_month == pay_month,
        Paycheck.pay_year == pay_year,
    ))

    return result.scalars().first()