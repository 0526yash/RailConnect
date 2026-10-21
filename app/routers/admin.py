
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.database import get_session
from datetime import date
from app.models import Station, Train, User, TrainAvailability
from app.routers.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )
    return current_user


class StationCreate(BaseModel):
    code: str = Field(min_length=2, max_length=10)
    name: str = Field(min_length=2, max_length=100)
    city: str = Field(min_length=2, max_length=100)

class TrainCreate(BaseModel):
    train_number: str = Field(min_length=2, max_length=10)
    name: str = Field(min_length=2, max_length=100)

    source_station_id: int = Field(gt=0)
    destination_station_id: int = Field(gt=0)

    departure_time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")
    arrival_time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")

    fare: int = Field(gt=0)
    total_seats: int = Field(gt=0)

@router.post("/stations", status_code=status.HTTP_201_CREATED)
def create_station(
    data: StationCreate,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin),
):
    code = data.code.strip().upper()

    existing = session.exec(
        select(Station).where(Station.code == code)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Station code already exists",
        )

    station = Station(
        code=code,
        name=data.name.strip(),
        city=data.city.strip(),
    )

    session.add(station)

    try:
        session.commit()
        session.refresh(station)
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not create station",
        )

    return {
        "message": "Station created successfully",
        "station": {
            "id": station.id,
            "code": station.code,
            "name": station.name,
            "city": station.city,
            "is_active": station.is_active,
        },
    }

@router.post("/trains", status_code=status.HTTP_201_CREATED)
def create_train(
    data: TrainCreate,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin),
):
    train_number = data.train_number.strip().upper()

    # Check duplicate train number
    existing = session.exec(
        select(Train).where(Train.train_number == train_number)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Train number already exists",
        )

    # Check source station
    source = session.get(Station, data.source_station_id)
    if source is None or not source.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source station not found or inactive",
        )

    # Check destination station
    destination = session.get(Station, data.destination_station_id)
    if destination is None or not destination.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination station not found or inactive",
        )

    if source.id == destination.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source and destination must be different",
        )

    train = Train(
        train_number=train_number,
        name=data.name.strip(),
        source_station_id=data.source_station_id,
        destination_station_id=data.destination_station_id,
        departure_time=data.departure_time,
        arrival_time=data.arrival_time,
        fare=data.fare,
        total_seats=data.total_seats,
        available_seats=data.total_seats,
    )

    session.add(train)

    try:
        session.commit()
        session.refresh(train)
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not create train; check for duplicate train number",
        )

    return {
        "message": "Train created successfully",
        "train": {
            "id": train.id,
            "train_number": train.train_number,
            "name": train.name,
            "source_station_id": train.source_station_id,
            "destination_station_id": train.destination_station_id,
            "departure_time": train.departure_time,
            "arrival_time": train.arrival_time,
            "fare": train.fare,
            "total_seats": train.total_seats,
            "available_seats": train.available_seats,
        },
    }

class AvailabilityCreate(BaseModel):
    train_id: int = Field(gt=0)
    journey_date: date


@router.post(
    "/availability",
    status_code=status.HTTP_201_CREATED,
)
def create_train_availability(
    data: AvailabilityCreate,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin),
):
    if data.journey_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Journey date cannot be in the past",
        )

    train = session.get(Train, data.train_id)

    if train is None or not train.is_active:
        raise HTTPException(
            status_code=404,
            detail="Train not found or inactive",
        )

    existing = session.exec(
        select(TrainAvailability).where(
            TrainAvailability.train_id == data.train_id,
            TrainAvailability.journey_date == data.journey_date,
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Availability already exists for this date",
        )

    availability = TrainAvailability(
        train_id=train.id,
        journey_date=data.journey_date,
        available_seats=train.total_seats,
    )

    session.add(availability)

    try:
        session.commit()
        session.refresh(availability)
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not create availability",
        )

    return {
        "message": "Date-wise availability created",
        "train_id": availability.train_id,
        "journey_date": availability.journey_date,
        "available_seats": availability.available_seats,
    }


@router.get("/availability")
def get_train_availability(
    train_id: int,
    journey_date: date,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin),
):
    availability = session.exec(
        select(TrainAvailability).where(
            TrainAvailability.train_id == train_id,
            TrainAvailability.journey_date == journey_date,
        )
    ).first()

    if availability is None:
        raise HTTPException(
            status_code=404,
            detail="Availability not found",
        )

    return {
        "train_id": availability.train_id,
        "journey_date": availability.journey_date,
        "available_seats": availability.available_seats,
    }
