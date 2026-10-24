
from datetime import date

from sqlmodel import Session

from app.services.train_service import search_trains


def search_trains_controller(
    source: str,
    destination: str,
    journey_date: date,
    session: Session,
):
    return search_trains(
        source=source,
        destination=destination,
        journey_date=journey_date,
        session=session,
    )
