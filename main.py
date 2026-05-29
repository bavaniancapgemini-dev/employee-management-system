from database import (
    create_table,
    add_employee,
    show_employees
)

from reports import highest_salary

from utils import line


create_table()


while True:

    line()

    print("EMPLOYEE MANAGEMENT SYSTEM")

    line()

    print("1. Add Employee")
    print("2. View Employees")
    print("3. Highest Salary")
    print("4. Exit")

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

        print("Goodbye")

        break

    else:

        print("Invalid Choice")