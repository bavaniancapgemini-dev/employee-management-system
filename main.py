
from database import (
    create_table,
    add_employee,
    show_employees,
    search_employee,
    delete_employee,
    update_salary,
    apply_leave,
    view_leave_requests,
    update_leave_status,
    employee_leave_history
)

from payroll import (
    create_payroll_table,
    generate_payroll,
    view_payroll,
    update_payment_status
)

from reports import (
    highest_salary,
    average_salary,
    department_report,
    top_performer,
    total_employees
)

from attendance import (
    create_attendance_table,
    mark_attendance,
    view_attendance
)

from auth import (
    create_auth_table,
    login_user,
    create_account,
    change_account_password
)

from performance import create_performance_table
from organization import create_organization_tables
from training import create_training_tables

from roles import open_role_dashboard

from backup import export_employees
from utils import line
from getpass import getpass


# INITIALIZE DATABASE

create_table()
create_auth_table()
create_payroll_table()
create_attendance_table()
create_performance_table()
create_organization_tables()
create_training_tables()

# MAIN LOGIN SYSTEM

while True:

    line()

    print("EMPLOYEE MANAGEMENT SYSTEM")

    line()

    print("1. Login")
    print("2. Exit")

    choice = input("Choose: ")

    if choice == "1":

        print("\n========== LOGIN ==========")

        username = input("Username: ").strip()
        password = getpass("Password: ")

        user = login_user(username, password)

        if user:

            print("\nLogin Successful!")
            print("Welcome:", user["username"])
            print("Role:", user["role"])

            open_role_dashboard(user)

            print("\nLogged out successfully.")

        else:

            print("\nInvalid username or password.")
            print("Your account may also be inactive.")

    elif choice == "2":

        print("Goodbye!")
        break

    else:

        print("Invalid choice.")
