from datetime import date
from pydantic import BaseModel, Field, validator

class CreateAggregatedDataRequest(BaseModel):
    """
    Schema for requests that require month and year input for aggregated employee data operations.

    Attributes:
        month (int): The month for the operation (must be between 1 and 12).
        year (int): The year for the operation (must be >= 2025).
    """
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2025)
    
    @validator("month")
    def validate_month(cls, v):
        if not 1 <= v <= 12:
            raise ValueError("Month must be between 1 and 12")
        return v

    @validator("year")
    def validate_year(cls, v):
        if v < 2025:
            raise ValueError("Year must be greater than or equal to 2025")
        return v