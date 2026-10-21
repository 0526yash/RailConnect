# RailSync — Mini Railway Booking Platform

RailSync is a railway ticket-booking backend built with **Python, FastAPI, and SQLModel**. It provides REST APIs for passenger authentication, train search, seat availability, ticket booking, and cancellation.

## Features

- **Authentication:** Token-based passenger authentication.
- **Train Search:** Search for trains by source, destination, and journey date.
- **Ticket Booking:** Create bookings with a generated PNR.
- **Seat Availability:** Track available seats for each train and journey date.
- **Booking Validation:** Validate journey dates and seat numbers.
- **Duplicate Booking Prevention:** Prevent duplicate confirmed bookings for the same seat, train, and journey date.
- **Cancellation:** Cancel confirmed tickets and restore seat availability.
- **Passenger Data Isolation:** Restrict passengers to their own booking records.
- **Admin Authorization:** Protect administrator-only operations.
- **Interactive API Documentation:** Explore endpoints using Swagger UI and ReDoc.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| SQLModel | Database models and ORM |
| SQLAlchemy | Database interaction |
| SQLite | Database |
| Uvicorn | ASGI server |
| Swagger UI / ReDoc | API documentation |

## Project Structure

```text
RailSync/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── admin.py
│       ├── trains.py
│       └── bookings.py
├── tests/
│   └── test_api.py
├── screenshots/
├── .gitignore
├── requirements.txt
├── README.md
├── create_admin.py
├── reset_admin_password.py
├── add_seat_index.py
└── fix_booking_constraint.py
```

*Database files and the virtual environment should remain local and should not be committed.*

## Getting Started

### Prerequisites

- Python installed
- Git installed
- A terminal such as PowerShell

### 1. Clone the repository

After renaming the GitHub repository to `RailSync`, use:

```bash
git clone https://github.com/0526yash/RailSync.git
cd RailSync
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this in the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

**Command Prompt:**

```bat
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the application

From the project root, run:

```bash
python -m uvicorn app.main:app --reload
```

### 6. Open the API documentation

Once the server is running:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Main API Areas

| Area | Purpose |
|---|---|
| Authentication | Passenger login and access tokens |
| Trains | Train search and availability |
| Bookings | Create, view, and cancel bookings |
| Admin | Administrator-protected operations |

For exact endpoints, request parameters, and schemas, start the application and visit Swagger UI at `/docs`.

## Validation and Security

The current implementation includes:

- Past journey-date validation.
- Seat-number range validation.
- Duplicate confirmed-seat booking prevention.
- Cancellation status checks.
- Passenger-specific booking access.
- Administrator authorization checks.

These are application-level safeguards. Further security review and automated testing are recommended before production use.

## Testing

Automated API tests are available in `tests/test_api.py`.

Run them using:

```bash
python -m pytest tests/ -v
```

The current test suite contains eight tests covering:

- Home and health endpoints.
- API documentation availability.
- Successful train search.
- Station-code normalization.
- Unknown station handling.
- Same-station validation.
- Past journey-date validation.

Additional regression tests can be added as the project grows.

## Future Improvements

- Expand automated test coverage for authentication and bookings.
- Railway timetable and route management.
- Booking history and PNR lookup.
- A React frontend for passengers and administrators.
- Deployment with a production-ready database.
- Production logging, monitoring, and security hardening.

## Repository

GitHub: https://github.com/0526yash/RailConnect

*Update the repository URL above after the GitHub rename is complete.*

---

**RailSync — Smarter Journeys. Seamless Connections.**
