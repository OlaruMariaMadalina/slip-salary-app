import os
from decimal import Decimal
from datetime import date
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.employee_repository import get_employees_by_department_id
from app.db.repositories.vacation_repository import count_vacation_days_by_employee_id
from app.db.repositories.timesheet_repository import count_working_days_by_employee_id
from app.db.repositories.bonus_repository import sum_bonus_by_employee_id

async def extract_aggregated_employee_data(department_id: str, start_date: date, end_date: date, session: AsyncSession):
    employees = await get_employees_by_department_id(session, department_id)
    data = []
    
    for employee in employees:   
        working_days = await count_working_days_by_employee_id(session, employee.id, start_date, end_date)
        vacation_days = await count_vacation_days_by_employee_id(session, employee.id, start_date, end_date)
        bonus = await sum_bonus_by_employee_id(session, employee.id, start_date, end_date)
        salary = employee.base_salary + Decimal(str(bonus))
        
        data.append({
            "Employee First Name": employee.first_name,
            "Employee Last Name": employee.last_name, 
            "Employee Email": employee.email,
            "Employee Monthly Salary": employee.base_salary,
            "Employee Final Salary": salary,
            "Number of working days": working_days,
            "Number of vacation days taken": vacation_days,
            "Additional bonuses": bonus,
        })
    return data

def generate_excel(data_excel, file_name):
    df = pd.DataFrame(data_excel)
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'excel_reports')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.abspath(os.path.join(output_dir, file_name))
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return file_path
