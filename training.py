import sqlite3
import csv
import json
import os

from datetime import date, datetime


DATABASE_NAME = "employees.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# ==========================================
# 1. CREATE TRAINING DATABASE TABLES
# ==========================================

def create_training_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL UNIQUE,
            description TEXT,
            duration_hours INTEGER DEFAULT 0,
            trainer_name TEXT,
            created_on TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Not Started',
            assessment_score REAL,
            certificate_name TEXT,
            enrolled_on TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_on TEXT,
            UNIQUE(employee_id, course_id),
            FOREIGN KEY(employee_id) REFERENCES employees(id),
            FOREIGN KEY(course_id) REFERENCES training_courses(id)
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# 2. ADD TRAINING COURSE
# ==========================================

def add_training_course(
    course_name,
    description,
    duration_hours,
    trainer_name
):

    course_name = course_name.strip()

    if not course_name:
        return False, "Course name is required."

    if duration_hours < 0:
        return False, "Duration cannot be negative."

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO training_courses (
                course_name,
                description,
                duration_hours,
                trainer_name
            )
            VALUES (?, ?, ?, ?)
        """, (
            course_name,
            description.strip(),
            duration_hours,
            trainer_name.strip()
        ))

        connection.commit()

        return True, "Training course added successfully."

    except sqlite3.IntegrityError:

        return False, "A course with this name already exists."

    finally:
        connection.close()


# ==========================================
# 3. VIEW TRAINING COURSES
# ==========================================

def view_training_courses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            course_name,
            description,
            duration_hours,
            trainer_name
        FROM training_courses
        ORDER BY id
    """)

    courses = cursor.fetchall()

    connection.close()

    return courses


def display_training_courses():

    print("\n========== TRAINING COURSES ==========")

    courses = view_training_courses()

    if not courses:
        print("No training courses available.")
        return

    for course in courses:

        print("\nCourse ID:", course[0])
        print("Course Name:", course[1])
        print("Description:", course[2])
        print("Duration:", course[3], "hours")
        print("Trainer:", course[4])
        
# ==========================================
# 3A. UPDATE TRAINING COURSE
# ==========================================

def update_training_course(
    course_id,
    course_name,
    description,
    duration_hours,
    trainer_name
):

    course_name = course_name.strip()

    if not course_name:
        return False, "Course name is required."

    if duration_hours < 0:
        return False, "Duration cannot be negative."

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM training_courses WHERE id = ?",
        (course_id,)
    )

    course = cursor.fetchone()

    if course is None:
        connection.close()
        return False, "Course ID does not exist."

    try:

        cursor.execute("""
            UPDATE training_courses
            SET course_name = ?,
                description = ?,
                duration_hours = ?,
                trainer_name = ?
            WHERE id = ?
        """, (
            course_name,
            description.strip(),
            duration_hours,
            trainer_name.strip(),
            course_id
        ))

        connection.commit()

        return True, "Training course updated successfully."

    except sqlite3.IntegrityError:

        return False, "Another course already has this name."

    finally:
        connection.close()


# ==========================================
# 3B. DELETE TRAINING COURSE
# ==========================================

def delete_training_course(course_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM training_courses
        WHERE id = ?
    """, (course_id,))

    course = cursor.fetchone()

    if course is None:
        connection.close()
        return False, "Course ID does not exist."

    cursor.execute("""
        SELECT COUNT(*)
        FROM training_enrollments
        WHERE course_id = ?
    """, (course_id,))

    enrollment_count = cursor.fetchone()[0]

    if enrollment_count > 0:
        connection.close()
        return False, (
            "Cannot delete this course because employees "
            "are enrolled in it."
        )

    cursor.execute("""
        DELETE FROM training_courses
        WHERE id = ?
    """, (course_id,))

    connection.commit()
    connection.close()

    return True, "Training course deleted successfully."


# ==========================================
# 4. ENROLL EMPLOYEE IN TRAINING
# ==========================================

def enroll_employee(employee_id, course_id):

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

    cursor.execute(
        "SELECT id FROM training_courses WHERE id = ?",
        (course_id,)
    )

    course = cursor.fetchone()

    if course is None:
        connection.close()
        return False, "Training course ID does not exist."

    try:

        cursor.execute("""
            INSERT INTO training_enrollments (
                employee_id,
                course_id
            )
            VALUES (?, ?)
        """, (employee_id, course_id))

        connection.commit()

        return True, "Employee enrolled successfully."

    except sqlite3.IntegrityError:

        return False, "This employee is already enrolled in this course."

    finally:
        connection.close()


# ==========================================
# 5. VIEW ALL ENROLLMENTS
# ==========================================

def view_training_enrollments():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            training_enrollments.id,
            employees.id,
            employees.name,
            training_courses.course_name,
            training_enrollments.status,
            training_enrollments.assessment_score,
            training_enrollments.certificate_name,
            training_enrollments.enrolled_on,
            training_enrollments.completed_on
        FROM training_enrollments
        JOIN employees
            ON training_enrollments.employee_id = employees.id
        JOIN training_courses
            ON training_enrollments.course_id = training_courses.id
        ORDER BY training_enrollments.id DESC
    """)

    enrollments = cursor.fetchall()

    connection.close()

    return enrollments


def display_training_enrollments():

    print("\n========== TRAINING ENROLLMENTS ==========")

    enrollments = view_training_enrollments()

    if not enrollments:
        print("No training enrollments found.")
        return

    for item in enrollments:

        print("\nEnrollment ID:", item[0])
        print("Employee ID:", item[1])
        print("Employee Name:", item[2])
        print("Course:", item[3])
        print("Status:", item[4])
        print("Assessment Score:", item[5])
        print("Certificate:", item[6])
        print("Enrolled On:", item[7])
        print("Completed On:", item[8])


# ==========================================
# 6. UPDATE TRAINING PROGRESS
# ==========================================

def update_training_progress(enrollment_id, status):

    allowed_statuses = [
        "Not Started",
        "In Progress",
        "Completed"
    ]

    if status not in allowed_statuses:
        return False, "Invalid training status."

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM training_enrollments
        WHERE id = ?
    """, (enrollment_id,))

    enrollment = cursor.fetchone()

    if enrollment is None:
        connection.close()
        return False, "Enrollment ID does not exist."

    completed_on = None

    if status == "Completed":
        completed_on = date.today().isoformat()

    cursor.execute("""
        UPDATE training_enrollments
        SET status = ?,
            completed_on = ?
        WHERE id = ?
    """, (status, completed_on, enrollment_id))

    connection.commit()
    connection.close()

    return True, "Training progress updated successfully."


# ==========================================
# 7. SAVE ASSESSMENT SCORE
# ==========================================

def save_assessment_score(enrollment_id, score):

    if score < 0 or score > 100:
        return False, "Score must be between 0 and 100."

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM training_enrollments
        WHERE id = ?
    """, (enrollment_id,))

    enrollment = cursor.fetchone()

    if enrollment is None:
        connection.close()
        return False, "Enrollment ID does not exist."

    cursor.execute("""
        UPDATE training_enrollments
        SET assessment_score = ?
        WHERE id = ?
    """, (score, enrollment_id))

    connection.commit()
    connection.close()

    return True, "Assessment score saved successfully."


# ==========================================
# 8. ADD CERTIFICATE
# ==========================================

def add_training_certificate(enrollment_id, certificate_name):

    certificate_name = certificate_name.strip()

    if not certificate_name:
        return False, "Certificate name is required."

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status
        FROM training_enrollments
        WHERE id = ?
    """, (enrollment_id,))

    enrollment = cursor.fetchone()

    if enrollment is None:
        connection.close()
        return False, "Enrollment ID does not exist."

    if enrollment[0] != "Completed":
        connection.close()
        return False, "Complete the training before adding a certificate."

    cursor.execute("""
        UPDATE training_enrollments
        SET certificate_name = ?
        WHERE id = ?
    """, (certificate_name, enrollment_id))

    connection.commit()
    connection.close()

    return True, "Certificate recorded successfully."


# ==========================================
# 9. EMPLOYEE TRAINING HISTORY
# ==========================================

def employee_training_history(employee_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            training_courses.course_name,
            training_enrollments.status,
            training_enrollments.assessment_score,
            training_enrollments.certificate_name,
            training_enrollments.enrolled_on,
            training_enrollments.completed_on
        FROM training_enrollments
        JOIN training_courses
            ON training_enrollments.course_id = training_courses.id
        WHERE training_enrollments.employee_id = ?
        ORDER BY training_enrollments.id DESC
    """, (employee_id,))

    history = cursor.fetchall()

    connection.close()

    return history


def display_employee_training_history(employee_id):

    print("\n========== MY TRAINING HISTORY ==========")

    history = employee_training_history(employee_id)

    if not history:
        print("No training records found.")
        return

    for item in history:

        print("\nCourse:", item[0])
        print("Status:", item[1])
        print("Assessment Score:", item[2])
        print("Certificate:", item[3])
        print("Enrolled On:", item[4])
        print("Completed On:", item[5])


# ==========================================
# 10. TRAINING REPORT
# ==========================================

def training_summary_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN status = 'Not Started' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END),
            SUM(CASE WHEN certificate_name IS NOT NULL THEN 1 ELSE 0 END)
        FROM training_enrollments
    """)

    report = cursor.fetchone()

    connection.close()

    return report


def display_training_summary_report():

    print("\n========== TRAINING SUMMARY REPORT ==========")

    report = training_summary_report()

    print("Total Enrollments:", report[0] or 0)
    print("Not Started:", report[1] or 0)
    print("In Progress:", report[2] or 0)
    print("Completed:", report[3] or 0)
    print("Certificates Recorded:", report[4] or 0)


# ==========================================
# 11. DEPARTMENT TRAINING REPORT
# ==========================================

def department_training_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            employees.department,
            COUNT(training_enrollments.id),
            SUM(
                CASE
                    WHEN training_enrollments.status = 'Completed'
                    THEN 1 ELSE 0
                END
            )
        FROM employees
        LEFT JOIN training_enrollments
            ON employees.id = training_enrollments.employee_id
        GROUP BY employees.department
        ORDER BY employees.department
    """)

    report = cursor.fetchall()

    connection.close()

    return report


def display_department_training_report():

    print("\n========== DEPARTMENT TRAINING REPORT ==========")

    report = department_training_report()

    if not report:
        print("No employee records found.")
        return

    for item in report:

        print("\nDepartment:", item[0] or "Not Assigned")
        print("Total Enrollments:", item[1])
        print("Completed Trainings:", item[2] or 0)


# ==========================================
# 12. INTERACTIVE FUNCTIONS
# ==========================================

def create_training_course_interactive():

    print("\n========== ADD TRAINING COURSE ==========")

    course_name = input("Course Name: ").strip()
    description = input("Description: ").strip()
    trainer_name = input("Trainer Name: ").strip()

    try:
        duration = int(input("Duration in Hours: "))

    except ValueError:
        print("Please enter a valid number.")
        return

    success, message = add_training_course(
        course_name,
        description,
        duration,
        trainer_name
    )

    print(message)


def enroll_employee_interactive():

    print("\n========== EMPLOYEE TRAINING ENROLLMENT ==========")

    try:
        employee_id = int(input("Employee ID: "))

        display_training_courses()

        course_id = int(input("\nCourse ID: "))

    except ValueError:
        print("Please enter valid numeric IDs.")
        return

    success, message = enroll_employee(employee_id, course_id)

    print(message)


def update_training_progress_interactive():

    print("\n========== UPDATE TRAINING PROGRESS ==========")

    display_training_enrollments()

    try:
        enrollment_id = int(input("\nEnrollment ID: "))

    except ValueError:
        print("Please enter a valid enrollment ID.")
        return

    print("\n1. Not Started")
    print("2. In Progress")
    print("3. Completed")

    choice = input("Select Status: ").strip()

    statuses = {
        "1": "Not Started",
        "2": "In Progress",
        "3": "Completed"
    }

    if choice not in statuses:
        print("Invalid status choice.")
        return

    success, message = update_training_progress(
        enrollment_id,
        statuses[choice]
    )

    print(message)


def save_assessment_interactive():

    print("\n========== SAVE ASSESSMENT SCORE ==========")

    display_training_enrollments()

    try:
        enrollment_id = int(input("\nEnrollment ID: "))
        score = float(input("Assessment Score (0-100): "))

    except ValueError:
        print("Please enter valid numbers.")
        return

    success, message = save_assessment_score(
        enrollment_id,
        score
    )

    print(message)


def add_certificate_interactive():

    print("\n========== RECORD CERTIFICATE ==========")

    display_training_enrollments()

    try:
        enrollment_id = int(input("\nEnrollment ID: "))

    except ValueError:
        print("Please enter a valid enrollment ID.")
        return

    certificate_name = input("Certificate Name: ").strip()

    success, message = add_training_certificate(
        enrollment_id,
        certificate_name
    )

    print(message)
    
def update_training_course_interactive():

    print("\n========== UPDATE TRAINING COURSE ==========")

    display_training_courses()

    try:
        course_id = int(input("\nEnter Course ID: "))

    except ValueError:
        print("Please enter a valid course ID.")
        return

    course_name = input("New Course Name: ").strip()
    description = input("New Description: ").strip()
    trainer_name = input("New Trainer Name: ").strip()

    try:
        duration = int(input("New Duration in Hours: "))

    except ValueError:
        print("Please enter a valid duration.")
        return

    success, message = update_training_course(
        course_id,
        course_name,
        description,
        duration,
        trainer_name
    )

    print(message)


def delete_training_course_interactive():

    print("\n========== DELETE TRAINING COURSE ==========")

    display_training_courses()

    try:
        course_id = int(input("\nEnter Course ID to Delete: "))

    except ValueError:
        print("Please enter a valid course ID.")
        return

    confirmation = input(
        "Are you sure you want to delete this course? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Course deletion cancelled.")
        return

    success, message = delete_training_course(course_id)

    print(message)
    
# ==========================================
# 12A. TRAINING ANALYTICS
# ==========================================

def training_analytics_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM training_courses
    """)
    total_courses = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Not Started' THEN 1 ELSE 0 END),
            AVG(assessment_score),
            SUM(
                CASE
                    WHEN certificate_name IS NOT NULL
                    AND TRIM(certificate_name) != ''
                    THEN 1 ELSE 0
                END
            )
        FROM training_enrollments
    """)

    result = cursor.fetchone()

    total_enrollments = result[0] or 0
    completed = result[1] or 0
    in_progress = result[2] or 0
    not_started = result[3] or 0
    average_score = result[4]
    certificates = result[5] or 0

    completion_rate = 0

    if total_enrollments > 0:
        completion_rate = (
            completed / total_enrollments
        ) * 100

    average_score = average_score or 0

    connection.close()

    return {
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "completed": completed,
        "in_progress": in_progress,
        "not_started": not_started,
        "average_score": average_score,
        "certificates": certificates,
        "completion_rate": completion_rate
    }


# ==========================================
# 12B. COURSE POPULARITY REPORT
# ==========================================

def course_popularity_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            training_courses.course_name,
            COUNT(training_enrollments.id) AS total_enrollments,
            SUM(
                CASE
                    WHEN training_enrollments.status = 'Completed'
                    THEN 1 ELSE 0
                END
            ) AS completed
        FROM training_courses
        LEFT JOIN training_enrollments
            ON training_courses.id = training_enrollments.course_id
        GROUP BY training_courses.id, training_courses.course_name
        ORDER BY total_enrollments DESC,
                 training_courses.course_name
    """)

    report = cursor.fetchall()

    connection.close()

    return report


# ==========================================
# 12C. DISPLAY TRAINING ANALYTICS
# ==========================================

def display_training_analytics():

    print("\n===================================")
    print("       TRAINING ANALYTICS")
    print("===================================")

    report = training_analytics_report()

    print("\n========== KEY PERFORMANCE INDICATORS ==========")

    print("Total Training Courses:", report["total_courses"])
    print("Total Enrollments:", report["total_enrollments"])
    print("Completed Trainings:", report["completed"])
    print("In Progress:", report["in_progress"])
    print("Not Started:", report["not_started"])

    print(
        "Training Completion Rate:",
        round(report["completion_rate"], 2),
        "%"
    )

    print(
        "Average Assessment Score:",
        round(report["average_score"], 2),
        "%"
    )

    print("Certificates Issued:", report["certificates"])

    print("\n========== COURSE POPULARITY ==========")

    courses = course_popularity_report()

    if not courses:
        print("No training courses available.")

    else:

        for course in courses:

            print("\nCourse:", course[0])
            print("Total Enrollments:", course[1])
            print("Completed Enrollments:", course[2] or 0)

    print("\n===================================")
    
# ==========================================
# 12D. EXPORT TRAINING DATA TO CSV
# ==========================================

def export_training_to_csv():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            training_enrollments.id AS enrollment_id,
            employees.id AS employee_id,
            employees.name AS employee_name,
            employees.department,
            training_courses.id AS course_id,
            training_courses.course_name,
            training_courses.duration_hours,
            training_courses.trainer_name,
            training_enrollments.status,
            training_enrollments.assessment_score,
            training_enrollments.certificate_name,
            training_enrollments.enrolled_on,
            training_enrollments.completed_on
        FROM training_enrollments
        JOIN employees
            ON training_enrollments.employee_id = employees.id
        JOIN training_courses
            ON training_enrollments.course_id = training_courses.id
        ORDER BY training_enrollments.id
    """)

    rows = cursor.fetchall()
    connection.close()

    os.makedirs("exports", exist_ok=True)

    file_path = os.path.join("exports", "training_report.csv")

    headers = [
        "Enrollment ID",
        "Employee ID",
        "Employee Name",
        "Department",
        "Course ID",
        "Course Name",
        "Duration Hours",
        "Trainer",
        "Status",
        "Assessment Score",
        "Certificate",
        "Enrolled On",
        "Completed On"
    ]

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(headers)
        writer.writerows(rows)

    return file_path, len(rows)


# ==========================================
# 12E. EXPORT TRAINING DATA TO JSON
# ==========================================

def export_training_to_json():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            course_name,
            description,
            duration_hours,
            trainer_name,
            created_on
        FROM training_courses
        ORDER BY id
    """)

    courses = cursor.fetchall()

    course_headers = [
        "course_id",
        "course_name",
        "description",
        "duration_hours",
        "trainer_name",
        "created_on"
    ]

    course_data = [
        dict(zip(course_headers, course))
        for course in courses
    ]

    cursor.execute("""
        SELECT
            training_enrollments.id,
            employees.id,
            employees.name,
            employees.department,
            training_courses.course_name,
            training_enrollments.status,
            training_enrollments.assessment_score,
            training_enrollments.certificate_name,
            training_enrollments.enrolled_on,
            training_enrollments.completed_on
        FROM training_enrollments
        JOIN employees
            ON training_enrollments.employee_id = employees.id
        JOIN training_courses
            ON training_enrollments.course_id = training_courses.id
        ORDER BY training_enrollments.id
    """)

    enrollments = cursor.fetchall()
    connection.close()

    enrollment_headers = [
        "enrollment_id",
        "employee_id",
        "employee_name",
        "department",
        "course_name",
        "status",
        "assessment_score",
        "certificate_name",
        "enrolled_on",
        "completed_on"
    ]

    enrollment_data = [
        dict(zip(enrollment_headers, enrollment))
        for enrollment in enrollments
    ]

    export_data = {
        "exported_on": datetime.now().isoformat(timespec="seconds"),
        "total_courses": len(course_data),
        "total_enrollments": len(enrollment_data),
        "courses": course_data,
        "enrollments": enrollment_data
    }

    os.makedirs("exports", exist_ok=True)

    file_path = os.path.join("exports", "training_report.json")

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            export_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    return file_path, len(enrollment_data)


# ==========================================
# 12F. INTERACTIVE TRAINING EXPORT
# ==========================================

def export_training_interactive():

    while True:

        print("\n========== EXPORT TRAINING DATA ==========")

        print("1. Export to CSV")
        print("2. Export to JSON")
        print("3. Export to Both Formats")
        print("4. Back")

        choice = input("Choose: ").strip()

        if choice == "1":

            path, count = export_training_to_csv()

            print("\nCSV export completed.")
            print("File:", os.path.abspath(path))
            print("Exported enrollments:", count)

        elif choice == "2":

            path, count = export_training_to_json()

            print("\nJSON export completed.")
            print("File:", os.path.abspath(path))
            print("Exported enrollments:", count)

        elif choice == "3":

            csv_path, csv_count = export_training_to_csv()

            json_path, json_count = export_training_to_json()

            print("\nBoth exports completed.")

            print("CSV File:", os.path.abspath(csv_path))
            print("JSON File:", os.path.abspath(json_path))

            print("CSV enrollments:", csv_count)
            print("JSON enrollments:", json_count)

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")

# ==========================================
# 13. TRAINING MANAGEMENT MENU
# ==========================================

def training_management_menu():

    while True:

        print("\n===================================")
        print("     TRAINING MANAGEMENT")
        print("===================================")

        print("1. Add Training Course")
        print("2. View Training Courses")
        print("3. Enroll Employee")
        print("4. View Training Enrollments")
        print("5. Update Training Progress")
        print("6. Save Assessment Score")
        print("7. Record Certificate")
        print("8. Training Summary Report")
        print("9. Department Training Report")
        print("10. Update Training Course")
        print("11. Delete Training Course")
        print("12. Training Analytics Dashboard")
        print("13. Export Training Data")
        print("14. Back to Dashboard")

        choice = input("Choose: ").strip()

        if choice == "1":
            create_training_course_interactive()

        elif choice == "2":
            display_training_courses()

        elif choice == "3":
            enroll_employee_interactive()

        elif choice == "4":
            display_training_enrollments()

        elif choice == "5":
            update_training_progress_interactive()

        elif choice == "6":
            save_assessment_interactive()

        elif choice == "7":
            add_certificate_interactive()

        elif choice == "8":
            display_training_summary_report()

        elif choice == "9":
            display_department_training_report()

        elif choice == "10":
            update_training_course_interactive()

        elif choice == "11":
            delete_training_course_interactive()

        elif choice == "12":
            display_training_analytics()

        elif choice == "13":
            export_training_interactive()

        elif choice == "14":
            break

        else:
            print("Invalid choice. Please try again.")