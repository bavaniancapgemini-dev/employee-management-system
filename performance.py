
import sqlite3


def create_performance_table():

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_reviews(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            review_period TEXT NOT NULL,
            reviewer TEXT NOT NULL,
            rating INTEGER NOT NULL,
            strengths TEXT,
            areas_to_improve TEXT,
            comments TEXT,
            review_date TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (employee_id)
            REFERENCES employees(id),

            CHECK (rating BETWEEN 1 AND 10)
        )
    """)

    connection.commit()
    connection.close()


def add_performance_review(
    employee_id,
    review_period,
    reviewer,
    rating,
    strengths,
    areas_to_improve,
    comments
):

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM employees WHERE id = ?",
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:
        connection.close()
        return False, "Employee ID does not exist."

    if not 1 <= rating <= 10:
        connection.close()
        return False, "Rating must be between 1 and 10."

    cursor.execute("""
        INSERT INTO performance_reviews(
            employee_id,
            review_period,
            reviewer,
            rating,
            strengths,
            areas_to_improve,
            comments
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        employee_id,
        review_period,
        reviewer,
        rating,
        strengths,
        areas_to_improve,
        comments
    ))

    connection.commit()
    connection.close()

    return True, "Performance review added successfully."


def view_performance_reviews():

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            performance_reviews.id,
            employees.id,
            employees.name,
            performance_reviews.review_period,
            performance_reviews.reviewer,
            performance_reviews.rating,
            performance_reviews.strengths,
            performance_reviews.areas_to_improve,
            performance_reviews.comments,
            performance_reviews.review_date

        FROM performance_reviews

        JOIN employees
        ON performance_reviews.employee_id = employees.id

        ORDER BY performance_reviews.id DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data


def employee_performance_history(employee_id):

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            review_period,
            reviewer,
            rating,
            strengths,
            areas_to_improve,
            comments,
            review_date

        FROM performance_reviews

        WHERE employee_id = ?

        ORDER BY id DESC
    """, (employee_id,))

    data = cursor.fetchall()

    connection.close()

    return data


def department_performance_report():

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            employees.department,
            COUNT(performance_reviews.id),
            ROUND(AVG(performance_reviews.rating), 2)

        FROM employees

        LEFT JOIN performance_reviews
        ON employees.id = performance_reviews.employee_id

        GROUP BY employees.department
    """)

    data = cursor.fetchall()

    connection.close()

    return data


def create_review_interactive():

    print("\n========== ADD PERFORMANCE REVIEW ==========")

    try:
        employee_id = int(input("Enter Employee ID: "))
        rating = int(input("Performance Rating (1-10): "))

    except ValueError:
        print("Employee ID and rating must be numbers.")
        return

    review_period = input(
        "Review Period (e.g. November 2026): "
    ).strip()

    reviewer = input("Reviewer Name: ").strip()

    strengths = input("Employee Strengths: ").strip()

    areas_to_improve = input(
        "Areas for Improvement: "
    ).strip()

    comments = input("Additional Comments: ").strip()

    if not review_period or not reviewer:
        print("Review period and reviewer are required.")
        return

    success, message = add_performance_review(
        employee_id,
        review_period,
        reviewer,
        rating,
        strengths,
        areas_to_improve,
        comments
    )

    print(message)


def display_performance_reviews():

    print("\n========== PERFORMANCE REVIEWS ==========")

    reviews = view_performance_reviews()

    if reviews:

        for review in reviews:
            print("\nReview ID:", review[0])
            print("Employee ID:", review[1])
            print("Employee Name:", review[2])
            print("Review Period:", review[3])
            print("Reviewer:", review[4])
            print("Rating:", review[5], "/ 10")
            print("Strengths:", review[6])
            print("Areas to Improve:", review[7])
            print("Comments:", review[8])
            print("Review Date:", review[9])

    else:

        print("No performance reviews found.")


def display_department_performance():

    print("\n========== DEPARTMENT PERFORMANCE ==========")

    reports = department_performance_report()

    for report in reports:

        print(
            "Department:", report[0],
            "| Total Reviews:", report[1],
            "| Average Rating:", report[2]
        )
