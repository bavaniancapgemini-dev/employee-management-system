import sqlite3


def highest_salary():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM employees ORDER BY salary DESC LIMIT 1"
    )

    data = cursor.fetchone()

    connection.close()

    return data