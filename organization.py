
import sqlite3


DATABASE_NAME = "employees.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_organization_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_on TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS designations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            designation_name TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            description TEXT,
            created_on TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (designation_name, department_id),
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    """)

    # Add designation column to the existing employees table
    cursor.execute("PRAGMA table_info(employees)")
    columns = [column[1] for column in cursor.fetchall()]

    if "designation" not in columns:
        cursor.execute("""
            ALTER TABLE employees
            ADD COLUMN designation TEXT
        """)

    # Bring existing employee departments into the new department table
    cursor.execute("""
        SELECT DISTINCT department
        FROM employees
        WHERE department IS NOT NULL
        AND TRIM(department) != ''
    """)

    existing_departments = cursor.fetchall()

    for department in existing_departments:
        cursor.execute("""
            INSERT OR IGNORE INTO departments (department_name)
            VALUES (?)
        """, (department[0].strip(),))

    connection.commit()
    connection.close()


def add_department(department_name, description):

    department_name = department_name.strip()

    if not department_name:
        return False, "Department name is required."

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO departments (department_name, description)
            VALUES (?, ?)
        """, (department_name, description.strip()))

        connection.commit()
        return True, "Department added successfully."

    except sqlite3.IntegrityError:
        return False, "This department already exists."

    finally:
        connection.close()


def view_departments():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, department_name, description, created_on
        FROM departments
        ORDER BY department_name
    """)

    departments = cursor.fetchall()
    connection.close()

    return departments


def add_designation(
    designation_name,
    department_id,
    description
):

    designation_name = designation_name.strip()

    if not designation_name:
        return False, "Designation name is required."

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM departments WHERE id = ?",
        (department_id,)
    )

    department = cursor.fetchone()

    if department is None:
        connection.close()
        return False, "Department ID does not exist."

    try:
        cursor.execute("""
            INSERT INTO designations (
                designation_name,
                department_id,
                description
            )
            VALUES (?, ?, ?)
        """, (
            designation_name,
            department_id,
            description.strip()
        ))

        connection.commit()
        return True, "Designation added successfully."

    except sqlite3.IntegrityError:
        return False, "This designation already exists in that department."

    finally:
        connection.close()


def view_designations():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            designations.id,
            designations.designation_name,
            departments.department_name,
            designations.description
        FROM designations
        JOIN departments
        ON designations.department_id = departments.id
        ORDER BY departments.department_name,
                 designations.designation_name
    """)

    designations = cursor.fetchall()
    connection.close()

    return designations


def assign_employee(employee_id, department_id, designation_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM employees WHERE id = ?",
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:
        connection.close()
        return False, "Employee ID does not exist."

    cursor.execute("""
        SELECT department_name
        FROM departments
        WHERE id = ?
    """, (department_id,))

    department = cursor.fetchone()

    if department is None:
        connection.close()
        return False, "Department ID does not exist."

    cursor.execute("""
        SELECT id
        FROM designations
        WHERE id = ?
        AND department_id = ?
    """, (designation_id, department_id))

    designation = cursor.fetchone()

    if designation is None:
        connection.close()
        return False, "Designation does not belong to this department."

    cursor.execute("""
        SELECT designation_name
        FROM designations
        WHERE id = ?
    """, (designation_id,))

    designation_name = cursor.fetchone()[0]

    cursor.execute("""
        UPDATE employees
        SET department = ?,
            designation = ?
        WHERE id = ?
    """, (
        department[0],
        designation_name,
        employee_id
    ))

    connection.commit()
    connection.close()

    return True, "Employee department and designation updated."


def department_employee_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            departments.id,
            departments.department_name,
            COUNT(employees.id)
        FROM departments
        LEFT JOIN employees
        ON departments.department_name = employees.department
        GROUP BY departments.id, departments.department_name
        ORDER BY departments.department_name
    """)

    report = cursor.fetchall()
    connection.close()

    return report


def display_departments():

    print("\n========== DEPARTMENTS ==========")

    departments = view_departments()

    if not departments:
        print("No departments found.")
        return

    for department in departments:
        print("\nDepartment ID:", department[0])
        print("Name:", department[1])
        print("Description:", department[2])


def display_designations():

    print("\n========== DESIGNATIONS ==========")

    designations = view_designations()

    if not designations:
        print("No designations found.")
        return

    for designation in designations:
        print("\nDesignation ID:", designation[0])
        print("Name:", designation[1])
        print("Department:", designation[2])
        print("Description:", designation[3])


def create_department_interactive():

    print("\n========== ADD DEPARTMENT ==========")

    name = input("Department Name: ").strip()
    description = input("Description: ").strip()

    success, message = add_department(name, description)

    print(message)


def create_designation_interactive():

    print("\n========== ADD DESIGNATION ==========")

    display_departments()

    try:
        department_id = int(input("\nEnter Department ID: "))

    except ValueError:
        print("Please enter a valid department ID.")
        return

    name = input("Designation Name: ").strip()
    description = input("Description: ").strip()

    success, message = add_designation(
        name,
        department_id,
        description
    )

    print(message)


def assign_employee_interactive():

    print("\n========== ASSIGN EMPLOYEE ==========")

    try:
        employee_id = int(input("Employee ID: "))

    except ValueError:
        print("Employee ID must be a number.")
        return

    display_departments()

    try:
        department_id = int(input("\nDepartment ID: "))

    except ValueError:
        print("Department ID must be a number.")
        return

    display_designations()

    try:
        designation_id = int(input("\nDesignation ID: "))

    except ValueError:
        print("Designation ID must be a number.")
        return

    success, message = assign_employee(
        employee_id,
        department_id,
        designation_id
    )

    print(message)


def display_department_employee_report():

    print("\n========== DEPARTMENT EMPLOYEE REPORT ==========")

    report = department_employee_report()

    if not report:
        print("No departments found.")
        return

    total_employees = 0

    for item in report:

        print(
            "Department:", item[1],
            "| Employee Count:", item[2]
        )

        total_employees += item[2]

    print("\nTotal Employees:", total_employees)


def organization_management_menu():

    while True:

        print("\n===================================")
        print("     ORGANIZATION MANAGEMENT")
        print("===================================")

        print("1. Add Department")
        print("2. View Departments")
        print("3. Add Designation")
        print("4. View Designations")
        print("5. Assign Employee")
        print("6. Department Employee Report")
        print("7. Back to Dashboard")

        choice = input("Choose: ").strip()

        if choice == "1":
            create_department_interactive()

        elif choice == "2":
            display_departments()

        elif choice == "3":
            create_designation_interactive()

        elif choice == "4":
            display_designations()

        elif choice == "5":
            assign_employee_interactive()

        elif choice == "6":
            display_department_employee_report()

        elif choice == "7":
            break

        else:
            print("Invalid choice. Please try again.")
