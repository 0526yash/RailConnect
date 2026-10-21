from datetime import date
import secrets
import string

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.database import get_session
from app.models import Booking, Train, TrainAvailability, User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


class BookingCreate(BaseModel):
    train_id: int = Field(gt=0)
    journey_date: date
    seat_number: int = Field(gt=0)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    train = session.get(Train, booking_data.train_id)

    if train is None or not train.is_active:
        raise HTTPException(
            status_code=404,
            detail="Train not found or inactive",
        )

    if booking_data.journey_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Journey date cannot be in the past",
        )

    if booking_data.seat_number > train.total_seats:
        raise HTTPException(
            status_code=400,
            detail="Invalid seat number",
        )

    availability = session.exec(
        select(TrainAvailability).where(
            TrainAvailability.train_id == booking_data.train_id,
            TrainAvailability.journey_date == booking_data.journey_date,
        )
    ).first()

    if availability is None:
        availability = TrainAvailability(
        train_id=booking_data.train_id,
        journey_date=booking_data.journey_date,
        available_seats=train.total_seats,
    )
    session.add(availability)
    session.flush()


    result = session.exec(
        update(TrainAvailability)
        .where(
            TrainAvailability.id == availability.id,
            TrainAvailability.available_seats > 0,
        )
        .values(
            available_seats=TrainAvailability.available_seats - 1
        )
    )

    if result.rowcount == 0:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="No seats available for this date",
        )

    booking = Booking(
        pnr="RC" + "".join(
            secrets.choice(string.digits) for _ in range(8)
        ),
        passenger_id=current_user.id,
        train_id=booking_data.train_id,
        journey_date=booking_data.journey_date,
        seat_number=booking_data.seat_number,
        status="confirmed",
    )

    session.add(booking)

    try:
        session.commit()
        session.refresh(booking)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="This seat is already booked for this train and date",
        )

    return {
        "message": "Booking successful",
        "booking": {
            "id": booking.id,
            "pnr": booking.pnr,
            "train_id": booking.train_id,
            "journey_date": booking.journey_date,
            "seat_number": booking.seat_number,
            "status": booking.status,
        },
    }


@router.get("/my")
def get_my_bookings(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    bookings = session.exec(
        select(Booking)
        .where(Booking.passenger_id == current_user.id)
        .order_by(Booking.id.desc())
    ).all()

    return {
        "total_bookings": len(bookings),
        "bookings": [
            {
                "id": booking.id,
                "pnr": booking.pnr,
                "train_id": booking.train_id,
                "journey_date": booking.journey_date,
                "seat_number": booking.seat_number,
                "status": booking.status,
            }
            for booking in bookings
        ],
    }
@router.patch("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        booking = session.exec(
            select(Booking).where(
                Booking.id == booking_id,
                Booking.passenger_id == current_user.id,
            )
        ).first()

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found",
            )

        if booking.status != "confirmed":
            raise HTTPException(
                status_code=400,
                detail="Booking is already cancelled",
            )

        train = session.get(Train, booking.train_id)

        if train is None:
            raise HTTPException(
                status_code=404,
                detail="Train not found",
            )

        availability = session.exec(
            select(TrainAvailability).where(
                TrainAvailability.train_id == booking.train_id,
                TrainAvailability.journey_date == booking.journey_date,
            )
        ).first()

        if availability is None:
            raise HTTPException(
                status_code=404,
                detail="Availability record not found",
            )

        # Change the booking only if it is still confirmed.
        result = session.exec(
            update(Booking)
            .where(
                Booking.id == booking_id,
                Booking.passenger_id == current_user.id,
                Booking.status == "confirmed",
            )
            .values(status="cancelled")
        )

        if result.rowcount != 1:
            raise HTTPException(
                status_code=409,
                detail="Booking was already cancelled or changed",
            )

        # Restore one seat, without exceeding train capacity.
        seat_result = session.exec(
            update(TrainAvailability)
            .where(
                TrainAvailability.id == availability.id,
                TrainAvailability.available_seats < train.total_seats,
            )
            .values(
                available_seats=TrainAvailability.available_seats + 1
            )
        )

        if seat_result.rowcount != 1:
            raise HTTPException(
                status_code=409,
                detail="Seat availability is already at capacity or cannot be restored",
            )

        session.commit()

        return {
            "message": "Booking cancelled successfully",
            "booking_id": booking_id,
            "pnr": booking.pnr,
            "status": "cancelled",
        }

    except HTTPException:
        session.rollback()
        raise

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Cancellation failed; changes rolled back",
        )
