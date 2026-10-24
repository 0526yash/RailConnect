
from datetime import date

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    train_id: int = Field(gt=0)
    journey_date: date
    seat_number: int = Field(gt=0)
