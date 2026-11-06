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
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leave_requests(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        leave_type TEXT,
        start_date TEXT,
        end_date TEXT,
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        applied_on TEXT DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (employee_id) REFERENCES employees(id)
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
    
def apply_leave(employee_id, leave_type, start_date, end_date, reason):

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO leave_requests
        (employee_id, leave_type, start_date, end_date, reason)
        VALUES (?, ?, ?, ?, ?)
    """, (employee_id, leave_type, start_date, end_date, reason))

    connection.commit()
    connection.close()


def view_leave_requests():

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            leave_requests.id,
            employees.name,
            leave_requests.leave_type,
            leave_requests.start_date,
            leave_requests.end_date,
            leave_requests.reason,
            leave_requests.status,
            leave_requests.applied_on
        FROM leave_requests
        JOIN employees
        ON leave_requests.employee_id = employees.id
        ORDER BY leave_requests.id DESC
    """)

    data = cursor.fetchall()
    connection.close()

    return data


def update_leave_status(leave_id, status):

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE leave_requests
        SET status = ?
        WHERE id = ?
    """, (status, leave_id))

    connection.commit()
    connection.close()


def employee_leave_history(employee_id):

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM leave_requests
        WHERE employee_id = ?
        ORDER BY id DESC
    """, (employee_id,))

    data = cursor.fetchall()
    connection.close()

    return data