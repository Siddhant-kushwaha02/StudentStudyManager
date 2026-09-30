from database import connect_db
from validation import require_text


def get_subjects():
    """Return every subject as (subject_id, subject_name)."""
    connection = connect_db()
    try:
        return connection.execute(
            "SELECT subject_id, subject_name FROM subjects ORDER BY subject_name"
        ).fetchall()
    finally:
        connection.close()


def create_subject(subject_name):
    """Add a subject, rejecting blank or case-insensitive duplicate names."""
    subject_name = require_text(subject_name, "Subject name")
    connection = connect_db()
    try:
        cursor = connection.execute(
            "SELECT 1 FROM subjects WHERE lower(subject_name) = lower(?)",
            (subject_name,),
        )
        if cursor.fetchone():
            raise ValueError("That subject already exists.")
        cursor = connection.execute(
            "INSERT INTO subjects (subject_name) VALUES (?)", (subject_name,)
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def add_subject():
    print("\n===== ADD SUBJECT =====")

    subject_name = input("Enter subject name: ")

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO subjects (subject_name) VALUES (?)",
        (subject_name,)
    )

    connection.commit()
    connection.close()

    print("\nSubject added successfully!")


def view_subjects():
    print("\n===== SUBJECTS =====")

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM subjects")

    subjects = cursor.fetchall()

    connection.close()

    if not subjects:
        print("No subjects found.")
        return

    for subject in subjects:
        print("ID:", subject[0], "| Subject:", subject[1])

def delete_subject():
    print("\n===== DELETE SUBJECT =====")

    subject_id = input("Enter subject ID: ")

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM subjects WHERE subject_id = ?",
        (subject_id,)
    )

    connection.commit()
    connection.close()

    print("\nSubject deleted successfully!")        