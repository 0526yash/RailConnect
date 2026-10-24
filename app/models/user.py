
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    role: str = Field(default="passenger", max_length=20)
    is_active: bool = Field(default=True)
