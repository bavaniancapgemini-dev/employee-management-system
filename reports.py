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

def average_salary():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT AVG(salary) FROM employees"
    )

    data = cursor.fetchone()

    connection.close()

    return data

import sqlite3

def department_report():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT department, COUNT(*)
    FROM employees
    GROUP BY department
    """)

    data = cursor.fetchall()

    connection.close()

    return data

def top_performer():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM employees
    ORDER BY rating DESC
    LIMIT 1
    """)

    data = cursor.fetchone()

    connection.close()

    return data

def total_employees():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM employees"
    )

    data = cursor.fetchone()

    connection.close()

    return data[0]