
from datetime import date

from sqlalchemy import Index, text
from sqlmodel import SQLModel, Field


class Booking(SQLModel, table=True):
    __tablename__ = "booking"

    __table_args__ = (
        Index(
            "uq_active_train_date_seat",
            "train_id",
            "journey_date",
            "seat_number",
            unique=True,
            sqlite_where=text("status = 'confirmed'"),
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    pnr: str = Field(unique=True, index=True, max_length=10)
    passenger_id: int = Field(foreign_key="user.id", index=True)
    train_id: int = Field(foreign_key="train.id", index=True)
    journey_date: date = Field(index=True)
    seat_number: int = Field(gt=0)
    status: str = Field(default="confirmed", max_length=20)
