
from sqlmodel import SQLModel, Field


class Train(SQLModel, table=True):
    __tablename__ = "train"

    id: int | None = Field(default=None, primary_key=True)
    train_number: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(index=True, max_length=100)

    source_station_id: int = Field(foreign_key="station.id")
    destination_station_id: int = Field(foreign_key="station.id")

    departure_time: str = Field(max_length=5)
    arrival_time: str = Field(max_length=5)

    fare: int = Field(gt=0)
    total_seats: int = Field(gt=0)
    available_seats: int = Field(ge=0)
    is_active: bool = Field(default=True)
