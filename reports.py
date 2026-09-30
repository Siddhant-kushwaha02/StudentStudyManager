from database import connect_db


def get_progress(user_id):
    """Return progress counts and completion percentage for one student."""
    connection = connect_db()
    try:
        total_tasks = connection.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_id,)
        ).fetchone()[0]
        completed_tasks = connection.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'Completed'",
            (user_id,),
        ).fetchone()[0]
    finally:
        connection.close()

    pending_tasks = total_tasks - completed_tasks
    percentage = (completed_tasks / total_tasks * 100) if total_tasks else 0
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_percentage": round(percentage, 2),
    }


def show_progress(user_id):
    progress = get_progress(user_id)

    print("\n===== MY PROGRESS =====")
    print("Total Tasks     :", progress["total_tasks"])
    print("Completed Tasks :", progress["completed_tasks"])
    print("Pending Tasks   :", progress["pending_tasks"])
    print("Completion      :", progress["completion_percentage"], "%")