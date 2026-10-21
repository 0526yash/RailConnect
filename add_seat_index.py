import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / "railconnect.db"

with sqlite3.connect(db_path) as connection:
    connection.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_active_train_date_seat
        ON booking (train_id, journey_date, seat_number)
        WHERE status = 'confirmed'
    """)

    indexes = connection.execute(
        "PRAGMA index_list(booking)"
    ).fetchall()

    print("Indexes:", indexes)
