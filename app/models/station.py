
from sqlmodel import SQLModel, Field


class Station(SQLModel, table=True):
    __tablename__ = "station"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(index=True, max_length=100)
    city: str = Field(max_length=100)
    is_active: bool = Field(default=True)
