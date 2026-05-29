import sqlite3


def create_table():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        salary INTEGER
    )
    """)

    connection.commit()

    connection.close()


def add_employee(name, department, salary):

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO employees(name, department, salary) VALUES (?, ?, ?)",
        (name, department, salary)
    )

    connection.commit()

    connection.close()


def show_employees():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM employees")

    data = cursor.fetchall()

    connection.close()

    return data