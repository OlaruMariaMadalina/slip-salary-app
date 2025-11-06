import asyncio
from sqlalchemy import select
from app.db.engine import SessionLocal
from app.models.department import Department
from app.models.employee import Employee

async def show_all():
    async with SessionLocal() as session:
        print("\n--- Departamente ---")
        result = await session.execute(select(Department))
        departments = result.scalars().all()
        for dep in departments:
            print(f"Departament: {dep.department_name} (id={dep.id}) - descriere: {dep.department_description}")
            if dep.manager_id:
                manager = await session.get(Employee, dep.manager_id)
                if manager:
                    print(f"  Manager: {manager.first_name} {manager.last_name} (email: {manager.email})")
            emps = await session.execute(select(Employee).where(Employee.department_id == dep.id))
            for emp in emps.scalars().all():
                print(f"    Angajat: {emp.first_name} {emp.last_name} (email: {emp.email}, functie: {emp.job_title})")
            
        print("\n--- Timesheet ---")
        from app.models.timesheet import Timesheet  # Import aici pentru a evita importuri circulare
        result = await session.execute(select(Timesheet))
        timesheets = result.scalars().all()
        for ts in timesheets:
            print(f"Timesheet ID: {ts.id}, Employee ID: {ts.employee_id}, Data: {ts.work_date}, Ore lucrate: {ts.hours_worked}")
        print("\n--- Bonusuri ---")
        from app.models.bonus import Bonus  # Import aici pentru a evita importuri circulare
        result = await session.execute(select(Bonus))
        bonuses = result.scalars().all()
        for bonus in bonuses:
            print(f"Bonus ID: {bonus.id}, Employee ID: {bonus.employee_id}, Suma: {bonus.bonus_amount}, Bonus_Date: {bonus.bonus_date}")

        print("\n--- Vacante ---")
        from app.models.vacation import Vacation  # Import aici pentru a evita importuri circulare
        result = await session.execute(select(Vacation))
        vacations = result.scalars().all()
        for vac in vacations:
            print(f"Vacation ID: {vac.id}, Employee ID: {vac.employee_id}, Data inceput: {vac.start_date}, Data sfarsit: {vac.end_date}")
if __name__ == "__main__":
    asyncio.run(show_all())
