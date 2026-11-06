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

from reports import (
    highest_salary,
    average_salary,
    department_report,
    top_performer,
    total_employees
)

from attendance import (
    mark_attendance,
    view_attendance
)

from backup import export_employees

from utils import line



create_table()


while True:

    line()

    print("EMPLOYEE MANAGEMENT SYSTEM")

    line()

    print("1. Add Employee")
    print("2. View Employees")
    print("3. Highest Salary")
    print("4. Search Employee")
    print("5. Delete Employee")
    print("6. Update Salary")
    print("7. Average Salary")
    print("8. Department Report")
    print("9. Mark Attendance")
    print("10. View Attendance")
    print("11. Export JSON")
    print("12. Top Performer")
    print("13. Dashboard")
    print("14. Apply for Leave")
    print("15. View Leave Requests")
    print("16. Approve / Reject Leave")
    print("17. Employee Leave History")
    print("18. Exit")

    choice = input("Choose: ")

    if choice == "1":

        name = input("Employee Name: ")

        department = input("Department: ")

        salary = int(input("Salary: "))

        rating = int(input("Performance Rating (1-10): "))

        add_employee(name, department, salary, rating)

        print("Employee Added")

    elif choice == "2":

        employees = show_employees()

        for employee in employees:

            print(employee)

    elif choice == "3":

        employee = highest_salary()

        print("\nHighest Salary Employee:")
        print(employee)

    elif choice == "4":

        name = input("Enter employee name: ")

        result = search_employee(name)

        for employee in result:

            print(employee)

    elif choice == "5":

        employee_id = int(input("Enter employee ID: "))

        delete_employee(employee_id)

        print("Employee Deleted")

    elif choice == "6":

        employee_id = int(input("Enter employee ID: "))

        new_salary = int(input("Enter new salary: "))

        update_salary(employee_id, new_salary)

        print("Salary Updated")

    elif choice == "7":

        avg = average_salary()

        print("Average Salary:", avg[0])

    elif choice == "8":

        report = department_report()

        for department in report:

            print(department)

    elif choice == "9":

        employee_id = int(input("Enter employee ID: "))

        mark_attendance(employee_id)

        print("Attendance Marked")

    elif choice == "10":

        records = view_attendance()

        for record in records:

            print(record)

    elif choice == "11":

        export_employees()

        print("JSON Export Complete")

    elif choice == "12":

        employee = top_performer()

        print(employee)

    elif choice == "13":

        print("Total Employees:", total_employees())

        print("Average Salary:", average_salary())

        print("Top Performer:", top_performer())

    elif choice == "14":

        print("\n--- APPLY FOR LEAVE ---")

        employee_id = int(input("Employee ID: "))
        leave_type = input("Leave Type (Casual/Sick/Earned): ")
        start_date = input("Start Date (YYYY-MM-DD): ")
        end_date = input("End Date (YYYY-MM-DD): ")
        reason = input("Reason: ")

        employees = show_employees()

        if any(employee[0] == employee_id for employee in employees):

            apply_leave(
                employee_id,
                leave_type,
                start_date,
                end_date,
                reason
            )

            print("Leave Application Submitted!")

        else:

            print("Employee ID not found.")

    elif choice == "15":

        print("\n--- ALL LEAVE REQUESTS ---")

        requests = view_leave_requests()

        if requests:

            for request in requests:
                print(request)

        else:

            print("No leave requests found.")

    elif choice == "16":

        print("\n--- APPROVE / REJECT LEAVE ---")

        leave_id = int(input("Enter Leave Request ID: "))

        status = input("Enter status (Approved/Rejected): ").strip().title()

        if status in ["Approved", "Rejected"]:

            update_leave_status(leave_id, status)

            print("Leave Status Updated!")

        else:

            print("Invalid status.")

    elif choice == "17":

        print("\n--- EMPLOYEE LEAVE HISTORY ---")

        employee_id = int(input("Enter Employee ID: "))

        history = employee_leave_history(employee_id)

        if history:

            for record in history:
                print(record)

        else:

            print("No leave history found.")

    elif choice == "18":

        print("Goodbye")

        break

    else:

        print("Invalid Choice")