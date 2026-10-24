
from datetime import date

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.controllers.train_controller import search_trains_controller

router = APIRouter(prefix="/trains", tags=["Trains"])


@router.get("/search")
def search_trains_endpoint(
    source: str,
    destination: str,
    journey_date: date,
    session: Session = Depends(get_session),
):
    return search_trains_controller(
        source=source,
        destination=destination,
        journey_date=journey_date,
        session=session,
    )
