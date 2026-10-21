
import getpass

from sqlmodel import Session, select

from app.database import create_db_and_tables, engine
from app.models import User
from app.routers.auth import hash_password


def main():
    create_db_and_tables()

    email = input("Admin email: ").strip().lower()
    name = input("Admin name: ").strip()

    if not email or not name:
        print("Name and email are required.")
        return

    with Session(engine) as session:
        existing = session.exec(
            select(User).where(User.email == email)
        ).first()

        if existing:
            print(
                "This email already exists. "
                "No role changes were made."
            )
            return

        password = getpass.getpass("Admin password (min 12 chars): ")

        if len(password) < 12 or len(password) > 72:
            print("Password must be 12–72 characters.")
            return

        admin = User(
            name=name,
            email=email,
            hashed_password=hash_password(password),
            role="admin",
            is_active=True,
        )

        session.add(admin)
        session.commit()

        print("Admin account created successfully.")


if __name__ == "__main__":
    main()
