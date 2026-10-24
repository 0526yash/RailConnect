
from datetime import date

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field


class TrainAvailability(SQLModel, table=True):
    __tablename__ = "train_availability"

    __table_args__ = (
        UniqueConstraint(
            "train_id",
            "journey_date",
            name="uq_train_availability_date",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    train_id: int = Field(foreign_key="train.id", index=True)
    journey_date: date = Field(index=True)
    available_seats: int = Field(ge=0)
