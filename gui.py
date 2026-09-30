"""Tkinter interface for the Student Study & Task Management System."""

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from database import connect_db
from login import authenticate_user
from password_utils import hash_password
from register import create_user
from reports import get_progress
from subject_manager import create_subject, get_subjects
from task_manager import (
    create_task,
    delete_task_by_id,
    get_tasks,
    mark_task_completed,
    update_task_details,
)


def register_window(parent):
    window = tk.Toplevel(parent)
    window.title("Student Registration")
    window.geometry("400x400")
    window.transient(parent)

    tk.Label(window, text="Student Registration", font=("Arial", 20, "bold")).pack(pady=20)
    fields = {}
    for label in ("Name", "Email", "Password"):
        tk.Label(window, text=label).pack()
        entry = tk.Entry(window, width=30, show="*" if label == "Password" else "")
        entry.pack(pady=5)
        fields[label] = entry

    def register():
        try:
            create_user(fields["Name"].get(), fields["Email"].get(), fields["Password"].get())
        except ValueError as error:
            messagebox.showwarning("Check registration details", str(error), parent=window)
            return
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration failed", "This email is already registered.", parent=window)
            return
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not register: {error}", parent=window)
            return
        messagebox.showinfo("Success", "Registration successful!", parent=window)
        window.destroy()

    tk.Button(window, text="Register", width=15, command=register).pack(pady=20)


def _subject_map():
    return {name: subject_id for subject_id, name in get_subjects()}


def add_task_window(parent, user_id, on_saved=None):
    window = tk.Toplevel(parent)
    window.title("Add Task")
    window.geometry("400x450")
    tk.Label(window, text="ADD TASK", font=("Arial", 20, "bold")).pack(pady=20)

    tk.Label(window, text="Task Name").pack()
    task_entry = tk.Entry(window, width=35)
    task_entry.pack(pady=5)
    tk.Label(window, text="Subject").pack()
    try:
        subjects = _subject_map()
    except sqlite3.Error as error:
        messagebox.showerror("Database error", f"Could not load subjects: {error}", parent=window)
        window.destroy()
        return
    if not subjects:
        messagebox.showinfo("No subjects", "Add a subject before creating a task.", parent=window)
        window.destroy()
        return
    subject_var = tk.StringVar(value=next(iter(subjects)))
    ttk.OptionMenu(window, subject_var, subject_var.get(), *subjects.keys()).pack(pady=5)

    tk.Label(window, text="Due Date (YYYY-MM-DD or DD-MM-YYYY)").pack()
    date_entry = tk.Entry(window, width=35)
    date_entry.pack(pady=5)
    tk.Label(window, text="Priority").pack()
    priority_var = tk.StringVar(value="Medium")
    ttk.OptionMenu(window, priority_var, "Medium", "Low", "Medium", "High").pack(pady=5)

    def save_task():
        try:
            create_task(user_id, subjects[subject_var.get()], task_entry.get(), date_entry.get(), priority_var.get())
        except ValueError as error:
            messagebox.showwarning("Check task details", str(error), parent=window)
            return
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not add task: {error}", parent=window)
            return
        messagebox.showinfo("Success", "Task added successfully!", parent=window)
        if on_saved:
            on_saved()
        window.destroy()

    tk.Button(window, text="Add Task", width=20, command=save_task).pack(pady=20)


def my_tasks_window(parent, user_id):
    window = tk.Toplevel(parent)
    window.title("My Tasks")
    window.geometry("900x500")
    columns = ("Task ID", "Task Name", "Subject", "Due Date", "Priority", "Status")
    table = ttk.Treeview(window, columns=columns, show="headings", selectmode="browse")
    widths = (75, 220, 150, 120, 90, 100)
    for column, width in zip(columns, widths):
        table.heading(column, text=column)
        table.column(column, width=width, anchor="center" if column != "Task Name" else "w")
    table.pack(fill="both", expand=True, padx=12, pady=12)

    def refresh():
        table.delete(*table.get_children())
        try:
            rows = get_tasks(user_id)
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not load tasks: {error}", parent=window)
            return
        for row in rows:
            table.insert("", "end", values=tuple(value if value is not None else "(No subject)" for value in row))

    def selected_task():
        selection = table.selection()
        if not selection:
            messagebox.showwarning("Select a task", "Choose a task from the table first.", parent=window)
            return None
        return table.item(selection[0], "values")

    def complete_task():
        row = selected_task()
        if not row:
            return
        try:
            updated = mark_task_completed(user_id, row[0])
        except (ValueError, sqlite3.Error) as error:
            messagebox.showerror("Could not complete task", str(error), parent=window)
            return
        if not updated:
            messagebox.showwarning("Task not found", "That task is no longer available.", parent=window)
        refresh()

    def delete_task():
        row = selected_task()
        if not row or not messagebox.askyesno("Delete task", f"Delete '{row[1]}'?", parent=window):
            return
        try:
            deleted = delete_task_by_id(user_id, row[0])
        except (ValueError, sqlite3.Error) as error:
            messagebox.showerror("Could not delete task", str(error), parent=window)
            return
        if not deleted:
            messagebox.showwarning("Task not found", "That task is no longer available.", parent=window)
        refresh()

    def edit_task():
        row = selected_task()
        if not row:
            return
        try:
            subjects = _subject_map()
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not load subjects: {error}", parent=window)
            return
        if not subjects:
            messagebox.showinfo("No subjects", "Add a subject before updating this task.", parent=window)
            return
        edit = tk.Toplevel(window)
        edit.title("Update Task")
        edit.geometry("380x360")
        tk.Label(edit, text="Task Name").pack(pady=(12, 0))
        name_entry = tk.Entry(edit, width=35)
        name_entry.insert(0, row[1])
        name_entry.pack(pady=5)
        tk.Label(edit, text="Subject").pack()
        subject_names = list(subjects)
        current_subject = row[2] if row[2] in subjects else subject_names[0]
        subject_var = tk.StringVar(value=current_subject)
        ttk.OptionMenu(edit, subject_var, current_subject, *subject_names).pack(pady=5)
        tk.Label(edit, text="Due Date (YYYY-MM-DD or DD-MM-YYYY)").pack()
        date_entry = tk.Entry(edit, width=35)
        date_entry.insert(0, row[3])
        date_entry.pack(pady=5)
        tk.Label(edit, text="Priority").pack()
        priority_var = tk.StringVar(value=row[4] if row[4] in ("Low", "Medium", "High") else "Medium")
        ttk.OptionMenu(edit, priority_var, priority_var.get(), "Low", "Medium", "High").pack(pady=5)

        def save_changes():
            try:
                updated = update_task_details(
                    user_id, row[0], subjects[subject_var.get()], name_entry.get(),
                    date_entry.get(), priority_var.get(),
                )
            except ValueError as error:
                messagebox.showwarning("Check task details", str(error), parent=edit)
                return
            except sqlite3.Error as error:
                messagebox.showerror("Database error", f"Could not update task: {error}", parent=edit)
                return
            if not updated:
                messagebox.showwarning("Task not found", "That task is no longer available.", parent=edit)
                return
            edit.destroy()
            refresh()

        tk.Button(edit, text="Save Changes", command=save_changes).pack(pady=15)

    buttons = tk.Frame(window)
    buttons.pack(pady=(0, 12))
    tk.Button(buttons, text="Refresh", width=14, command=refresh).pack(side="left", padx=5)
    tk.Button(buttons, text="Mark Completed", width=16, command=complete_task).pack(side="left", padx=5)
    tk.Button(buttons, text="Update Task", width=14, command=edit_task).pack(side="left", padx=5)
    tk.Button(buttons, text="Delete Task", width=14, command=delete_task).pack(side="left", padx=5)
    refresh()


def subjects_window(parent):
    window = tk.Toplevel(parent)
    window.title("Subjects")
    window.geometry("450x420")
    tk.Label(window, text="Subjects", font=("Arial", 18, "bold")).pack(pady=12)
    table = ttk.Treeview(window, columns=("Subject ID", "Subject Name"), show="headings", height=12)
    table.heading("Subject ID", text="Subject ID")
    table.heading("Subject Name", text="Subject Name")
    table.column("Subject ID", width=100, anchor="center")
    table.column("Subject Name", width=280)
    table.pack(fill="both", expand=True, padx=15, pady=8)

    def refresh():
        table.delete(*table.get_children())
        try:
            for subject in get_subjects():
                table.insert("", "end", values=subject)
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not load subjects: {error}", parent=window)

    def add_subject():
        name = subject_entry.get()
        try:
            create_subject(name)
        except ValueError as error:
            messagebox.showwarning("Check subject name", str(error), parent=window)
            return
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not add subject: {error}", parent=window)
            return
        subject_entry.delete(0, tk.END)
        refresh()

    entry_frame = tk.Frame(window)
    entry_frame.pack(pady=8)
    tk.Label(entry_frame, text="New subject:").pack(side="left", padx=5)
    subject_entry = tk.Entry(entry_frame, width=25)
    subject_entry.pack(side="left", padx=5)
    tk.Button(entry_frame, text="Add Subject", command=add_subject).pack(side="left", padx=5)
    tk.Button(window, text="Refresh", command=refresh).pack(pady=(0, 12))
    refresh()


def progress_window(parent, user_id):
    window = tk.Toplevel(parent)
    window.title("My Progress")
    window.geometry("400x350")
    tk.Label(window, text="MY PROGRESS", font=("Arial", 20, "bold")).pack(pady=20)
    values = {}
    for label in ("Total Tasks", "Completed Tasks", "Pending Tasks", "Completion Percentage"):
        line = tk.Frame(window)
        line.pack(fill="x", padx=45, pady=10)
        tk.Label(line, text=f"{label}:", font=("Arial", 12)).pack(side="left")
        value = tk.Label(line, text="", font=("Arial", 12, "bold"))
        value.pack(side="right")
        values[label] = value

    def refresh():
        try:
            progress = get_progress(user_id)
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not load progress: {error}", parent=window)
            return
        values["Total Tasks"].config(text=str(progress["total_tasks"]))
        values["Completed Tasks"].config(text=str(progress["completed_tasks"]))
        values["Pending Tasks"].config(text=str(progress["pending_tasks"]))
        values["Completion Percentage"].config(text=f"{progress['completion_percentage']:.2f}%")

    tk.Button(window, text="Refresh", command=refresh).pack(pady=18)
    refresh()


def dashboard(user):
    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Student Dashboard")
    dashboard_window.geometry("600x500")
    dashboard_window.transient(root)
    tk.Label(dashboard_window, text="STUDENT STUDY MANAGER", font=("Arial", 22, "bold")).pack(pady=25)
    tk.Label(dashboard_window, text=f"Welcome, {user[1]}!", font=("Arial", 15)).pack(pady=10)
    button_frame = tk.Frame(dashboard_window)
    button_frame.pack(pady=30)

    tk.Button(button_frame, text="Add Task", width=20, height=2,
              command=lambda: add_task_window(dashboard_window, user[0])).grid(row=0, column=0, padx=15, pady=15)
    tk.Button(button_frame, text="My Tasks", width=20, height=2,
              command=lambda: my_tasks_window(dashboard_window, user[0])).grid(row=0, column=1, padx=15, pady=15)
    tk.Button(button_frame, text="Subjects", width=20, height=2,
              command=lambda: subjects_window(dashboard_window)).grid(row=1, column=0, padx=15, pady=15)
    tk.Button(button_frame, text="Progress", width=20, height=2,
              command=lambda: progress_window(dashboard_window, user[0])).grid(row=1, column=1, padx=15, pady=15)

    def logout():
        dashboard_window.destroy()
        email_entry.focus_set()

    tk.Button(dashboard_window, text="Logout", width=20, command=logout).pack(pady=20)
    dashboard_window.protocol("WM_DELETE_WINDOW", logout)


def run_gui():
    global root, email_entry, password_entry
    root = tk.Tk()
    root.title("Student Study Manager")
    root.geometry("500x500")
    tk.Label(root, text="STUDENT STUDY MANAGER", font=("Arial", 22, "bold")).pack(pady=40)
    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root, width=35)
    email_entry.pack(pady=8)
    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, width=35, show="*")
    password_entry.pack(pady=8)

    def login():
        try:
            user = authenticate_user(email_entry.get(), password_entry.get())
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not log in: {error}", parent=root)
            return
        if user:
            password_entry.delete(0, tk.END)
            dashboard(user)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.", parent=root)

    tk.Button(root, text="Login", width=20, command=login).pack(pady=20)
    tk.Button(root, text="Register", width=20, command=lambda: register_window(root)).pack()
    root.mainloop()


if __name__ == "__main__":
    run_gui()
