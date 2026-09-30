from database import connect_db
from password_utils import hash_password, verify_password


def authenticate_user(email, password):
    """Return (user_id, name, role) on success, otherwise None."""
    email = email.strip().lower()
    connection = connect_db()
    try:
        row = connection.execute("""
            SELECT user_id, name, role, password
            FROM users WHERE email = ?
        """, (email,)).fetchone()
        if not row:
            return None
        is_valid, is_hashed = verify_password(password, row[3])
        if not is_valid:
            return None
        if not is_hashed:
            connection.execute(
                "UPDATE users SET password = ? WHERE user_id = ?",
                (hash_password(password), row[0]),
            )
            connection.commit()
        return row[0], row[1], row[2]
    finally:
        connection.close()


def login_user():
    print("\n===== STUDENT LOGIN =====")

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user = authenticate_user(email, password)

    if user:
        print("\nLogin successful!")
        print("Welcome,", user[1])
        return user
    else:
        print("\nInvalid email or password.")
        return None