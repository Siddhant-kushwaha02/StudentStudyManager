"""Unit tests use a temporary SQLite file and never touch the real database."""

import tempfile
import sqlite3
import unittest
from pathlib import Path
from unittest.mock import patch

import database
from login import authenticate_user
from register import create_user
from reports import get_progress
from subject_manager import create_subject
from task_manager import (
    create_task,
    delete_task_by_id,
    get_tasks,
    mark_task_completed,
    update_task_details,
)


class StudentStudyManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_override = patch.object(
            database, "DATABASE", Path(self.temp_dir.name) / "test_study_manager.db"
        )
        self.database_override.start()
        database.create_tables()
        self.user_id = create_user("Test Student", "student@example.com", "secret123")
        self.other_user_id = create_user("Other Student", "other@example.com", "secret123")
        self.subject_id = create_subject("Programming")

    def tearDown(self):
        self.database_override.stop()
        self.temp_dir.cleanup()

    def test_database_creation_and_registration(self):
        connection = database.connect_db()
        try:
            tables = {
                row[0] for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
        finally:
            connection.close()
        self.assertTrue({"users", "subjects", "tasks"}.issubset(tables))
        self.assertGreater(self.user_id, 0)

    def test_login_works_and_wrong_password_fails(self):
        self.assertEqual(
            authenticate_user("student@example.com", "secret123"),
            (self.user_id, "Test Student", "student"),
        )
        self.assertIsNone(authenticate_user("student@example.com", "incorrect"))

    def test_legacy_password_is_upgraded_on_login(self):
        connection = database.connect_db()
        connection.execute(
            "UPDATE users SET password = 'legacy123' WHERE user_id = ?", (self.user_id,)
        )
        connection.commit()
        connection.close()
        self.assertIsNotNone(authenticate_user("student@example.com", "legacy123"))
        connection = database.connect_db()
        stored = connection.execute(
            "SELECT password FROM users WHERE user_id = ?", (self.user_id,)
        ).fetchone()[0]
        connection.close()
        self.assertTrue(stored.startswith("pbkdf2_sha256$"))

    def test_task_crud_is_limited_to_owner(self):
        create_task(self.user_id, self.subject_id, "Lab work", "30-09-2026", "high")
        task = get_tasks(self.user_id)[0]
        self.assertEqual(task[1:3], ("Lab work", "Programming"))
        self.assertEqual(task[3:], ("2026-09-30", "High", "Pending"))
        self.assertEqual(get_tasks(self.other_user_id), [])

        self.assertFalse(update_task_details(
            self.other_user_id, task[0], self.subject_id, "Other", "2026-10-01", "Low"
        ))
        self.assertTrue(update_task_details(
            self.user_id, task[0], self.subject_id, "Updated lab", "2026-10-01", "Low"
        ))
        self.assertTrue(mark_task_completed(self.user_id, task[0]))
        self.assertEqual(get_progress(self.user_id), {
            "total_tasks": 1,
            "completed_tasks": 1,
            "pending_tasks": 0,
            "completion_percentage": 100.0,
        })
        self.assertTrue(delete_task_by_id(self.user_id, task[0]))
        self.assertEqual(get_tasks(self.user_id), [])

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "valid date"):
            create_task(self.user_id, self.subject_id, "Lab", "not-a-date", "High")
        with self.assertRaisesRegex(ValueError, "task first"):
            delete_task_by_id(self.user_id, "abc")
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            create_subject("  ")

    def test_duplicate_email_and_subject_are_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            create_user("Duplicate", "student@example.com", "secret123")
        with self.assertRaisesRegex(ValueError, "already exists"):
            create_subject("programming")

    def test_empty_progress_is_zero(self):
        self.assertEqual(get_progress(self.other_user_id), {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "completion_percentage": 0,
        })


if __name__ == "__main__":
    unittest.main()
