
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.bookings import router as bookings_router
from app.models import User, Station, Train, Booking, TrainAvailability
from app.database import create_db_and_tables
from app.routers.auth import router as auth_router
from app.routers.admin import router as admin_router
from app.routers.trains import router as trains_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="RailSync API",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(trains_router)
app.include_router(bookings_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to RailConnect API!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}