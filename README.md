# RailConnect — Mini Railway Booking Platform

RailConnect is a railway booking backend built with **FastAPI** and **SQLModel**. It provides APIs for train search, passenger authentication, ticket booking, and cancellation.

## Features

- Passenger authentication using access tokens
- Train search by source, destination, and journey date
- Railway ticket booking with PNR generation
- Seat availability tracking
- Duplicate confirmed-seat booking prevention
- Ticket cancellation and seat restoration
- Passenger-specific booking access
- Admin-protected operations
- Interactive API documentation through Swagger UI

## Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **ORM:** SQLModel / SQLAlchemy
- **Database:** SQLite
- **API documentation:** Swagger UI

## Project Structure

```text
Railconnect/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── routers/
│       ├── auth.py
│       ├── admin.py
│       ├── trains.py
│       └── bookings.py
├── .venv/
├── railconnect.db
└── README.md
```

## Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

Install the packages listed in your project's `requirements.txt`, if available:

```powershell
pip install -r requirements.txt
```

If no requirements file exists, install the dependencies used by the application.

### 3. Run the application

From the project root, run:

```powershell
python -m uvicorn app.main:app --reload
```

### 4. Open the API documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Main API Areas

| Area | Purpose |
|---|---|
| Authentication | Passenger login and access tokens |
| Trains | Train search and availability |
| Bookings | Create, view, and cancel bookings |
| Admin | Administrator-protected operations |

Refer to `/docs` for the exact routes, parameters, and request schemas exposed by the running application.

## Security and Validation

The implementation includes passenger-specific booking access, admin authorization, past-date validation, seat-number validation, duplicate confirmed-seat protection, and cancellation checks.

## Testing

Tests performed manually through the API include train search, invalid input handling, duplicate-seat rejection, cancellation, repeated cancellation, admin authorization, and cross-passenger cancellation protection.

## Notes

- Keep database files and secrets out of public repositories.
- Do not commit `.venv/`, access tokens, passwords, or private environment files.
- Confirm the database initialization and dependency instructions before sharing the project.
- Automated test coverage and production deployment hardening can be added later.

## Future Improvements

- Automated API tests using pytest
- Railway timetable and route management
- Booking history and improved PNR lookup
- Deployment with a production database
- Frontend integration
