from datetime import date
import calendar

def get_month_start_end_dates(month: int, year: int):
    start_date = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)
    return start_date, end_date