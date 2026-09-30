import sqlite3

from database import connect_db
from password_utils import hash_password
from validation import require_text


def create_user(name, email, password):
    """Register a student and return the new user ID."""
    name = require_text(name, "Name")
    email = require_text(email, "Email").lower()
    password = require_text(password, "Password")
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        raise ValueError("Enter a valid email address.")
    if len(password) < 6:
        raise ValueError("Password must contain at least 6 characters.")

    connection = connect_db()
    try:
        cursor = connection.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, 'student')
        """, (name, email, hash_password(password)))
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def register_user():
    print("\n===== STUDENT REGISTRATION =====")

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        create_user(name, email, password)
        print("\nRegistration successful!")
    except ValueError as error:
        print(f"\n{error}")
    except sqlite3.IntegrityError:
        print("\nThis email is already registered.")