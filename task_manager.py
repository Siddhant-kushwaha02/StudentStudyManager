from database import connect_db
from validation import normalize_due_date, require_text, validate_priority


def get_tasks(user_id):
    """Return a student's tasks with readable subject names."""
    connection = connect_db()
    try:
        return connection.execute("""
            SELECT tasks.task_id, tasks.task_name, subjects.subject_name,
                   tasks.due_date, tasks.priority, tasks.status
            FROM tasks
            LEFT JOIN subjects ON tasks.subject_id = subjects.subject_id
            WHERE tasks.user_id = ?
            ORDER BY tasks.due_date, tasks.task_id
        """, (user_id,)).fetchall()
    finally:
        connection.close()


def create_task(user_id, subject_id, task_name, due_date, priority):
    """Create a pending task after validating its user-entered fields."""
    task_name = require_text(task_name, "Task name")
    due_date = normalize_due_date(due_date)
    priority = validate_priority(priority)
    connection = connect_db()
    try:
        subject = connection.execute(
            "SELECT 1 FROM subjects WHERE subject_id = ?", (subject_id,)
        ).fetchone()
        if not subject:
            raise ValueError("Select a valid subject before adding a task.")
        connection.execute("""
            INSERT INTO tasks
                (user_id, subject_id, task_name, due_date, priority, status)
            VALUES (?, ?, ?, ?, ?, 'Pending')
        """, (user_id, subject_id, task_name, due_date, priority))
        connection.commit()
    finally:
        connection.close()


def update_task_details(user_id, task_id, subject_id, task_name, due_date, priority):
    """Update a task only when it belongs to the supplied student."""
    try:
        task_id = int(task_id)
    except (TypeError, ValueError) as error:
        raise ValueError("Select a valid task to update.") from error
    task_name = require_text(task_name, "Task name")
    due_date = normalize_due_date(due_date)
    priority = validate_priority(priority)
    connection = connect_db()
    try:
        cursor = connection.execute("""
            UPDATE tasks
            SET subject_id = ?, task_name = ?, due_date = ?, priority = ?
            WHERE task_id = ? AND user_id = ?
        """, (subject_id, task_name, due_date, priority, task_id, user_id))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def mark_task_completed(user_id, task_id):
    """Mark one of the supplied student's tasks completed."""
    return _change_task_status(user_id, task_id, "Completed")


def _change_task_status(user_id, task_id, status):
    try:
        task_id = int(task_id)
    except (TypeError, ValueError) as error:
        raise ValueError("Select a valid task first.") from error
    connection = connect_db()
    try:
        cursor = connection.execute(
            "UPDATE tasks SET status = ? WHERE task_id = ? AND user_id = ?",
            (status, task_id, user_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_task_by_id(user_id, task_id):
    """Delete one of the supplied student's tasks."""
    try:
        task_id = int(task_id)
    except (TypeError, ValueError) as error:
        raise ValueError("Select a valid task first.") from error
    connection = connect_db()
    try:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE task_id = ? AND user_id = ?",
            (task_id, user_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()

def select_subject():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT subject_id, subject_name FROM subjects")
    subjects = cursor.fetchall()

    connection.close()

    if not subjects:
        print("No subjects available.")
        return None

    print("\n===== SELECT SUBJECT =====")

    for i, subject in enumerate(subjects, start=1):
        print(i, ".", subject[1])

    choice = int(input("Enter subject number: "))

    if choice < 1 or choice > len(subjects):
        print("Invalid subject.")
        return None

    return subjects[choice - 1][0]

def add_task(user_id):
    print("\n===== ADD TASK =====")

    task_name = input("Enter task name: ")

    subject_id = select_subject()

    if subject_id is None:
        return

    due_date = input("Enter due date (DD-MM-YYYY): ")
    priority = input("Enter priority (Low/Medium/High): ")

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO tasks
    (user_id, subject_id, task_name, due_date, priority, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, subject_id, task_name, due_date, priority, "Pending"))

    connection.commit()
    connection.close()

    print("\nTask added successfully!")


def view_tasks(user_id):
    print("\n===== MY TASKS =====")

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT task_id, subject_id, task_name, due_date, priority, status
    FROM tasks
    WHERE user_id = ?
    """, (user_id,))

    tasks = cursor.fetchall()

    connection.close()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print("\nTask ID:", task[0])
        print("Subject ID:", task[1])
        print("Task:", task[2])
        print("Due Date:", task[3])
        print("Priority:", task[4])
        print("Status:", task[5])

def update_task(user_id):
    print("\n===== UPDATE TASK =====")

    task_id = input("Enter task ID: ")
    new_name = input("Enter new task name: ")
    new_date = input("Enter new due date: ")
    new_priority = input("Enter new priority: ")

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE tasks
    SET task_name = ?, due_date = ?, priority = ?
    WHERE task_id = ? AND user_id = ?
    """, (new_name, new_date, new_priority, task_id, user_id))

    connection.commit()
    connection.close()

    print("\nTask updated successfully!")    

def delete_task(user_id):
    print("\n===== DELETE TASK =====")

    task_id = input("Enter task ID: ")

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM tasks
    WHERE task_id = ? AND user_id = ?
    """, (task_id, user_id))

    connection.commit()
    connection.close()

    print("\nTask deleted successfully!")

def complete_task(user_id):
    print("\n===== COMPLETE TASK =====")

    task_id = input("Enter task ID: ")

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE tasks
    SET status = ?
    WHERE task_id = ? AND user_id = ?
    """, ("Completed", task_id, user_id))

    connection.commit()
    connection.close()

    print("\nTask marked as completed!")        