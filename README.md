
# Slip Salary App

Slip Salary App is a web application for managing employee payroll, timesheets, bonuses, vacations, and generating salary slips in Excel and PDF formats. It provides both a FastAPI backend and a Streamlit frontend for managers to register, log in, and perform payroll operations for their department.

## Features

- **User Authentication:** Register and login for department managers.
- **Employee Management:** View and manage employees by department.
- **Timesheets & Vacations:** Track working days and vacation days.
- **Bonuses:** Add and view employee bonuses.
- **Payroll Generation:** Generate aggregated Excel reports and individual PDF payslips.
- **Email Sending:** Send reports and payslips via email to employees and managers.
- **Role-based Access:** Only managers can register and access payroll features.

## Technologies

- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL
- **Frontend:** Streamlit
- **PDF/Excel:** ReportLab, PyPDF2, Pandas, XlsxWriter
- **Email:** SMTP

## Project Structure

```
slip-salary-app/
├── app/
│   ├── config.py
│   ├── db/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── frontend/
├── tests/
├── main.py
├── requirements.txt
├── docker-compose.yaml
├── README.md
```

## Installation

1. **Clone the repository:**
	git clone https://github.com/OlaruMariaMadalina/slip-salary-app.git
	cd slip-salary-app

2. **Install dependencies:**
	python -m venv venv
	venv\Scripts\activate
	pip install -r requirements.txt

3. **Start PostgreSQL (recommended via Docker):**
	docker-compose up -d

## Running the Backend (FastAPI)

uvicorn app.main:app --reload

The API will be available at [http://localhost:8000](http://localhost:8000).

## Running the Frontend (Streamlit)
streamlit run app/frontend/streamlit.py

The dashboard will be available at [http://localhost:8501](http://localhost:8501).

## Database Migration (Alembic)

1. **Create a new migration:**
	alembic revision --autogenerate -m "Migration message"

2. **Apply migrations:**
	alembic upgrade head
