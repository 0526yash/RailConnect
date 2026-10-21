from datetime import date
from sqlalchemy import Index, text
from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    role: str = Field(default="passenger", max_length=20)
    is_active: bool = Field(default=True)


class Station(SQLModel, table=True):
    __tablename__ = "station"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(index=True, max_length=100)
    city: str = Field(max_length=100)
    is_active: bool = Field(default=True)


class Train(SQLModel, table=True):
    __tablename__ = "train"

    id: int | None = Field(default=None, primary_key=True)
    train_number: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(index=True, max_length=100)

    source_station_id: int = Field(foreign_key="station.id")
    destination_station_id: int = Field(foreign_key="station.id")

    departure_time: str = Field(max_length=5)
    arrival_time: str = Field(max_length=5)

    # Fare is stored in whole rupees for this fictional project.
    fare: int = Field(gt=0)

    total_seats: int = Field(gt=0)
    available_seats: int = Field(ge=0)

    is_active: bool = Field(default=True)


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
