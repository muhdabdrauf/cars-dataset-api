from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List


class CarBase(BaseModel):
    model_id: int = Field(..., gt=0, description="Enter valid Model ID")
    color_id: int = Field(..., gt=0, description="Enter valid Color ID")
    purchased_date: date = Field(..., description="Enter valid purchased date")
    @field_validator("purchased_date")
    def validate_date(cls, v):
        if v > date.today():
            raise ValueError("purchased_date cannot be in the future")
        return v

class CarCreate(CarBase):
    car_id: int


class CarResponse(CarBase):
    car_id: int = Field(..., gt=0, description="Enter valid Car ID")

    class Config:
        orm_mode = True

class PaginatedCarResponse(BaseModel):
    items: List[CarResponse]
    page: int
    page_size: int
    total: int
