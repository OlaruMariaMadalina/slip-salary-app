from datetime import date
import calendar

def get_month_start_end_dates(month: int, year: int):
    """
    Calculate the first and last date of a given month and year.

    Args:
        month (int): The month (1-12).
        year (int): The year (e.g., 2025).

    Returns:
        tuple[date, date]: A tuple containing the start date and end date of the month.
    """
    start_date = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)
    return start_date, end_date