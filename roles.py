
from getpass import getpass

from database import (
    show_employees,
    search_employee,
    add_employee,
    delete_employee,
    update_salary,
    view_leave_requests,
    update_leave_status
)

from reports import (
    highest_salary,
    average_salary,
    department_report,
    top_performer,
    total_employees
)

from attendance import (
    mark_attendance,
    view_attendance,
    employee_attendance
)

from backup import export_employees
from payroll import view_payroll
from performance import (
    create_review_interactive,
    display_performance_reviews,
    employee_performance_history,
    display_department_performance
)
from organization import organization_management_menu

from auth import (
    view_accounts,
    update_account_status,
    create_account
)


def create_user_account():

    print("\n========== CREATE USER ACCOUNT ==========")
    print("1. HR Manager")
    print("2. Employee")

    role_choice = input("Choose account role: ").strip()

    if role_choice == "1":
        role = "HR Manager"
        employee_id = None

    elif role_choice == "2":
        role = "Employee"

        try:
            employee_id = int(input("Enter Employee ID: "))
        except ValueError:
            print("Employee ID must be a number.")
            return

        employees = show_employees()

        if not any(emp[0] == employee_id for emp in employees):
            print("Employee ID does not exist.")
            return

    else:
        print("Invalid role choice.")
        return

    username = input("Enter Username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    password = getpass("Enter Password: ")
    confirm_password = getpass("Confirm Password: ")

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    success, message = create_account(
        username,
        password,
        role,
        employee_id
    )

    print(message)


def show_reports():

    print("\n========== DASHBOARD REPORTS ==========")

    print("Total Employees:", total_employees())
    print("Average Salary:", average_salary())
    print("Highest Salary:", highest_salary())
    print("Top Performer:", top_performer())

    print("\nDepartment Report:")

    for department in department_report():
        print(department)


def display_leave_requests():

    requests = view_leave_requests()

    if requests:
        for request in requests:
            print(request)
    else:
        print("No leave requests found.")


def change_leave_status():

    display_leave_requests()

    try:
        leave_id = int(input("\nEnter Leave Request ID: "))
    except ValueError:
        print("Leave ID must be a number.")
        return

    requests = view_leave_requests()

    if not any(request[0] == leave_id for request in requests):
        print("Leave request not found.")
        return

    print("1. Approve")
    print("2. Reject")

    choice = input("Choose: ").strip()

    if choice == "1":
        status = "Approved"
    elif choice == "2":
        status = "Rejected"
    else:
        print("Invalid choice.")
        return

    update_leave_status(leave_id, status)
    print("Leave request status updated to", status)


def admin_dashboard(user):

    while True:

        print("\n========== ADMIN DASHBOARD ==========")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Search Employee")
        print("4. Delete Employee")
        print("5. Update Employee Salary")
        print("6. Dashboard Reports")
        print("7. Mark Attendance")
        print("8. View Attendance")
        print("9. View Payroll")
        print("10. View Leave Requests")
        print("11. Approve / Reject Leave")
        print("12. View User Accounts")
        print("13. Activate / Deactivate Account")
        print("14. Create HR / Employee Account")
        print("15. Export Employees")
        print("16. Performance Review Management")
        print("17. Organization Management")
        print("18. Logout")

        choice = input("Choose: ").strip()

        if choice == "1":

            name = input("Employee Name: ").strip()
            department = input("Department: ").strip()

            try:
                salary = int(input("Salary: "))
                rating = int(input("Rating (1-10): "))

                if salary < 0 or not 1 <= rating <= 10:
                    print("Enter a valid salary and rating.")
                    continue

            except ValueError:
                print("Salary and rating must be numbers.")
                continue

            if not name or not department:
                print("Name and department cannot be empty.")
                continue

            add_employee(name, department, salary, rating)
            print("Employee added successfully.")

        elif choice == "2":

            for employee in show_employees():
                print(employee)

        elif choice == "3":

            name = input("Enter Employee Name: ").strip()

            results = search_employee(name)

            if results:
                for employee in results:
                    print(employee)
            else:
                print("Employee not found.")

        elif choice == "4":

            try:
                employee_id = int(input("Enter Employee ID: "))
            except ValueError:
                print("Employee ID must be a number.")
                continue

            employee = next(
                (emp for emp in show_employees()
                 if emp[0] == employee_id),
                None
            )

            if employee is None:
                print("Employee not found.")
                continue

            print("Employee:", employee)
            confirm = input("Delete this employee? (yes/no): ").strip().lower()

            if confirm == "yes":
                delete_employee(employee_id)
                print("Employee deleted.")
            else:
                print("Deletion cancelled.")

        elif choice == "5":

            try:
                employee_id = int(input("Enter Employee ID: "))
                new_salary = int(input("Enter New Salary: "))

                if new_salary < 0:
                    print("Salary cannot be negative.")
                    continue

            except ValueError:
                print("Enter valid numbers.")
                continue

            if any(emp[0] == employee_id for emp in show_employees()):
                update_salary(employee_id, new_salary)
                print("Salary updated successfully.")
            else:
                print("Employee not found.")

        elif choice == "6":

            show_reports()

        elif choice == "7":

            try:
                employee_id = int(input("Enter Employee ID: "))
            except ValueError:
                print("Employee ID must be a number.")
                continue

            if any(emp[0] == employee_id for emp in show_employees()):
                mark_attendance(employee_id)
                print("Attendance marked successfully.")
            else:
                print("Employee not found.")

        elif choice == "8":

            records = view_attendance()

            if records:
                for record in records:
                    print(record)
            else:
                print("No attendance records found.")

        elif choice == "9":

            records = view_payroll()

            if records:
                for record in records:
                    print(record)
            else:
                print("No payroll records found.")

        elif choice == "10":

            display_leave_requests()

        elif choice == "11":

            change_leave_status()

        elif choice == "12":

            accounts = view_accounts()

            if accounts:
                for account in accounts:
                    print(account)
            else:
                print("No accounts found.")

        elif choice == "13":

            try:
                user_id = int(input("Enter Account ID: "))
            except ValueError:
                print("Account ID must be a number.")
                continue

            if user_id == user["id"]:
                print("You cannot deactivate your own account.")
                continue

            status = input(
                "Status (Active/Inactive): "
            ).strip().title()

            if update_account_status(user_id, status):
                print("Account status updated.")
            else:
                print("Invalid status or account ID.")

        elif choice == "14":

            create_user_account()

        elif choice == "15":

            export_employees()
            print("Export completed.")
            
        elif choice == "16":

            print("\n========== PERFORMANCE MANAGEMENT ==========")
            print("1. Add Performance Review")
            print("2. View All Performance Reviews")
            print("3. Department Performance Report")

            performance_choice = input("Choose: ").strip()

            if performance_choice == "1":

                create_review_interactive()

            elif performance_choice == "2":

                display_performance_reviews()

            elif performance_choice == "3":

                display_department_performance()

            else:

                print("Invalid choice.")

        elif choice == "17":

            organization_management_menu()

        elif choice == "18":

            print("Logging out...")
            break

        else:

            print("Invalid choice.")


def hr_dashboard(user):

    while True:

        print("\n========== HR MANAGER DASHBOARD ==========")
        print("1. View Employees")
        print("2. Search Employee")
        print("3. View Attendance")
        print("4. View Leave Requests")
        print("5. Approve / Reject Leave")
        print("6. View Payroll")
        print("7. Dashboard Reports")
        print("8. Performance Review Management")
        print("9. Organization Management")
        print("10. Logout")

        choice = input("Choose: ").strip()

        if choice == "1":

            for employee in show_employees():
                print(employee)

        elif choice == "2":

            name = input("Employee Name: ").strip()

            results = search_employee(name)

            if results:
                for employee in results:
                    print(employee)
            else:
                print("Employee not found.")

        elif choice == "3":

            records = view_attendance()

            if records:
                for record in records:
                    print(record)
            else:
                print("No attendance records found.")

        elif choice == "4":

            display_leave_requests()

        elif choice == "5":

            change_leave_status()

        elif choice == "6":

            records = view_payroll()

            if records:
                for record in records:
                    print(record)
            else:
                print("No payroll records found.")

        elif choice == "7":

            show_reports()
            
        elif choice == "8":
            
            print("\n========== PERFORMANCE MANAGEMENT ==========")
            print("1. Add Performance Review")
            print("2. View All Performance Reviews")
            print("3. Department Performance Report")

            performance_choice = input("Choose: ").strip()

            if performance_choice == "1":

                create_review_interactive()

            elif performance_choice == "2":

                display_performance_reviews()

            elif performance_choice == "3":

                display_department_performance()

            else:

                print("Invalid choice.")
                
        elif choice == "9":

            organization_management_menu()

        elif choice == "10":

            print("Logging out...")
            break

        else:

            print("Invalid choice.")


def employee_dashboard(user):

    while True:

        print("\n========== EMPLOYEE DASHBOARD ==========")
        print("1. View My Profile")
        print("2. View My Attendance")
        print("3. Apply for Leave")
        print("4. View My Leave History")
        print("5. View My Performance Reviews")
        print("6. Logout")

        choice = input("Choose: ").strip()

        employee_id = user["employee_id"]

        if choice == "1":

            if employee_id is None:
                print("No employee profile is linked to this account.")
                continue

            employee = next(
                (emp for emp in show_employees()
                 if emp[0] == employee_id),
                None
            )

            if employee:
                print(employee)
            else:
                print("Employee profile not found.")

        elif choice == "2":

            if employee_id is None:
                print("No employee profile is linked to this account.")
                continue

            records = employee_attendance(employee_id)

            if records:
                for record in records:
                    print(record)
            else:
                print("No attendance records found.")

        elif choice == "3":

            from database import apply_leave

            if employee_id is None:
                print("No employee profile is linked to this account.")
                continue

            leave_type = input("Leave Type: ")
            start_date = input("Start Date (YYYY-MM-DD): ")
            end_date = input("End Date (YYYY-MM-DD): ")
            reason = input("Reason: ")

            apply_leave(
                employee_id,
                leave_type,
                start_date,
                end_date,
                reason
            )

            print("Leave application submitted.")

        elif choice == "4":

            from database import employee_leave_history

            if employee_id is None:
                print("No employee profile is linked to this account.")
                continue

            records = employee_leave_history(employee_id)

            if records:
                for record in records:
                    print(record)
            else:
                print("No leave history found.")
                
        elif choice == "5":

            if employee_id is None:
                print("No employee profile is linked to this account.")
                continue

            records = employee_performance_history(employee_id)

            if records:

                for record in records:

                    print("\nReview ID:", record[0])
                    print("Review Period:", record[1])
                    print("Reviewer:", record[2])
                    print("Rating:", record[3], "/ 10")
                    print("Strengths:", record[4])
                    print("Areas to Improve:", record[5])
                    print("Comments:", record[6])
                    print("Review Date:", record[7])

            else:

                print("No performance reviews found.")

        elif choice == "6":

            print("Logging out...")
            break

        else:

            print("Invalid choice.")


def open_role_dashboard(user):

    if user["role"] == "Admin":
        admin_dashboard(user)

    elif user["role"] == "HR Manager":
        hr_dashboard(user)

    elif user["role"] == "Employee":
        employee_dashboard(user)

    else:
        print("Unknown user role.")
