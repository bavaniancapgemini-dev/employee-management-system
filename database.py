import sqlite3


def create_table():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        salary INTEGER,
        rating INTEGER
    )
    """)

    connection.commit()

    connection.close()


def add_employee(name, department, salary, rating):

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO employees(name, department, salary, rating) VALUES (?, ?, ?, ?)",
        (name, department, salary, rating)
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

def search_employee(name):

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM employees WHERE name=?",
        (name,)
    )

    data = cursor.fetchall()

    connection.close()

    return data

def delete_employee(employee_id):

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=?",
        (employee_id,)
    )

    connection.commit()

    connection.close()

def update_salary(employee_id, new_salary):

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute(
        "UPDATE employees SET salary=? WHERE id=?",
        (new_salary, employee_id)
    )

    connection.commit()

    connection.close()