
from sqlmodel import Session

from app.models import User
from app.schemas.booking import BookingCreate
from app.services.booking_service import (
    create_booking,
    get_my_bookings,
    cancel_booking,
)


def create_booking_controller(
    booking_data: BookingCreate,
    session: Session,
    current_user: User,
):
    return create_booking(
        booking_data=booking_data,
        session=session,
        current_user=current_user,
    )


def get_my_bookings_controller(
    session: Session,
    current_user: User,
):
    return get_my_bookings(
        session=session,
        current_user=current_user,
    )


def cancel_booking_controller(
    booking_id: int,
    session: Session,
    current_user: User,
):
    return cancel_booking(
        booking_id=booking_id,
        session=session,
        current_user=current_user,
    )
