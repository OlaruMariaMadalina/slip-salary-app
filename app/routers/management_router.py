import os
from fastapi import Depends, status, APIRouter, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_utils import decode_jwt
from app.db.repositories.department_repository import get_department_by_employee_id
from app.db.repositories.employee_repository import get_employees_by_department_id
from app.db.repositories.user_repository import get_user_by_user_id
from app.db.db_deps import get_session
from app.schemas.management import CreateAggregatedDataRequest
from app.utils.mail_utils import send_email_with_attachment
from app.utils.excel_utils import extract_aggregated_employee_data, generate_excel
from app.utils.pdf_utils import generate_pdf, extract_data_for_employee_paycheck
from app.utils.date_utils import get_month_start_end_dates
from app.db.repositories.paycheck_repository import (
    get_paycheck_by_employee_and_month,
    create_paycheck_for_employee,
)

router = APIRouter(prefix="/management", tags=["management"])

@router.post("/create-aggregated-employee-data", status_code=status.HTTP_200_OK)
async def create_aggregated_employee_data(
    data: CreateAggregatedDataRequest,
    session: AsyncSession = Depends(get_session),
    authorization: str = Header(..., alias="Authorization")
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    
    try:
        decoded_jwt = decode_jwt(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    user = await get_user_by_user_id(session, decoded_jwt.get("user_id"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    department = await get_department_by_employee_id(session, user.employee_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found for the manager")

    start_date, end_date = get_month_start_end_dates(data.month, data.year)
    extracted_data = await extract_aggregated_employee_data(department.id, start_date, end_date, session)
    file_name = f"{department.id}_{data.month}_{data.year}_aggregated_employee_data.xlsx"
    generate_excel(extracted_data, file_name)

    return {"msg": "Excel file generated and saved."}


@router.post("/send-aggregated-employee-data", status_code=status.HTTP_200_OK)
async def send_aggregated_employee_data(
    data: CreateAggregatedDataRequest,
    session: AsyncSession = Depends(get_session),
    authorization: str = Header(..., alias="Authorization")
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    
    try:
        decoded_jwt = decode_jwt(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    user = await get_user_by_user_id(session, decoded_jwt.get("user_id"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    department = await get_department_by_employee_id(session, user.employee_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found for the manager")
    
    file_path = f"app/excel_reports/{department.id}_{data.month}_{data.year}_aggregated_employee_data.xlsx"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Excel file not found. Please generate it first.")
    
    mail = send_email_with_attachment(
        recipient=user.username,
        subject="Aggregated Employee Data Report",
        body="Please find attached the aggregated employee data report.",
        filepath=file_path,
    )
    if not mail:
        raise HTTPException(status_code=404, detail="Some error occurred while sending email")

    return {"msg": "Aggregated employee data sent to the manager successfully"}


@router.post("/create-pdf-for-empoloyees", status_code=status.HTTP_200_OK)
async def create_pdf_for_employees(
    data: CreateAggregatedDataRequest,
    session: AsyncSession = Depends(get_session),
    authorization: str = Header(..., alias="Authorization")
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    
    try:
        decoded_jwt = decode_jwt(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    user = await get_user_by_user_id(session, decoded_jwt.get("user_id"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    department = await get_department_by_employee_id(session, user.employee_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found for the manager")
    
    employees = await get_employees_by_department_id(session, department.id)
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found in the manager's department")
    
    results = []
    start_date, end_date = get_month_start_end_dates(data.month, data.year)
    for employee in employees:
        extracted_data = await extract_data_for_employee_paycheck(employee.id, start_date, end_date, session)
        file_name = f"{employee.id}_{data.month}_to_{data.year}_paycheck_data.pdf"
        generate_pdf(extracted_data, file_name, employee.personal_identification_number)
        results.append({
            "employee_email": employee.email,
        })

    return {
        "msg": "PDF files generated and saved.",
        "results": results
    }


@router.post("/send-pdf-to-employees", status_code=status.HTTP_200_OK)
async def send_pdf_to_employees(
    data: CreateAggregatedDataRequest,
    session: AsyncSession = Depends(get_session),
    authorization: str = Header(..., alias="Authorization")
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    
    try:
        decoded_jwt = decode_jwt(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    user = await get_user_by_user_id(session, decoded_jwt.get("user_id"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    department = await get_department_by_employee_id(session, user.employee_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found for the manager")
    
    employees = await get_employees_by_department_id(session, department.id)
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found in the manager's department")
    
    results = []
    for employee in employees:
        paycheck = await get_paycheck_by_employee_and_month(
            session,
            employee.id,
            data.month,
            data.year
        )
        if paycheck:
            results.append({ "employee_email": employee.email, "paycheck_sent": False, "reason": "Paycheck already sent for employee" })
            continue
        
        file_path = f"app/paycheck_employees/{employee.id}_{data.month}_to_{data.year}_paycheck_data.pdf"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="PDF file not found. Please generate it first.")
        
        mail = send_email_with_attachment(
            recipient=employee.email,
            subject=f"Payslip for {data.month}/{data.year}",
            body=f"Attached to this email you will find the payslip for {data.month}/{data.year}.",
            filepath=file_path,
        )
        if not mail:
            raise HTTPException(status_code=404, detail="Some error occurred while sending email")
        print("Sending paycheck...")
        print(f"Paycheck for {employee.id} sent successfully.")
        print(f"data.month: {data.month}, data.year: {data.year}")

        await create_paycheck_for_employee(
            session,
            employee.id,
            data.month,
            data.year
        )
            
        results.append({
            "employee_email": employee.email,
            "paycheck_sent": True
        })

    return {
        "msg": "Aggregated employee data sent to the manager successfully",
        "results": results
    }
    
    
