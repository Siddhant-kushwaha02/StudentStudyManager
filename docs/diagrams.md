# System Design Diagrams

The Mermaid diagrams below describe the current desktop application and its intended data flow.

## 1. System Architecture Diagram

```mermaid
flowchart LR
    Student[Student]
    GUI[Tkinter GUI\ngui.py]
    Auth[User management\nregister.py + login.py]
    Tasks[Task management\ntask_manager.py]
    Subjects[Subject management\nsubject_manager.py]
    Reports[Progress & reports\nreports.py]
    DBLayer[SQLite access\ndatabase.py]
    DB[(study_manager.db)]
    Student --> GUI
    GUI --> Auth
    GUI --> Tasks
    GUI --> Subjects
    GUI --> Reports
    Auth --> DBLayer
    Tasks --> DBLayer
    Subjects --> DBLayer
    Reports --> DBLayer
    DBLayer --> DB
```

## 2. User Workflow Diagram

```mermaid
flowchart TD
    Start([Start application]) --> Login{Existing account?}
    Login -- No --> Register[Register account]
    Register --> SignIn[Enter email and password]
    Login -- Yes --> SignIn
    SignIn --> Valid{Credentials valid?}
    Valid -- No --> SignIn
    Valid -- Yes --> Dashboard[Student dashboard]
    Dashboard --> Choice{Choose feature}
    Choice --> AddTask[Add task]
    Choice --> ViewTasks[View, update, complete, or delete own tasks]
    Choice --> Subject[View or add subjects]
    Choice --> Progress[View progress]
    AddTask --> Dashboard
    ViewTasks --> Dashboard
    Subject --> Dashboard
    Progress --> Dashboard
    Dashboard --> Logout[Logout]
    Logout --> End([Finish])
```

## 3. Use Case Diagram

```mermaid
flowchart LR
    Student((Student))
    subgraph System[Student Study & Task Management System]
        Register[Register]
        Login[Log in]
        ManageTasks[Add and view personal tasks]
        Update[Update task]
        Complete[Mark task completed]
        Delete[Delete task]
        ManageSubjects[View and add subjects]
        ViewProgress[View progress report]
        Logout[Log out]
    end
    Student --> Register
    Student --> Login
    Student --> ManageTasks
    Student --> Update
    Student --> Complete
    Student --> Delete
    Student --> ManageSubjects
    Student --> ViewProgress
    Student --> Logout
```

## 4. Sequence Diagram

```mermaid
sequenceDiagram
    actor Student
    participant GUI as Tkinter GUI
    participant Auth as Login module
    participant DB as SQLite database
    Student->>GUI: Enter email and password
    GUI->>Auth: authenticate_user(email, password)
    Auth->>DB: Find account by email
    DB-->>Auth: Account and stored password hash
    Auth-->>GUI: Student ID, name, role or no match
    GUI-->>Student: Show dashboard or login error
    Student->>GUI: Open My Tasks
    GUI->>DB: Select tasks for logged-in student ID
    DB-->>GUI: Task rows with subject names
    GUI-->>Student: Display task table
```

## 5. Class/Component Diagram

```mermaid
classDiagram
    class GUI {
        +run_gui()
        +dashboard(user)
        +my_tasks_window(parent, user_id)
        +subjects_window(parent)
        +progress_window(parent, user_id)
    }
    class UserManagement {
        +create_user(name, email, password)
        +authenticate_user(email, password)
    }
    class TaskManager {
        +create_task(user_id, subject_id, name, due_date, priority)
        +get_tasks(user_id)
        +update_task_details(...)
        +mark_task_completed(user_id, task_id)
        +delete_task_by_id(user_id, task_id)
    }
    class SubjectManager {
        +get_subjects()
        +create_subject(subject_name)
    }
    class Reports {
        +get_progress(user_id)
    }
    class Database {
        +connect_db()
        +create_tables()
    }
    GUI --> UserManagement
    GUI --> TaskManager
    GUI --> SubjectManager
    GUI --> Reports
    UserManagement --> Database
    TaskManager --> Database
    SubjectManager --> Database
    Reports --> Database
```

## 6. ER Diagram

```mermaid
erDiagram
    USER ||--o{ TASK : owns
    SUBJECT ||--o{ TASK : classifies
    USER {
        int user_id PK
        string name
        string email UK
        string password
        string role
    }
    SUBJECT {
        int subject_id PK
        string subject_name
    }
    TASK {
        int task_id PK
        int user_id FK
        int subject_id FK
        string task_name
        string due_date
        string priority
        string status
    }
```

A user can have zero or many tasks. A subject can be used by zero or many tasks. Every task is associated with one user and one subject in normal application use.
