import sqlite3


def mark_attendance(employee_id):

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER
    )
    """)

    cursor.execute(
        "INSERT INTO attendance(employee_id) VALUES (?)",
        (employee_id,)
    )

    connection.commit()

    connection.close()


def view_attendance():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM attendance")

    data = cursor.fetchall()

    connection.close()

    return data
