import asyncio
from calendar import monthrange
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import select

from app.db.engine import SessionLocal
from app.models.bonus import Bonus
from app.models.department import Department
from app.models.employee import Employee
from app.models.timesheet import Timesheet
from app.models.vacation import Vacation

async def seed():
    from sqlalchemy import text
    async with SessionLocal() as session:

        # Delete from user_accounts first to avoid FK violation
        await session.execute(text('DELETE FROM paychecks'))
        await session.execute(text('DELETE FROM bonuses'))
        await session.execute(text('DELETE FROM vacations'))
        await session.execute(text('DELETE FROM timesheets'))
        await session.execute(text('DELETE FROM user_accounts'))
        await session.execute(text('DELETE FROM employees'))
        await session.execute(text('DELETE FROM departments'))
        await session.commit()

        data_dept = Department(department_name="Data", department_description="Data Department")
        dev_dept = Department(department_name="Development", department_description="Development Department")
        session.add_all([data_dept, dev_dept])
        await session.commit()
        await session.refresh(data_dept)
        await session.refresh(dev_dept)

        dev_manager = Employee(
            first_name="Maria",
            last_name="Olaru",
            personal_identification_number="2990202022222",
            email="mariamadalinaolaru26@gmail.com",
            job_title="Dev Manager",
            hire_date=date(2017, 2, 2),
            base_salary=Decimal("13000.00"),
            department_id=dev_dept.id,
        )
        data_manager = Employee(
            first_name="Andrei",
            last_name="Manager",
            personal_identification_number="1990101011111",
            email="andrei.manager@datacorp.com",
            job_title="Data Manager",
            hire_date=date(2018, 1, 1),
            base_salary=Decimal("12000.00"),
            department_id=data_dept.id,
        )

        session.add_all([data_manager, dev_manager])
        await session.commit()
        await session.refresh(data_manager)
        await session.refresh(dev_manager)


        data_dept.manager_id = data_manager.id
        dev_dept.manager_id = dev_manager.id
        await session.commit()


        employees_data = [
            Employee(
                first_name="Ana",
                last_name="Popescu",
                personal_identification_number="1980101011111",
                email="ana.popescu@datacorp.com",
                job_title="Data Analyst",
                hire_date=date(2020, 1, 10),
                base_salary=Decimal("7000.00"),
                department_id=data_dept.id,
            ),
            Employee(
                first_name="Mihai",
                last_name="Ionescu",
                personal_identification_number="1980202022222",
                email="mihai.ionescu@datacorp.com",
                job_title="Data Engineer",
                hire_date=date(2021, 3, 15),
                base_salary=Decimal("8000.00"),
                department_id=data_dept.id,
            ),
            Employee(
                first_name="Elena",
                last_name="Georgescu",
                personal_identification_number="2980303033333",
                email="elena.georgescu@datacorp.com",
                job_title="Data Scientist",
                hire_date=date(2022, 5, 20),
                base_salary=Decimal("9000.00"),
                department_id=data_dept.id,
            ),
        ]


        employees_dev = [
            Employee(
                first_name="Rodica Elena",
                last_name="Rosca",
                personal_identification_number="1111111111111",
                email="olarumaria96@yahoo.ro",
                job_title="Python Developer",
                hire_date=date(2019, 2, 1),
                base_salary=Decimal("8500.00"),
                department_id=dev_dept.id,
            ),
            Employee(
                first_name="Ana",
                last_name="Ciobanu",
                personal_identification_number="2222222222222",
                email="viorelonica95@gmail.com",
                job_title="Python Developer",
                hire_date=date(2020, 6, 10),
                base_salary=Decimal("7800.00"),
                department_id=dev_dept.id,
            ),
            Employee(
                first_name="Sergiu",
                last_name="Ungureanu",
                personal_identification_number="3333333333333",
                email="viorel.onica@yahoo.com",
                job_title="Python Developer",
                hire_date=date(2021, 8, 25),
                base_salary=Decimal("9500.00"),
                department_id=dev_dept.id,
            ),
        ]
        session.add_all(employees_data + employees_dev + [data_manager, dev_manager])
        await session.flush()
        # Set the month and year for which to generate timesheets
        year = 2025
        month = 11  

        num_days = monthrange(year, month)[1]
        
        result = await session.execute(select(Employee))
        all_employees = result.scalars().all()

        timesheets = []
        for employee in all_employees:
            for day in range(1, num_days + 1):
                work_date = date(year, month, day)
                if work_date.weekday() < 5: 
                    timesheet = Timesheet(
                        employee_id=employee.id,
                        work_date=work_date,
                        hours_worked=8
                    )
                    timesheets.append(timesheet)

        session.add_all(timesheets)
        await session.commit()
        
        # Adaugă un bonus pentru un angajat (de exemplu, pentru Ana Popescu)
        # Adaugă un bonus pentru Ana Popescu
        ana = await session.execute(select(Employee).where(Employee.email == "ana.popescu@datacorp.com"))
        ana_employee = ana.scalar_one_or_none()
        if ana_employee:
            bonus = Bonus(
            employee_id=ana_employee.id,
            bonus_amount=Decimal("1000.00"),
            bonus_date=datetime(year, month, 5)
            )
            session.add(bonus)
            await session.commit()

        # Adaugă zile de concediu (vacation) pentru Mihai Ionescu
        mihai = await session.execute(select(Employee).where(Employee.email == "mihai.ionescu@datacorp.com"))
        mihai_employee = mihai.scalar_one_or_none()
        if mihai_employee:
            vacation_days = [date(year, month, 5), date(year, month, 6)]
            for vac_day in vacation_days:
            # Adaugă concediul
                vacation = Vacation(
                    employee_id=mihai_employee.id,
                    start_date=vac_day,
                    end_date=vac_day,
                )
            session.add(vacation)
            # Șterge timesheet-ul pentru ziua de concediu
            await session.execute(
                select(Timesheet)
                .where(
                Timesheet.employee_id == mihai_employee.id,
                Timesheet.work_date == vac_day
                )
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(
                Timesheet.__table__.delete().where(
                Timesheet.employee_id == mihai_employee.id,
                Timesheet.work_date == vac_day
                )
            )
            await session.commit()
if __name__ == "__main__":
    asyncio.run(seed())