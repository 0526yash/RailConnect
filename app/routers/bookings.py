from datetime import date
import secrets
import string

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.booking import BookingCreate
from sqlmodel import Session, select
from app.controllers.booking_controller import (
    create_booking_controller,
    get_my_bookings_controller,
    cancel_booking_controller,
)

from app.database import get_session
from app.models import Booking, Train, TrainAvailability, User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_booking_endpoint(
    booking_data: BookingCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_booking_controller(
        booking_data=booking_data,
        session=session,
        current_user=current_user,
    )
    
@router.get("/my")
def get_my_bookings_endpoint(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_my_bookings_controller(
        session=session,
        current_user=current_user,
    )

@router.patch("/{booking_id}/cancel")
def cancel_booking_endpoint(
    booking_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return cancel_booking_controller(
        booking_id=booking_id,
        session=session,
        current_user=current_user,
    )
