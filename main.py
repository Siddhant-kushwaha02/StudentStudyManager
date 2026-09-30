from database import create_tables


if __name__ == "__main__":
    create_tables()
    from gui import run_gui

    run_gui()