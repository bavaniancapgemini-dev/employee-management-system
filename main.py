from database import (
    create_table,
    add_employee,
    show_employees,
    search_employee,
    delete_employee,
    update_salary
)

from reports import (
    highest_salary,
    average_salary
)

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
    print("8. Exit")

    choice = input("Choose: ")

    if choice == "1":

        name = input("Employee Name: ")

        department = input("Department: ")

        salary = int(input("Salary: "))

        add_employee(name, department, salary)

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

        print("Goodbye")

        break

    else:

        print("Invalid Choice")