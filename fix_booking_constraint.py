
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "railconnect.db"


def main():
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = OFF")
        connection.execute("BEGIN")

        # Remove the old table-level seat uniqueness constraint.
        connection.execute("""
            CREATE TABLE booking_new (
                id INTEGER NOT NULL PRIMARY KEY,
                pnr VARCHAR(10) NOT NULL UNIQUE,
                passenger_id INTEGER NOT NULL,
                train_id INTEGER NOT NULL,
                journey_date DATE NOT NULL,
                seat_number INTEGER NOT NULL CHECK (seat_number > 0),
                status VARCHAR(20) NOT NULL DEFAULT 'confirmed',
                FOREIGN KEY(passenger_id) REFERENCES user(id),
                FOREIGN KEY(train_id) REFERENCES train(id)
            )
        """)

        # Preserve all existing bookings and their IDs.
        connection.execute("""
            INSERT INTO booking_new
                (id, pnr, passenger_id, train_id,
                 journey_date, seat_number, status)
            SELECT
                id, pnr, passenger_id, train_id,
                journey_date, seat_number, status
            FROM booking
        """)

        connection.execute("DROP TABLE booking")
        connection.execute(
            "ALTER TABLE booking_new RENAME TO booking"
        )

        # Restore the existing indexes.
        connection.execute("""
            CREATE INDEX ix_booking_journey_date
            ON booking(journey_date)
        """)
        connection.execute("""
            CREATE INDEX ix_booking_train_id
            ON booking(train_id)
        """)
        connection.execute("""
            CREATE INDEX ix_booking_passenger_id
            ON booking(passenger_id)
        """)
        connection.execute("""
            CREATE INDEX ix_booking_pnr
            ON booking(pnr)
        """)

        # Only one confirmed booking per train/date/seat.
        # Cancelled bookings do not block reuse of the seat.
        connection.execute("""
            CREATE UNIQUE INDEX uq_active_train_date_seat
            ON booking(train_id, journey_date, seat_number)
            WHERE status = 'confirmed'
        """)

        connection.commit()
        print("Migration successful. Booking history preserved.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
