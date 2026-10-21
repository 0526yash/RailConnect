import getpass
from sqlmodel import Session, select

from app.database import engine
from app.models import User
from app.routers.auth import hash_password


def main():
    email = input("Enter admin email: ").strip().lower()

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if user is None:
            print("No account found with this email.")
            return

        if user.role != "admin":
            print("This account is not an admin.")
            return

        password = getpass.getpass("Enter new password (12-72 characters): ")

        if len(password) < 12 or len(password) > 72:
            print("Password must be 12-72 characters.")
            return

        confirm = getpass.getpass("Confirm new password: ")

        if password != confirm:
            print("Passwords do not match.")
            return

        user.hashed_password = hash_password(password)
        session.add(user)
        session.commit()

        print("Admin password reset successfully!")


if __name__ == "__main__":
    main()