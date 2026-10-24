
from datetime import date

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Station, Train, TrainAvailability


def search_trains(
    source: str,
    destination: str,
    journey_date: date,
    session: Session,
):
    source_code = source.strip().upper()
    destination_code = destination.strip().upper()

    source_station = session.exec(
        select(Station).where(Station.code == source_code)
    ).first()

    destination_station = session.exec(
        select(Station).where(Station.code == destination_code)
    ).first()

    if source_station is None or destination_station is None:
        raise HTTPException(
            status_code=404,
            detail="Source or destination station not found",
        )

    if source_station.id == destination_station.id:
        raise HTTPException(
            status_code=400,
            detail="Source and destination must be different",
        )

    if journey_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Journey date cannot be in the past",
        )

    trains = session.exec(
        select(Train).where(
            Train.source_station_id == source_station.id,
            Train.destination_station_id == destination_station.id,
            Train.is_active == True,
        )
    ).all()

    available_trains = []

    for train in trains:
        availability = session.exec(
            select(TrainAvailability).where(
                TrainAvailability.train_id == train.id,
                TrainAvailability.journey_date == journey_date,
            )
        ).first()

        available_trains.append({
            "id": train.id,
            "train_number": train.train_number,
            "name": train.name,
            "departure_time": train.departure_time,
            "arrival_time": train.arrival_time,
            "fare": train.fare,
            "journey_date": journey_date,
            "available_seats": (
                availability.available_seats
                if availability is not None
                else 0
            ),
            "availability_created": availability is not None,
        })

    return {
        "source": source_station.name,
        "destination": destination_station.name,
        "journey_date": journey_date,
        "total_trains": len(available_trains),
        "trains": available_trains,
    }
