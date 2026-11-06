
import sqlite3
from datetime import datetime


def create_payroll_table():

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payroll(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            month TEXT,
            year INTEGER,
            basic_salary REAL,
            hra REAL,
            allowances REAL,
            overtime REAL,
            tax REAL,
            pf REAL,
            other_deductions REAL,
            gross_salary REAL,
            net_salary REAL,
            payment_status TEXT DEFAULT 'Pending',
            generated_on TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    """)

    connection.commit()
    connection.close()


def calculate_salary(basic_salary, hra, allowances,
                     overtime, tax, pf, other_deductions):

    gross_salary = basic_salary + hra + allowances + overtime

    total_deductions = tax + pf + other_deductions

    net_salary = gross_salary - total_deductions

    return gross_salary, net_salary


def generate_payroll(employee_id, month, year, basic_salary,
                     hra, allowances, overtime, tax, pf,
                     other_deductions):

    gross, net = calculate_salary(
        basic_salary,
        hra,
        allowances,
        overtime,
        tax,
        pf,
        other_deductions
    )

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO payroll(
            employee_id, month, year, basic_salary,
            hra, allowances, overtime, tax, pf,
            other_deductions, gross_salary, net_salary
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        employee_id, month, year, basic_salary,
        hra, allowances, overtime, tax, pf,
        other_deductions, gross, net
    ))

    connection.commit()
    connection.close()

    return gross, net


def view_payroll():

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT payroll.*, employees.name
        FROM payroll
        JOIN employees ON payroll.employee_id = employees.id
        ORDER BY payroll.year DESC, payroll.id DESC
    """)

    records = cursor.fetchall()
    connection.close()

    return records


def update_payment_status(payroll_id, status):

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE payroll
        SET payment_status = ?
        WHERE id = ?
    """, (status, payroll_id))

    connection.commit()
    connection.close()
