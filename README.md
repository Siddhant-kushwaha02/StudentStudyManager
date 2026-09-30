# Student Study & Task Management System

## Project Overview

The Student Study & Task Management System is a small desktop application for students who want to keep study tasks in one place. It uses a Tkinter interface and stores information locally in SQLite.

## Problem Statement

Students may track assignments, tests, and study activities in different notebooks or apps. This can make it easy to forget due dates or lose track of completed work. This project provides a simple way to organize tasks by subject and review progress.

## Objectives

- Store tasks with a subject, due date, priority, and status.
- Let each student manage only their own tasks.
- Show a simple summary of completed and pending work.
- Practice Python modules, Tkinter, SQLite, validation, and testing.

## Target Users

The main users are students who want a basic personal study and task tracker.

## Features

- Student registration and login.
- Passwords stored as salted PBKDF2 hashes. Existing plain-text passwords are upgraded after a successful login.
- Add tasks and view them in a table with their subject names.
- Update, complete, delete, and refresh a student's own tasks.
- View and add subjects.
- View total, completed, pending, and percentage progress.
- Validate required fields, date formats, and priorities.

## Functional Modules

1. **User Management:** registration and login.
2. **Task Management:** add, list, update, complete, and delete tasks.
3. **Subject Management:** view and add subjects.
4. **Progress & Reports:** calculate per-student task progress.

## Technologies

- Python 3
- Tkinter and ttk
- SQLite (`sqlite3`)
- Python `unittest`
- Mermaid diagrams for design documentation

No third-party Python packages are required.

## Project Structure

```text
StudentStudyManager/
├── main.py                 # create database tables and start the application
├── gui.py                  # Tkinter login, dashboard, and feature windows
├── database.py             # SQLite connection and table setup
├── login.py                # user authentication
├── register.py             # student registration
├── password_utils.py       # password hashing and verification
├── task_manager.py         # task operations and ownership checks
├── subject_manager.py      # view and add subjects
├── reports.py              # calculate student progress
├── validation.py           # shared input validation
├── test_project.py         # isolated unittest coverage
├── database/
│   └── study_manager.db       # created automatically; ignored by Git
├── docs/
│   ├── diagrams.md            # Mermaid design diagrams
│   └── project_report.md      # report draft (PDF submitted separately)
├── screenshots/               # add actual screenshots here
├── README.md
└── statement.md
```

The SQLite database is created automatically when the program runs. It is excluded from Git because it can contain local account data.

## Database Description

The SQLite database is `database/study_manager.db`, created automatically when the application starts.

- **users:** `user_id`, `name`, `email`, `password`, `role`
- **subjects:** `subject_id`, `subject_name`
- **tasks:** `task_id`, `user_id`, `subject_id`, `task_name`, `due_date`, `priority`, `status`

Each task is associated with its owner and a subject. Task actions in the GUI always include the logged-in user's ID. Dates are stored as `YYYY-MM-DD` after validation.

## Installation / Setup

1. Install Python 3.10 or newer. Tkinter is usually included with the standard Python installation.
2. Open this project folder in VS Code or a terminal.
3. No package installation is needed.
4. The program creates the database tables automatically; the existing database file is preserved.

## How to Run

From the project directory, run:

```powershell
python main.py
```

Register an account, log in, and use the dashboard. Add at least one subject before adding a task.

## Testing

Run the tests from the project directory:

```powershell
python -m unittest -v test_project.py
```

The test suite uses a separate temporary database. It does not erase or modify the normal `database/study_manager.db` file.

## Screenshots

Add real screenshots after running the application:

- [Add Login Screenshot]
- [Add Dashboard Screenshot]
- [Add Add Task Screenshot]
- [Add My Tasks Screenshot]
- [Add Progress Screenshot]

Screenshots are optional for the repository. Add actual images when available; no screenshots are included yet.

## Future Enhancements

- Add a task search and filtering option.
- Add reminders for tasks due soon.
- Add editing or deletion for subjects with safeguards.
- Improve the interface layout and add exportable reports.
