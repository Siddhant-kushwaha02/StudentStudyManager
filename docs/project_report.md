# Student Study & Task Management System — Project Report Draft

## Cover Page

**Project title:** Student Study & Task Management System  
**Course:** VITyarthi — Build Your Own Project  
**Student name:** [Enter your name]  
**Registration number:** [Enter your registration number]  
**Programme:** B.Tech Computer Science and Engineering  
**Year:** First Year  
**Institution:** [Enter institution name]  
**Submission date:** [Enter date]

## 1. Introduction

Students handle assignments, tests, and personal study plans throughout a semester. This project is a small desktop application that helps a student keep tasks organized by subject, due date, priority, and completion status. The application is written in Python, uses Tkinter for its interface, and stores information in SQLite.

## 2. Problem Statement

Study tasks are often noted in different places, which makes it difficult to remember due dates and see what remains unfinished. A simple, local system is needed to record study tasks and provide a quick view of progress for each student account.

## 3. Objectives

- Build a beginner-friendly desktop application using Python.
- Store users, subjects, and tasks in a relational SQLite database.
- Allow students to add and manage their own tasks.
- Show a basic progress summary.
- Practice modular programming, input validation, and testing.

## 4. Functional Requirements

1. A student can register with a name, email, and password.
2. A student can log in to the application.
3. A student can view available subjects and add a subject.
4. A student can add tasks with a task name, subject, due date, and priority.
5. A student can see their tasks, update a task, mark it completed, or delete it.
6. The application displays total, completed, pending, and percentage progress for the logged-in student.
7. The application rejects missing fields and invalid dates and reports database problems with a useful message.

## 5. Non-functional Requirements

- **Usability:** The interface uses familiar forms, buttons, and a table.
- **Security:** SQL statements use parameters; passwords are salted and hashed; task operations are scoped to the logged-in user ID.
- **Reliability:** Database operations commit changes and close connections, while input errors are reported instead of crashing the interface.
- **Maintainability:** User management, task management, subjects, reports, validation, and database access are separated into Python modules.
- **Portability:** The project uses Python standard-library components and a local SQLite file.

## 6. System Architecture

The student interacts with a Tkinter GUI. The GUI calls modules for user registration and authentication, task operations, subject operations, and progress calculations. These modules use `database.py` to connect to the SQLite database. Password helper functions are in `password_utils.py`, and shared date/text checks are in `validation.py`.

See [diagrams.md](diagrams.md) for the architecture, workflow, use case, sequence, component, and ER diagrams.

## 7. Design Diagrams

The diagrams in [diagrams.md](diagrams.md) cover:

- System Architecture Diagram
- User Workflow Diagram
- Use Case Diagram
- Sequence Diagram
- Class/Component Diagram
- ER Diagram

The ER model has a one-to-many relationship from User to Task and from Subject to Task. A task belongs to one user and one subject.

## 8. Design Decisions and Rationale

- **Tkinter:** It is included with Python and is adequate for a small desktop GUI.
- **SQLite:** It stores the data in a local file and does not need a separate database server.
- **Separate modules:** Each module has a clear responsibility, making the project easier to understand and test.
- **Parameterized SQL:** User-provided values are passed as parameters rather than joined into SQL strings.
- **User-scoped task changes:** Updates, completion, and deletion use both task ID and logged-in user ID.
- **Password hashes:** New registrations store a PBKDF2 hash and salt. If an existing account has a legacy plain-text password, it is upgraded after a successful login so the existing account can still be used.
- **Date normalization:** Both `YYYY-MM-DD` and `DD-MM-YYYY` input are accepted and stored consistently as `YYYY-MM-DD`.

## 9. Implementation Details

The main launch file creates the database tables and starts the GUI. Registration and login use the `users` table. The subject manager provides a subject list for task forms. The task manager performs CRUD operations and filters task queries by user ID. The reports module calculates completion counts from the database. `validation.py` checks text, dates, and priority values. `password_utils.py` contains password hashing and verification functions.

## 10. Screenshots / Results

Replace each placeholder with a real screenshot captured from the running application. No screenshots have been generated for this draft.

- [INSERT SCREENSHOT: Login Screen]
- [INSERT SCREENSHOT: Student Dashboard]
- [INSERT SCREENSHOT: Add Task]
- [INSERT SCREENSHOT: My Tasks]
- [INSERT SCREENSHOT: Progress Report]
- Optional: [INSERT SCREENSHOT: Subjects Window]

## 11. Testing Approach

`test_project.py` uses Python's `unittest` module and creates a temporary database for every test case. It checks database table creation, registration, successful and failed login, legacy password migration, task CRUD operations, owner scoping, input validation, and progress calculations. The tests do not use or erase the real application database.

Run the tests with `python -m unittest -v test_project.py` from the project directory.

## 12. Challenges Faced

The original project already had working command-line backend features and a partial GUI, so a key task was connecting new GUI windows without replacing the existing database structure. Another important point was keeping task changes restricted to the logged-in student's records while still showing readable subject names.

## 13. Learnings and Key Takeaways

This project demonstrates how Python modules can work together, how Tkinter widgets can collect and display data, and how SQLite can persist related records. It also provides practice with input validation, parameterized database queries, password hashing, and automated tests using a temporary database.

## 14. Future Enhancements

- Add task search, filters, or sorting controls.
- Add reminders for upcoming due dates.
- Allow safe editing and deletion of subjects.
- Add export options for progress reports.
- Improve the visual layout based on student feedback.

## 15. References

- Python documentation: https://docs.python.org/3/
- Tkinter documentation: https://docs.python.org/3/library/tkinter.html
- SQLite documentation: https://www.sqlite.org/docs.html
- Python `unittest` documentation: https://docs.python.org/3/library/unittest.html
- Mermaid documentation: https://mermaid.js.org/
