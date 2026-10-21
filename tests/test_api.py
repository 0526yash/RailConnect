
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models import Station, Train


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        source = Station(
            name="New Delhi",
            code="NDLS",
            city="New Delhi",
        )

        destination = Station(
            name="Kanpur Central",
            code="CNB",
            city="Kanpur",
        )

        session.add(source)
        session.add(destination)
        session.commit()

        session.refresh(source)
        session.refresh(destination)

        train = Train(
            train_number="RC101",
            name="New Delhi Kanpur Express",
            source_station_id=source.id,
            destination_station_id=destination.id,
            departure_time="08:00",
            arrival_time="13:00",
            fare=500,
            total_seats=100,
            available_seats=100,
            is_active=True,
        )

        session.add(train)
        session.commit()

    yield engine
    engine.dispose()


@pytest.fixture
def client(test_engine):
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    test_client = TestClient(app)

    try:
        yield test_client
    finally:
        test_client.close()
        app.dependency_overrides.clear()


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to RailConnect API!",
        "status": "running",
    }


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_api_documentation_available(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "RailSync API"


def test_train_search_success(client):
    journey_date = (date.today() + timedelta(days=1)).isoformat()

    response = client.get(
        "/trains/search",
        params={
            "source": "NDLS",
            "destination": "CNB",
            "journey_date": journey_date,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["total_trains"] == 1
    assert data["trains"][0]["train_number"] == "RC101"
    assert data["trains"][0]["available_seats"] == 0


def test_train_search_normalizes_station_codes(client):
    journey_date = (date.today() + timedelta(days=1)).isoformat()

    response = client.get(
        "/trains/search",
        params={
            "source": " ndls ",
            "destination": " cnb ",
            "journey_date": journey_date,
        },
    )

    assert response.status_code == 200
    assert response.json()["total_trains"] == 1


def test_train_search_unknown_station(client):
    journey_date = (date.today() + timedelta(days=1)).isoformat()

    response = client.get(
        "/trains/search",
        params={
            "source": "UNKNOWN",
            "destination": "CNB",
            "journey_date": journey_date,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Source or destination station not found"
    )


def test_train_search_same_station(client):
    journey_date = (date.today() + timedelta(days=1)).isoformat()

    response = client.get(
        "/trains/search",
        params={
            "source": "NDLS",
            "destination": "NDLS",
            "journey_date": journey_date,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Source and destination must be different"
    )


def test_train_search_past_date(client):
    journey_date = (date.today() - timedelta(days=1)).isoformat()

    response = client.get(
        "/trains/search",
        params={
            "source": "NDLS",
            "destination": "CNB",
            "journey_date": journey_date,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Journey date cannot be in the past"
    )