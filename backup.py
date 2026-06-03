import sqlite3
import json


def export_employees():

    connection = sqlite3.connect("employees.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    employee_list = []

    for employee in employees:

        employee_list.append({
            "id": employee[0],
            "name": employee[1],
            "department": employee[2],
            "salary": employee[3]
        })

    with open("employees.json", "w") as file:

        json.dump(employee_list, file, indent=4)

    connection.close()