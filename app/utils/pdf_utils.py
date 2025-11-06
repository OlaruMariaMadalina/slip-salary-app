import os
from datetime import date
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.employee_repository import get_employee_by_id
from app.db.repositories.timesheet_repository import count_working_days_by_employee_id
from app.db.repositories.vacation_repository import count_vacation_days_by_employee_id
from app.db.repositories.bonus_repository import sum_bonus_by_employee_id

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter


def generate_pdf(data_list, file_name: str, password: str):
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'paycheck_employees')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.abspath(os.path.join(output_dir, file_name))
    temp_file_path = file_path + ".tmp"

    c = canvas.Canvas(temp_file_path, pagesize=letter)
    width, height = letter

    y = height - 100
    for item in data_list:
        for key, value in item.items():
            c.drawString(100, y, f"{key}: {value}")
            y -= 20
        y -= 10 

    c.save()

    reader = PdfReader(temp_file_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)

    with open(file_path, "wb") as f:
        writer.write(f)

    os.remove(temp_file_path)
    return file_path

async def extract_data_for_employee_paycheck(employee_id: int, start_date: date, end_date: date, session: AsyncSession):
    employee = await get_employee_by_id(session, employee_id)
    data = []
    
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
