import sqlite3
import csv
import os
from datetime import date, datetime

DATABASE_NAME = "employees.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# ==========================================
# CREATE CAREER DEVELOPMENT TABLES
# ==========================================

def create_career_development_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Performance Improvement Plans
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_improvement_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            plan_title TEXT NOT NULL,
            identified_issues TEXT,
            improvement_goals TEXT,
            action_plan TEXT,
            start_date TEXT,
            end_date TEXT,
            review_date TEXT,
            status TEXT DEFAULT 'Active',
            outcome TEXT,
            created_on TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    """)

    # Promotion Recommendations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promotion_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            current_designation TEXT,
            recommended_designation TEXT NOT NULL,
            current_salary REAL,
            proposed_salary REAL,
            justification TEXT,
            recommended_by TEXT,
            recommendation_date TEXT,
            status TEXT DEFAULT 'Pending',
            decision_comments TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    """)

    # Employee Achievements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            achievement_title TEXT NOT NULL,
            category TEXT,
            description TEXT,
            achievement_date TEXT,
            awarded_by TEXT,
            created_on TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    """)

    connection.commit()
    connection.close()

    print("Career Development database tables created successfully!")


# ==========================================
# DATABASE VERIFICATION
# ==========================================

def verify_career_development_tables():

    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== CAREER DEVELOPMENT TABLES ==========")

    tables = [
        "performance_improvement_plans",
        "promotion_recommendations",
        "employee_achievements"
    ]

    for table in tables:
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = ?
        """, (table,))

        result = cursor.fetchone()

        if result:
            print(f"{table}: Available")
        else:
            print(f"{table}: Missing")

    connection.close()
    

# ==========================================
# PERFORMANCE IMPROVEMENT PLAN MANAGEMENT
# ==========================================

def create_improvement_plan():

    print("\n========== CREATE IMPROVEMENT PLAN ==========")

    employee_id = input("Employee ID: ").strip()

    if not employee_id.isdigit():
        print("Invalid Employee ID!")
        return

    plan_title = input("Plan Title: ").strip()
    identified_issues = input("Identified Issues: ").strip()
    improvement_goals = input("Improvement Goals: ").strip()
    action_plan = input("Action Plan: ").strip()
    start_date = input("Start Date (YYYY-MM-DD): ").strip()
    end_date = input("End Date (YYYY-MM-DD): ").strip()
    review_date = input("Review Date (YYYY-MM-DD): ").strip()

    if not all([
        plan_title,
        identified_issues,
        improvement_goals,
        action_plan,
        start_date,
        end_date,
        review_date
    ]):
        print("All fields are required!")
        return

    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        review = date.fromisoformat(review_date)

        if end < start:
            print("End date cannot be before start date!")
            return

        if review < start:
            print("Review date cannot be before start date!")
            return

    except ValueError:
        print("Invalid date! Use YYYY-MM-DD.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM employees WHERE id = ?",
        (int(employee_id),)
    )

    employee = cursor.fetchone()

    if not employee:
        print("Employee not found!")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO performance_improvement_plans (
            employee_id,
            plan_title,
            identified_issues,
            improvement_goals,
            action_plan,
            start_date,
            end_date,
            review_date,
            status,
            created_on
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(employee_id),
        plan_title,
        identified_issues,
        improvement_goals,
        action_plan,
        start_date,
        end_date,
        review_date,
        "Active",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()

    print("Performance Improvement Plan created successfully!")


def view_improvement_plans():

    print("\n========== ALL IMPROVEMENT PLANS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.employee_id,
            e.name,
            p.plan_title,
            p.start_date,
            p.end_date,
            p.status,
            p.outcome
        FROM performance_improvement_plans p
        JOIN employees e ON p.employee_id = e.id
        ORDER BY p.id DESC
    """)

    plans = cursor.fetchall()
    connection.close()

    if not plans:
        print("No improvement plans found.")
        return

    for plan in plans:
        print("\n--------------------------------")
        print("Plan ID:", plan[0])
        print("Employee ID:", plan[1])
        print("Employee Name:", plan[2])
        print("Plan Title:", plan[3])
        print("Start Date:", plan[4])
        print("End Date:", plan[5])
        print("Status:", plan[6])
        print("Outcome:", plan[7] or "Not recorded")


def update_improvement_plan_status():

    print("\n========== UPDATE PLAN STATUS ==========")

    plan_id = input("Plan ID: ").strip()

    if not plan_id.isdigit():
        print("Invalid Plan ID!")
        return

    print("\n1. Active")
    print("2. Completed")
    print("3. On Hold")
    print("4. Cancelled")

    choice = input("Choose status: ").strip()

    statuses = {
        "1": "Active",
        "2": "Completed",
        "3": "On Hold",
        "4": "Cancelled"
    }

    if choice not in statuses:
        print("Invalid choice!")
        return

    status = statuses[choice]

    outcome = input("Enter review outcome (optional): ").strip()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE performance_improvement_plans
        SET status = ?, outcome = ?
        WHERE id = ?
    """, (status, outcome or None, int(plan_id)))

    if cursor.rowcount == 0:
        print("Improvement Plan not found!")
    else:
        connection.commit()
        print("Improvement Plan updated successfully!")

    connection.close()


def employee_improvement_history():

    print("\n========== EMPLOYEE IMPROVEMENT HISTORY ==========")

    employee_id = input("Employee ID: ").strip()

    if not employee_id.isdigit():
        print("Invalid Employee ID!")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            plan_title,
            improvement_goals,
            start_date,
            end_date,
            status,
            outcome
        FROM performance_improvement_plans
        WHERE employee_id = ?
        ORDER BY id DESC
    """, (int(employee_id),))

    plans = cursor.fetchall()
    connection.close()

    if not plans:
        print("No improvement history found.")
        return

    for plan in plans:
        print("\n--------------------------------")
        print("Plan ID:", plan[0])
        print("Title:", plan[1])
        print("Goals:", plan[2])
        print("Start Date:", plan[3])
        print("End Date:", plan[4])
        print("Status:", plan[5])
        print("Outcome:", plan[6] or "Not recorded")


def performance_improvement_menu():

    while True:

        print("\n====================================")
        print(" PERFORMANCE IMPROVEMENT MANAGEMENT")
        print("====================================")
        print("1. Create Improvement Plan")
        print("2. View All Improvement Plans")
        print("3. Update Plan Status")
        print("4. Employee Improvement History")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_improvement_plan()

        elif choice == "2":
            view_improvement_plans()

        elif choice == "3":
            update_improvement_plan_status()

        elif choice == "4":
            employee_improvement_history()

        elif choice == "5":
            break

        else:
            print("Invalid choice! Try again.")
            

# ==========================================
# PROMOTION RECOMMENDATION MANAGEMENT
# ==========================================

def create_promotion_recommendation():

    print("\n========== CREATE PROMOTION RECOMMENDATION ==========")

    employee_id = input("Employee ID: ").strip()

    if not employee_id.isdigit():
        print("Invalid Employee ID!")
        return

    current_designation = input("Current Designation: ").strip()
    recommended_designation = input("Recommended Designation: ").strip()

    try:
        current_salary = float(input("Current Salary: "))
        proposed_salary = float(input("Proposed Salary: "))

        if current_salary < 0 or proposed_salary < 0:
            print("Salary cannot be negative!")
            return

        if proposed_salary <= current_salary:
            print("Proposed salary should be greater than current salary!")
            return

    except ValueError:
        print("Enter valid salary amounts!")
        return

    justification = input("Promotion Justification: ").strip()
    recommended_by = input("Recommended By: ").strip()

    if not all([
        current_designation,
        recommended_designation,
        justification,
        recommended_by
    ]):
        print("All fields are required!")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM employees WHERE id = ?",
        (int(employee_id),)
    )

    if not cursor.fetchone():
        print("Employee not found!")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO promotion_recommendations (
            employee_id,
            current_designation,
            recommended_designation,
            current_salary,
            proposed_salary,
            justification,
            recommended_by,
            recommendation_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(employee_id),
        current_designation,
        recommended_designation,
        current_salary,
        proposed_salary,
        justification,
        recommended_by,
        date.today().isoformat(),
        "Pending"
    ))

    connection.commit()
    connection.close()

    print("Promotion recommendation created successfully!")


def view_promotion_recommendations():

    print("\n========== PROMOTION RECOMMENDATIONS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.employee_id,
            e.name,
            p.current_designation,
            p.recommended_designation,
            p.current_salary,
            p.proposed_salary,
            p.recommended_by,
            p.recommendation_date,
            p.status,
            p.justification,
            p.decision_comments
        FROM promotion_recommendations p
        JOIN employees e ON p.employee_id = e.id
        ORDER BY p.id DESC
    """)

    recommendations = cursor.fetchall()
    connection.close()

    if not recommendations:
        print("No promotion recommendations found.")
        return

    for item in recommendations:

        print("\n----------------------------------------")
        print("Recommendation ID:", item[0])
        print("Employee ID:", item[1])
        print("Employee Name:", item[2])
        print("Current Designation:", item[3])
        print("Recommended Designation:", item[4])
        print("Current Salary:", item[5])
        print("Proposed Salary:", item[6])
        print("Recommended By:", item[7])
        print("Recommendation Date:", item[8])
        print("Status:", item[9])
        print("Justification:", item[10])
        print("Decision Comments:", item[11] or "None")


def update_promotion_decision():

    print("\n========== PROMOTION DECISION ==========")

    recommendation_id = input("Recommendation ID: ").strip()

    if not recommendation_id.isdigit():
        print("Invalid Recommendation ID!")
        return

    print("\n1. Approve")
    print("2. Reject")
    print("3. Keep Pending")

    choice = input("Choose decision: ").strip()

    decisions = {
        "1": "Approved",
        "2": "Rejected",
        "3": "Pending"
    }

    if choice not in decisions:
        print("Invalid choice!")
        return

    status = decisions[choice]
    comments = input("Decision Comments: ").strip()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE promotion_recommendations
        SET status = ?, decision_comments = ?
        WHERE id = ?
    """, (
        status,
        comments,
        int(recommendation_id)
    ))

    if cursor.rowcount == 0:
        print("Recommendation not found!")
    else:
        connection.commit()
        print("Promotion decision updated successfully!")

    connection.close()


def employee_promotion_history():

    print("\n========== EMPLOYEE PROMOTION HISTORY ==========")

    employee_id = input("Employee ID: ").strip()

    if not employee_id.isdigit():
        print("Invalid Employee ID!")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            current_designation,
            recommended_designation,
            current_salary,
            proposed_salary,
            recommendation_date,
            status,
            decision_comments
        FROM promotion_recommendations
        WHERE employee_id = ?
        ORDER BY id DESC
    """, (int(employee_id),))

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("No promotion history found.")
        return

    for record in records:

        print("\n----------------------------------------")
        print("Recommendation ID:", record[0])
        print("Current Designation:", record[1])
        print("Recommended Designation:", record[2])
        print("Current Salary:", record[3])
        print("Proposed Salary:", record[4])
        print("Date:", record[5])
        print("Status:", record[6])
        print("Comments:", record[7] or "None")


def promotion_management_menu():

    while True:

        print("\n====================================")
        print(" PROMOTION RECOMMENDATION MANAGEMENT")
        print("====================================")
        print("1. Create Promotion Recommendation")
        print("2. View All Recommendations")
        print("3. Approve / Reject Recommendation")
        print("4. Employee Promotion History")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_promotion_recommendation()

        elif choice == "2":
            view_promotion_recommendations()

        elif choice == "3":
            update_promotion_decision()

        elif choice == "4":
            employee_promotion_history()

        elif choice == "5":
            break

        else:
            print("Invalid choice! Try again.")
            

# ==========================================
# EMPLOYEE ACHIEVEMENTS & RECOGNITION
# ==========================================

def add_employee_achievement():

    print("\n========== ADD EMPLOYEE ACHIEVEMENT ==========")

    employee_id = input("Employee ID: ").strip()

    if not employee_id.isdigit():
        print("Invalid Employee ID!")
        return

    title = input("Achievement Title: ").strip()
    category = input(
        "Category (Award/Certificate/Project/Recognition): "
    ).strip()
    description = input("Description: ").strip()
    achievement_date = input(
        "Achievement Date (YYYY-MM-DD): "
    ).strip()
    awarded_by = input("Awarded By: ").strip()

    if not all([
        title,
        category,
        description,
        achievement_date,
        awarded_by
    ]):
        print("All fields are required!")
        return

    try:
        date.fromisoformat(achievement_date)
    except ValueError:
        print("Invalid date! Use YYYY-MM-DD.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM employees WHERE id = ?",
        (int(employee_id),)
    )

    if not cursor.fetchone():
        print("Employee not found!")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO employee_achievements (
            employee_id,
            achievement_title,
            category,
            description,
            achievement_date,
            awarded_by,
            created_on
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        int(employee_id),
        title,
        category,
        description,
        achievement_date,
        awarded_by,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()

    print("Employee achievement recorded successfully!")


def view_all_achievements():

    print("\n========== EMPLOYEE ACHIEVEMENTS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            a.id,
            a.employee_id,
            e.name,
            a.achievement_title,
            a.category,
            a.description,
            a.achievement_date,
            a.awarded_by
        FROM employee_achievements a
        JOIN employees e ON a.employee_id = e.id
        ORDER BY a.achievement_date DESC
    """)

    achievements = cursor.fetchall()
    connection.close()

    if not achievements:
        print("No achievements found.")
        return

    for item in achievements:

        print("\n----------------------------------------")
        print("Achievement ID:", item[0])
        print("Employee ID:", item[1])
        print("Employee Name:", item[2])
        print("Title:", item[3])
        print("Category:", item[4])
        print("Description:", item[5])
        print("Achievement Date:", item[6])
        print("Awarded By:", item[7])


def employee_achievement_history():

    print("\n========== EMPLOYEE ACHIEVEMENT HISTORY ==========")

    employee_id = input("Employee ID: ").strip()

    if not employee_id.isdigit():
        print("Invalid Employee ID!")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            achievement_title,
            category,
            description,
            achievement_date,
            awarded_by
        FROM employee_achievements
        WHERE employee_id = ?
        ORDER BY achievement_date DESC
    """, (int(employee_id),))

    achievements = cursor.fetchall()
    connection.close()

    if not achievements:
        print("No achievements found for this employee.")
        return

    for item in achievements:

        print("\n----------------------------------------")
        print("Achievement ID:", item[0])
        print("Title:", item[1])
        print("Category:", item[2])
        print("Description:", item[3])
        print("Date:", item[4])
        print("Awarded By:", item[5])


def delete_employee_achievement():

    print("\n========== DELETE ACHIEVEMENT ==========")

    achievement_id = input("Achievement ID: ").strip()

    if not achievement_id.isdigit():
        print("Invalid Achievement ID!")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM employee_achievements
        WHERE id = ?
    """, (int(achievement_id),))

    if cursor.rowcount == 0:
        print("Achievement not found!")
    else:
        connection.commit()
        print("Achievement deleted successfully!")

    connection.close()


def achievement_management_menu():

    while True:

        print("\n====================================")
        print(" ACHIEVEMENT & RECOGNITION MANAGEMENT")
        print("====================================")
        print("1. Add Employee Achievement")
        print("2. View All Achievements")
        print("3. Employee Achievement History")
        print("4. Delete Achievement")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_employee_achievement()

        elif choice == "2":
            view_all_achievements()

        elif choice == "3":
            employee_achievement_history()

        elif choice == "4":
            delete_employee_achievement()

        elif choice == "5":
            break

        else:
            print("Invalid choice! Try again.")
            

# ==========================================
# CAREER DEVELOPMENT ANALYTICS DASHBOARD
# ==========================================

def career_development_dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    print("\n" + "=" * 50)
    print("       CAREER DEVELOPMENT DASHBOARD")
    print("=" * 50)

    # --------------------------------------
    # 1. IMPROVEMENT PLAN ANALYTICS
    # --------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM performance_improvement_plans
    """)
    total_plans = cursor.fetchone()[0]

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM performance_improvement_plans
        GROUP BY status
    """)
    plan_status = cursor.fetchall()

    print("\n--- PERFORMANCE IMPROVEMENT PLANS ---")
    print("Total Plans:", total_plans)

    for status, count in plan_status:
        print(f"{status} Plans: {count}")

    # --------------------------------------
    # 2. PROMOTION ANALYTICS
    # --------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM promotion_recommendations
    """)
    total_promotions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM promotion_recommendations
        GROUP BY status
    """)
    promotion_status = cursor.fetchall()

    print("\n--- PROMOTION RECOMMENDATIONS ---")
    print("Total Recommendations:", total_promotions)

    for status, count in promotion_status:
        print(f"{status} Recommendations: {count}")

    # --------------------------------------
    # 3. SALARY INCREASE ANALYSIS
    # --------------------------------------

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(proposed_salary - current_salary), 0),
            COALESCE(AVG(proposed_salary - current_salary), 0)
        FROM promotion_recommendations
        WHERE status = 'Approved'
    """)

    salary_data = cursor.fetchone()

    print("\n--- APPROVED PROMOTION SALARY ANALYSIS ---")
    print("Approved Promotions:", salary_data[0])
    print("Total Proposed Salary Increase:", round(salary_data[1], 2))
    print("Average Salary Increase:", round(salary_data[2], 2))

    # --------------------------------------
    # 4. ACHIEVEMENT ANALYTICS
    # --------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM employee_achievements
    """)
    total_achievements = cursor.fetchone()[0]

    print("\n--- EMPLOYEE ACHIEVEMENTS ---")
    print("Total Achievements:", total_achievements)

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM employee_achievements
        GROUP BY category
        ORDER BY COUNT(*) DESC
    """)

    achievement_categories = cursor.fetchall()

    print("\nAchievement Categories:")

    if achievement_categories:
        for category, count in achievement_categories:
            print(f"{category}: {count}")
    else:
        print("No achievement records available.")

    # --------------------------------------
    # 5. TOP EMPLOYEES BY ACHIEVEMENTS
    # --------------------------------------

    cursor.execute("""
        SELECT
            e.id,
            e.name,
            COUNT(a.id) AS achievement_count
        FROM employees e
        JOIN employee_achievements a
            ON e.id = a.employee_id
        GROUP BY e.id, e.name
        ORDER BY achievement_count DESC, e.name
        LIMIT 5
    """)

    top_employees = cursor.fetchall()

    print("\n--- TOP 5 EMPLOYEES BY ACHIEVEMENTS ---")

    if top_employees:
        for employee in top_employees:
            print(
                f"Employee ID: {employee[0]} | "
                f"Name: {employee[1]} | "
                f"Achievements: {employee[2]}"
            )
    else:
        print("No achievement records available.")

    # --------------------------------------
    # 6. EMPLOYEE CAREER DEVELOPMENT SUMMARY
    # --------------------------------------

    cursor.execute("""
        SELECT
            COUNT(DISTINCT employee_id)
        FROM (
            SELECT employee_id
            FROM performance_improvement_plans

            UNION

            SELECT employee_id
            FROM promotion_recommendations

            UNION

            SELECT employee_id
            FROM employee_achievements
        )
    """)

    employees_with_records = cursor.fetchone()[0]

    print("\n--- CAREER DEVELOPMENT SUMMARY ---")
    print("Employees with Career Records:", employees_with_records)

    print("\n" + "=" * 50)
    print("       END OF CAREER DASHBOARD")
    print("=" * 50)

    connection.close()


# ==========================================
# CAREER DEVELOPMENT REPORT MENU
# ==========================================

def career_development_reports_menu():

    while True:

        print("\n========== CAREER DEVELOPMENT REPORTS ==========")
        print("1. View Career Development Dashboard")
        print("2. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            career_development_dashboard()

        elif choice == "2":
            break

        else:
            print("Invalid choice!")
            

# ==========================================
# CAREER DEVELOPMENT CSV EXPORTS
# ==========================================

def export_query_to_csv(filename, query):

    os.makedirs("exports", exist_ok=True)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()
    headers = [column[0] for column in cursor.description]

    file_path = os.path.join("exports", filename)

    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    connection.close()

    print(f"\nReport exported successfully: {file_path}")
    print("Total records:", len(rows))


def export_improvement_plans():

    query = """
        SELECT
            p.id AS plan_id,
            p.employee_id,
            e.name AS employee_name,
            p.plan_title,
            p.identified_issues,
            p.improvement_goals,
            p.action_plan,
            p.start_date,
            p.end_date,
            p.review_date,
            p.status,
            p.outcome
        FROM performance_improvement_plans p
        JOIN employees e ON p.employee_id = e.id
        ORDER BY p.id DESC
    """

    export_query_to_csv(
        "improvement_plans.csv",
        query
    )


def export_promotion_recommendations():

    query = """
        SELECT
            p.id AS recommendation_id,
            p.employee_id,
            e.name AS employee_name,
            p.current_designation,
            p.recommended_designation,
            p.current_salary,
            p.proposed_salary,
            p.justification,
            p.recommended_by,
            p.recommendation_date,
            p.status,
            p.decision_comments
        FROM promotion_recommendations p
        JOIN employees e ON p.employee_id = e.id
        ORDER BY p.id DESC
    """

    export_query_to_csv(
        "promotion_recommendations.csv",
        query
    )


def export_employee_achievements():

    query = """
        SELECT
            a.id AS achievement_id,
            a.employee_id,
            e.name AS employee_name,
            a.achievement_title,
            a.category,
            a.description,
            a.achievement_date,
            a.awarded_by
        FROM employee_achievements a
        JOIN employees e ON a.employee_id = e.id
        ORDER BY a.achievement_date DESC
    """

    export_query_to_csv(
        "employee_achievements.csv",
        query
    )


def export_career_summary():

    query = """
        SELECT
            e.id AS employee_id,
            e.name AS employee_name,

            (
                SELECT COUNT(*)
                FROM performance_improvement_plans p
                WHERE p.employee_id = e.id
            ) AS total_improvement_plans,

            (
                SELECT COUNT(*)
                FROM promotion_recommendations r
                WHERE r.employee_id = e.id
                  AND r.status = 'Approved'
            ) AS approved_promotions,

            (
                SELECT COUNT(*)
                FROM employee_achievements a
                WHERE a.employee_id = e.id
            ) AS total_achievements

        FROM employees e
        ORDER BY e.id
    """

    export_query_to_csv(
        "career_development_summary.csv",
        query
    )


def export_all_career_reports():

    print("\n========== EXPORTING CAREER REPORTS ==========")

    export_improvement_plans()
    export_promotion_recommendations()
    export_employee_achievements()
    export_career_summary()

    print("\nAll career development reports exported!")
    print("Check the exports folder.")


def career_export_menu():

    while True:

        print("\n========== CAREER REPORT EXPORT ==========")
        print("1. Export Improvement Plans")
        print("2. Export Promotion Recommendations")
        print("3. Export Employee Achievements")
        print("4. Export Career Development Summary")
        print("5. Export All Reports")
        print("6. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            export_improvement_plans()

        elif choice == "2":
            export_promotion_recommendations()

        elif choice == "3":
            export_employee_achievements()

        elif choice == "4":
            export_career_summary()

        elif choice == "5":
            export_all_career_reports()

        elif choice == "6":
            break

        else:
            print("Invalid choice!")

def career_development_menu():

    create_career_development_tables()
    verify_career_development_tables()

    while True:
        print("\n========== CAREER DEVELOPMENT ==========")
        print("1. Performance Improvement Management")
        print("2. Promotion Recommendation Management")
        print("3. Employee Achievements & Recognition")
        print("4. Career Development Dashboard")
        print("5. Export Career Development Reports")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            performance_improvement_menu()

        elif choice == "2":
            promotion_management_menu()

        elif choice == "3":
            achievement_management_menu()

        elif choice == "4":
            career_development_reports_menu()

        elif choice == "5":
            career_export_menu()

        elif choice == "6":
            print("Returning to previous menu.")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    career_development_menu()
