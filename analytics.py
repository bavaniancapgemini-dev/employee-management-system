
# ==========================================
# EMPLOYEE MANAGEMENT SYSTEM
# V9.0 - ADVANCED HR ANALYTICS
# STAGE 1 - EMPLOYEE ANALYTICS
# ==========================================

import sqlite3

DATABASE_NAME = "employees.db"


def get_connection():

    return sqlite3.connect(DATABASE_NAME)


def check_employee_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'employees'
    """)

    result = cursor.fetchone()
    connection.close()

    return result is not None


# ==========================================
# 1. EMPLOYEE KPI DASHBOARD
# ==========================================

def employee_kpi_dashboard():

    if not check_employee_table():
        print("Employee table not found.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(salary), 0),
            COALESCE(AVG(salary), 0),
            COALESCE(MAX(salary), 0),
            COALESCE(MIN(salary), 0),
            COUNT(DISTINCT department)
        FROM employees
    """)

    result = cursor.fetchone()
    connection.close()

    total_employees = result[0]
    total_salary = result[1]
    average_salary = result[2]
    highest_salary = result[3]
    lowest_salary = result[4]
    total_departments = result[5]

    print("\n======================================")
    print("       EMPLOYEE ANALYTICS DASHBOARD")
    print("======================================")

    print(f"Total Employees       : {total_employees}")
    print(f"Total Salary Expense  : {total_salary:,.2f}")
    print(f"Average Salary        : {average_salary:,.2f}")
    print(f"Highest Salary        : {highest_salary:,.2f}")
    print(f"Lowest Salary         : {lowest_salary:,.2f}")
    print(f"Total Departments     : {total_departments}")

    print("======================================")


# ==========================================
# 2. DEPARTMENT-WISE ANALYTICS
# ==========================================

def department_analytics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            department,
            COUNT(*) AS employee_count,
            SUM(salary) AS total_salary,
            AVG(salary) AS average_salary,
            MAX(salary) AS highest_salary,
            AVG(rating) AS average_rating
        FROM employees
        GROUP BY department
        ORDER BY employee_count DESC
    """)

    departments = cursor.fetchall()
    connection.close()

    print("\n========== DEPARTMENT ANALYTICS ==========")

    if not departments:
        print("No department records found.")
        return

    for department in departments:

        print("\nDepartment:", department[0])
        print("Employee Count:", department[1])
        print("Total Salary:", f"{department[2] or 0:,.2f}")
        print("Average Salary:", f"{department[3] or 0:,.2f}")
        print("Highest Salary:", f"{department[4] or 0:,.2f}")
        print("Average Rating:", f"{department[5] or 0:.2f}")


# ==========================================
# 3. TOP 5 HIGHEST-PAID EMPLOYEES
# ==========================================

def top_salary_employees():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, department, salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 5
    """)

    employees = cursor.fetchall()
    connection.close()

    print("\n========== TOP 5 HIGHEST-PAID EMPLOYEES ==========")

    if not employees:
        print("No employees found.")
        return

    for employee in employees:

        print("\nEmployee ID:", employee[0])
        print("Name:", employee[1])
        print("Department:", employee[2])
        print("Salary:", f"{employee[3]:,.2f}")


# ==========================================
# 4. TOP 5 PERFORMERS
# ==========================================

def top_performing_employees():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, department, rating
        FROM employees
        WHERE rating IS NOT NULL
        ORDER BY rating DESC, name ASC
        LIMIT 5
    """)

    employees = cursor.fetchall()
    connection.close()

    print("\n========== TOP 5 PERFORMERS ==========")

    if not employees:
        print("No performance ratings found.")
        return

    for employee in employees:

        print("\nEmployee ID:", employee[0])
        print("Name:", employee[1])
        print("Department:", employee[2])
        print("Rating:", employee[3], "/ 10")


# ==========================================
# 5. EMPLOYEE RATING DISTRIBUTION
# ==========================================

def employee_rating_analysis():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT rating, COUNT(*)
        FROM employees
        WHERE rating IS NOT NULL
        GROUP BY rating
        ORDER BY rating DESC
    """)

    ratings = cursor.fetchall()
    connection.close()

    print("\n========== EMPLOYEE RATING ANALYSIS ==========")

    if not ratings:
        print("No employee ratings available.")
        return

    for rating, count in ratings:

        print(f"Rating {rating}/10 : {count} employee(s)")


# ==========================================
# 6. EMPLOYEE ANALYTICS MENU
# ==========================================

def employee_analytics_menu():

    while True:

        print("\n======================================")
        print("        EMPLOYEE ANALYTICS")
        print("======================================")
        print("1. Employee KPI Dashboard")
        print("2. Department Analytics")
        print("3. Top 5 Highest-Paid Employees")
        print("4. Top 5 Performers")
        print("5. Employee Rating Analysis")
        print("6. Back")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":

            employee_kpi_dashboard()

        elif choice == "2":

            department_analytics()

        elif choice == "3":

            top_salary_employees()

        elif choice == "4":

            top_performing_employees()

        elif choice == "5":

            employee_rating_analysis()

        elif choice == "6":

            print("Returning to previous menu...")
            break

        else:

            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    employee_analytics_menu()


# ==========================================
# V9.0 STAGE 2 - RECRUITMENT ANALYTICS
# ==========================================


# ==========================================
# 1. RECRUITMENT KPI DASHBOARD
# ==========================================

def recruitment_kpi_dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*),
               COALESCE(SUM(vacancies), 0)
        FROM job_openings
        WHERE status = 'Open'
    """)

    open_jobs, open_vacancies = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM candidates")
    total_candidates = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM job_applications")
    total_applications = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM job_applications
        WHERE status = 'Hired'
    """)

    hired_candidates = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM recruitment_offers
        WHERE status = 'Accepted'
    """)

    accepted_offers = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM recruitment_offers
        WHERE status = 'Declined'
    """)

    declined_offers = cursor.fetchone()[0]

    connection.close()

    hiring_rate = (
        hired_candidates / total_applications * 100
        if total_applications > 0 else 0
    )

    print("\n======================================")
    print("       RECRUITMENT KPI DASHBOARD")
    print("======================================")

    print("Open Job Openings       :", open_jobs)
    print("Open Vacancies           :", open_vacancies)
    print("Registered Candidates    :", total_candidates)
    print("Total Applications       :", total_applications)
    print("Hired Candidates         :", hired_candidates)
    print("Accepted Offers          :", accepted_offers)
    print("Declined Offers          :", declined_offers)

    print(f"Hiring Conversion Rate   : {hiring_rate:.2f}%")

    print("======================================")


# ==========================================
# 2. APPLICATION STATUS REPORT
# ==========================================

def application_status_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM job_applications
        GROUP BY status
        ORDER BY COUNT(*) DESC
    """)

    results = cursor.fetchall()
    connection.close()

    print("\n========== APPLICATION STATUS REPORT ==========")

    if not results:
        print("No applications found.")
        return

    for status, count in results:

        print(f"{status:<25}: {count}")


# ==========================================
# 3. INTERVIEW OUTCOME REPORT
# ==========================================

def interview_outcome_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT result, COUNT(*)
        FROM interviews
        GROUP BY result
        ORDER BY COUNT(*) DESC
    """)

    results = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM interviews")
    total_interviews = cursor.fetchone()[0]

    connection.close()

    print("\n========== INTERVIEW OUTCOME REPORT ==========")

    print("Total Interviews:", total_interviews)

    if not results:
        print("No interview records found.")
        return

    for result, count in results:

        percentage = (
            count / total_interviews * 100
            if total_interviews else 0
        )

        print(
            f"{result:<20}: {count} "
            f"({percentage:.2f}%)"
        )


# ==========================================
# 4. OFFER ANALYTICS
# ==========================================

def offer_analytics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*), COALESCE(SUM(offered_salary), 0)
        FROM recruitment_offers
        GROUP BY status
        ORDER BY COUNT(*) DESC
    """)

    results = cursor.fetchall()

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(AVG(offered_salary), 0),
            COALESCE(MAX(offered_salary), 0),
            COALESCE(MIN(offered_salary), 0)
        FROM recruitment_offers
    """)

    summary = cursor.fetchone()
    connection.close()

    print("\n========== OFFER ANALYTICS ==========")

    print("Total Offers:", summary[0])
    print(f"Average Offered Salary: {summary[1]:,.2f}")
    print(f"Highest Offered Salary: {summary[2]:,.2f}")
    print(f"Lowest Offered Salary: {summary[3]:,.2f}")

    if not results:
        print("\nNo offers found.")
        return

    print("\nOffer Status Breakdown:")

    for status, count, salary in results:

        print(f"\nStatus: {status}")
        print("Number of Offers:", count)
        print(f"Total Offered Salary: {salary:,.2f}")


# ==========================================
# 5. JOB-WISE RECRUITMENT PERFORMANCE
# ==========================================

def job_wise_recruitment_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            j.id,
            j.job_title,
            j.department,
            j.vacancies,
            j.status,
            COUNT(DISTINCT a.id) AS applications,
            COUNT(DISTINCT CASE
                WHEN a.status = 'Hired' THEN a.id
            END) AS hired
        FROM job_openings j
        LEFT JOIN job_applications a
            ON j.id = a.job_id
        GROUP BY
            j.id,
            j.job_title,
            j.department,
            j.vacancies,
            j.status
        ORDER BY applications DESC
    """)

    results = cursor.fetchall()
    connection.close()

    print("\n========== JOB-WISE RECRUITMENT REPORT ==========")

    if not results:
        print("No job openings found.")
        return

    for job in results:

        print("\nJob ID:", job[0])
        print("Job Title:", job[1])
        print("Department:", job[2])
        print("Vacancies:", job[3])
        print("Job Status:", job[4])
        print("Applications Received:", job[5])
        print("Candidates Hired:", job[6])


# ==========================================
# 6. RECRUITMENT ANALYTICS MENU
# ==========================================

def recruitment_analytics_menu():

    while True:

        print("\n======================================")
        print("        RECRUITMENT ANALYTICS")
        print("======================================")
        print("1. Recruitment KPI Dashboard")
        print("2. Application Status Report")
        print("3. Interview Outcome Report")
        print("4. Offer Analytics")
        print("5. Job-Wise Recruitment Report")
        print("6. Back")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":

            recruitment_kpi_dashboard()

        elif choice == "2":

            application_status_report()

        elif choice == "3":

            interview_outcome_report()

        elif choice == "4":

            offer_analytics()

        elif choice == "5":

            job_wise_recruitment_report()

        elif choice == "6":

            print("Returning to previous menu...")
            break

        else:

            print("Invalid choice. Please try again.")


# ==========================================
# V9.0 - STAGE 3
# ATTENDANCE & LEAVE ANALYTICS
# ==========================================

def attendance_kpi_dashboard():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== ATTENDANCE KPI DASHBOARD ==========")

    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_records = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT employee_id)
        FROM attendance
    """)
    employees_marked = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE status = 'Present'
    """)
    present_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE status = 'Absent'
    """)
    absent_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE status = 'Late'
    """)
    late_count = cursor.fetchone()[0]

    attendance_rate = (
        present_count / total_records * 100
        if total_records else 0
    )

    print("Total Attendance Records:", total_records)
    print("Employees with Attendance:", employees_marked)
    print("Present Records:", present_count)
    print("Absent Records:", absent_count)
    print("Late Records:", late_count)
    print(f"Present Rate: {attendance_rate:.2f}%")

    connection.close()


def attendance_status_report():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== ATTENDANCE STATUS REPORT ==========")

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM attendance
        GROUP BY status
        ORDER BY COUNT(*) DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No attendance records found.")
    else:
        for status, count in records:
            print(f"{status}: {count}")

    connection.close()


def employee_attendance_analytics():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== EMPLOYEE ATTENDANCE ANALYTICS ==========")

    cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.department,
            COUNT(a.id) AS total_days,
            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END),
            SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END),
            SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END)
        FROM employees e
        LEFT JOIN attendance a
            ON e.id = a.employee_id
        GROUP BY e.id, e.name, e.department
        ORDER BY total_days DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No employee records found.")
    else:
        for record in records:
            employee_id, name, department, total, present, absent, late = record

            print("\nEmployee ID:", employee_id)
            print("Name:", name)
            print("Department:", department)
            print("Total Records:", total)
            print("Present:", present or 0)
            print("Absent:", absent or 0)
            print("Late:", late or 0)

            rate = (present or 0) / total * 100 if total else 0
            print(f"Attendance Rate: {rate:.2f}%")

    connection.close()


def daily_attendance_trend():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== DAILY ATTENDANCE TREND ==========")

    cursor.execute("""
        SELECT
            DATE(attendance_date),
            COUNT(*),
            SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END)
        FROM attendance
        GROUP BY DATE(attendance_date)
        ORDER BY DATE(attendance_date) DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No attendance data available.")
    else:
        for record in records:
            print("\nDate:", record[0])
            print("Total:", record[1])
            print("Present:", record[2] or 0)
            print("Absent:", record[3] or 0)
            print("Late:", record[4] or 0)

    connection.close()


def leave_kpi_dashboard():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== LEAVE KPI DASHBOARD ==========")

    cursor.execute("SELECT COUNT(*) FROM leave_requests")
    total_requests = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_requests
        WHERE status = 'Pending'
    """)
    pending = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_requests
        WHERE status = 'Approved'
    """)
    approved = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_requests
        WHERE status = 'Rejected'
    """)
    rejected = cursor.fetchone()[0]

    approval_rate = (
        approved / total_requests * 100
        if total_requests else 0
    )

    print("Total Leave Requests:", total_requests)
    print("Pending Requests:", pending)
    print("Approved Requests:", approved)
    print("Rejected Requests:", rejected)
    print(f"Approval Rate: {approval_rate:.2f}%")

    connection.close()


def leave_type_report():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== LEAVE TYPE REPORT ==========")

    cursor.execute("""
        SELECT
            leave_type,
            COUNT(*),
            SUM(
                CASE
                    WHEN julianday(end_date) >= julianday(start_date)
                    THEN CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1
                    ELSE 0
                END
            )
        FROM leave_requests
        GROUP BY leave_type
        ORDER BY COUNT(*) DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No leave requests found.")
    else:
        for leave_type, requests, days in records:
            print("\nLeave Type:", leave_type)
            print("Total Requests:", requests)
            print("Total Requested Days:", days or 0)

    connection.close()


def employee_leave_analytics():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== EMPLOYEE LEAVE ANALYTICS ==========")

    cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.department,
            COUNT(l.id),
            SUM(CASE WHEN l.status = 'Approved' THEN 1 ELSE 0 END),
            SUM(CASE WHEN l.status = 'Pending' THEN 1 ELSE 0 END),
            SUM(CASE WHEN l.status = 'Rejected' THEN 1 ELSE 0 END)
        FROM employees e
        LEFT JOIN leave_requests l
            ON e.id = l.employee_id
        GROUP BY e.id, e.name, e.department
        ORDER BY COUNT(l.id) DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No employee records found.")
    else:
        for record in records:
            employee_id, name, department, total, approved, pending, rejected = record

            print("\nEmployee ID:", employee_id)
            print("Name:", name)
            print("Department:", department)
            print("Total Requests:", total)
            print("Approved:", approved or 0)
            print("Pending:", pending or 0)
            print("Rejected:", rejected or 0)

    connection.close()


def attendance_leave_analytics_menu():

    while True:
        print("\n========================================")
        print("   ATTENDANCE & LEAVE ANALYTICS")
        print("========================================")
        print("1. Attendance KPI Dashboard")
        print("2. Attendance Status Report")
        print("3. Employee Attendance Analytics")
        print("4. Daily Attendance Trend")
        print("5. Leave KPI Dashboard")
        print("6. Leave Type Report")
        print("7. Employee Leave Analytics")
        print("8. Back")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            attendance_kpi_dashboard()

        elif choice == "2":
            attendance_status_report()

        elif choice == "3":
            employee_attendance_analytics()

        elif choice == "4":
            daily_attendance_trend()

        elif choice == "5":
            leave_kpi_dashboard()

        elif choice == "6":
            leave_type_report()

        elif choice == "7":
            employee_leave_analytics()

        elif choice == "8":
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================
# V9.0 - STAGE 4
# PAYROLL COST ANALYSIS
# ==========================================

def payroll_kpi_dashboard():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== PAYROLL KPI DASHBOARD ==========")

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(gross_salary), 0),
            COALESCE(SUM(net_salary), 0),
            COALESCE(AVG(net_salary), 0),
            COALESCE(MAX(net_salary), 0),
            COALESCE(MIN(net_salary), 0)
        FROM payroll
    """)

    total_records, gross_cost, net_cost, avg_salary, highest, lowest = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*)
        FROM payroll
        WHERE payment_status = 'Paid'
    """)
    paid = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM payroll
        WHERE payment_status = 'Pending'
    """)
    pending = cursor.fetchone()[0]

    print("Total Payroll Records:", total_records)
    print(f"Total Gross Payroll Cost: {gross_cost:,.2f}")
    print(f"Total Net Payroll Cost: {net_cost:,.2f}")
    print(f"Average Net Salary: {avg_salary:,.2f}")
    print(f"Highest Net Salary: {highest:,.2f}")
    print(f"Lowest Net Salary: {lowest:,.2f}")
    print("Paid Payroll Records:", paid)
    print("Pending Payroll Records:", pending)

    connection.close()


def monthly_payroll_report():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== MONTHLY PAYROLL REPORT ==========")

    cursor.execute("""
        SELECT
            month,
            year,
            COUNT(*),
            SUM(gross_salary),
            SUM(net_salary)
        FROM payroll
        GROUP BY year, month
        ORDER BY year DESC, month DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No payroll records found.")
    else:
        for record in records:
            month, year, count, gross, net = record

            print(f"\nPeriod: {month} {year}")
            print("Employees Processed:", count)
            print(f"Gross Payroll: {gross or 0:,.2f}")
            print(f"Net Payroll: {net or 0:,.2f}")

    connection.close()


def yearly_payroll_report():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== YEARLY PAYROLL REPORT ==========")

    cursor.execute("""
        SELECT
            year,
            COUNT(*),
            SUM(gross_salary),
            SUM(net_salary),
            AVG(net_salary)
        FROM payroll
        GROUP BY year
        ORDER BY year DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No payroll records found.")
    else:
        for year, count, gross, net, average in records:
            print(f"\nYear: {year}")
            print("Payroll Records:", count)
            print(f"Gross Payroll Cost: {gross or 0:,.2f}")
            print(f"Net Payroll Cost: {net or 0:,.2f}")
            print(f"Average Net Salary: {average or 0:,.2f}")

    connection.close()


def department_payroll_report():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== DEPARTMENT PAYROLL REPORT ==========")

    cursor.execute("""
        SELECT
            e.department,
            COUNT(p.id),
            SUM(p.gross_salary),
            SUM(p.net_salary),
            AVG(p.net_salary)
        FROM payroll p
        JOIN employees e
            ON p.employee_id = e.id
        GROUP BY e.department
        ORDER BY SUM(p.net_salary) DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No department payroll data found.")
    else:
        for department, count, gross, net, average in records:
            print("\nDepartment:", department)
            print("Payroll Records:", count)
            print(f"Gross Payroll: {gross or 0:,.2f}")
            print(f"Net Payroll: {net or 0:,.2f}")
            print(f"Average Net Salary: {average or 0:,.2f}")

    connection.close()


def payroll_payment_status_report():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== PAYROLL PAYMENT STATUS ==========")

    cursor.execute("""
        SELECT
            payment_status,
            COUNT(*),
            SUM(net_salary)
        FROM payroll
        GROUP BY payment_status
        ORDER BY COUNT(*) DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No payroll records found.")
    else:
        for status, count, amount in records:
            print("\nPayment Status:", status)
            print("Number of Records:", count)
            print(f"Total Net Salary: {amount or 0:,.2f}")

    connection.close()


def salary_component_analysis():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== SALARY COMPONENT ANALYSIS ==========")

    cursor.execute("""
        SELECT
            COALESCE(SUM(basic_salary), 0),
            COALESCE(SUM(HRA), 0),
            COALESCE(SUM(allowances), 0),
            COALESCE(SUM(overtime), 0),
            COALESCE(SUM(tax), 0),
            COALESCE(SUM(PF), 0),
            COALESCE(SUM(other_deductions), 0),
            COALESCE(SUM(gross_salary), 0),
            COALESCE(SUM(net_salary), 0)
        FROM payroll
    """)

    values = cursor.fetchone()

    components = [
        ("Basic Salary", values[0]),
        ("HRA", values[1]),
        ("Allowances", values[2]),
        ("Overtime", values[3]),
        ("Tax", values[4]),
        ("PF", values[5]),
        ("Other Deductions", values[6]),
        ("Gross Salary", values[7]),
        ("Net Salary", values[8])
    ]

    if not any(values):
        print("No payroll data available.")
    else:
        for name, amount in components:
            print(f"{name}: {amount:,.2f}")

    connection.close()


def highest_payroll_employees():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== HIGHEST PAYROLL EMPLOYEES ==========")

    cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.department,
            COUNT(p.id),
            SUM(p.net_salary),
            AVG(p.net_salary)
        FROM employees e
        JOIN payroll p
            ON e.id = p.employee_id
        GROUP BY e.id, e.name, e.department
        ORDER BY SUM(p.net_salary) DESC
        LIMIT 10
    """)

    records = cursor.fetchall()

    if not records:
        print("No payroll records found.")
    else:
        for record in records:
            employee_id, name, department, count, total, average = record

            print("\nEmployee ID:", employee_id)
            print("Name:", name)
            print("Department:", department)
            print("Payroll Records:", count)
            print(f"Total Net Payroll: {total or 0:,.2f}")
            print(f"Average Net Salary: {average or 0:,.2f}")

    connection.close()


def payroll_analytics_menu():

    while True:
        print("\n========================================")
        print("       PAYROLL COST ANALYSIS")
        print("========================================")
        print("1. Payroll KPI Dashboard")
        print("2. Monthly Payroll Report")
        print("3. Yearly Payroll Report")
        print("4. Department Payroll Report")
        print("5. Payment Status Report")
        print("6. Salary Component Analysis")
        print("7. Highest Payroll Employees")
        print("8. Back")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            payroll_kpi_dashboard()

        elif choice == "2":
            monthly_payroll_report()

        elif choice == "3":
            yearly_payroll_report()

        elif choice == "4":
            department_payroll_report()

        elif choice == "5":
            payroll_payment_status_report()

        elif choice == "6":
            salary_component_analysis()

        elif choice == "7":
            highest_payroll_employees()

        elif choice == "8":
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================
# V9.0 - STAGE 5
# TRAINING & PERFORMANCE ANALYTICS
# ==========================================


# ==========================================
# TRAINING ANALYTICS
# ==========================================

def training_kpi_dashboard():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== TRAINING KPI DASHBOARD ==========")

    cursor.execute("SELECT COUNT(*) FROM training_courses")
    total_courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM training_enrollments")
    total_enrollments = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM training_enrollments
        WHERE status = 'Completed'
    """)
    completed = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM training_enrollments
        WHERE status = 'In Progress'
    """)
    in_progress = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM training_enrollments
        WHERE status = 'Not Started'
    """)
    not_started = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM training_enrollments
        WHERE certificate_name IS NOT NULL
          AND TRIM(certificate_name) != ''
    """)
    certificates = cursor.fetchone()[0]

    cursor.execute("""
        SELECT AVG(assessment_score)
        FROM training_enrollments
        WHERE assessment_score IS NOT NULL
    """)
    average_score = cursor.fetchone()[0] or 0

    completion_rate = (
        completed / total_enrollments * 100
        if total_enrollments else 0
    )

    print("Total Courses:", total_courses)
    print("Total Enrollments:", total_enrollments)
    print("Completed Trainings:", completed)
    print("In Progress:", in_progress)
    print("Not Started:", not_started)
    print("Certificates Awarded:", certificates)
    print(f"Average Assessment Score: {average_score:.2f}")
    print(f"Training Completion Rate: {completion_rate:.2f}%")

    connection.close()


def course_wise_training_report():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== COURSE-WISE TRAINING REPORT ==========")

    cursor.execute("""
        SELECT
            c.course_name,
            COUNT(e.id),
            SUM(CASE WHEN e.status = 'Completed' THEN 1 ELSE 0 END),
            SUM(CASE WHEN e.status = 'In Progress' THEN 1 ELSE 0 END),
            SUM(CASE WHEN e.status = 'Not Started' THEN 1 ELSE 0 END),
            AVG(e.assessment_score)
        FROM training_courses c
        LEFT JOIN training_enrollments e
            ON c.id = e.course_id
        GROUP BY c.id, c.course_name
        ORDER BY COUNT(e.id) DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No training courses found.")
    else:
        for record in records:
            course, total, completed, progress, not_started, average = record

            print("\nCourse:", course)
            print("Total Enrollments:", total)
            print("Completed:", completed or 0)
            print("In Progress:", progress or 0)
            print("Not Started:", not_started or 0)
            print(f"Average Score: {average or 0:.2f}")

    connection.close()


def department_training_report():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== DEPARTMENT TRAINING REPORT ==========")

    cursor.execute("""
        SELECT
            emp.department,
            COUNT(te.id),
            SUM(CASE WHEN te.status = 'Completed' THEN 1 ELSE 0 END),
            COUNT(DISTINCT te.employee_id),
            AVG(te.assessment_score)
        FROM employees emp
        LEFT JOIN training_enrollments te
            ON emp.id = te.employee_id
        GROUP BY emp.department
        ORDER BY COUNT(te.id) DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No department records found.")
    else:
        for department, total, completed, employees, average in records:
            rate = completed / total * 100 if total else 0

            print("\nDepartment:", department)
            print("Total Enrollments:", total)
            print("Completed Trainings:", completed or 0)
            print("Employees Enrolled:", employees)
            print(f"Completion Rate: {rate:.2f}%")
            print(f"Average Assessment Score: {average or 0:.2f}")

    connection.close()


def training_assessment_analysis():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== TRAINING ASSESSMENT ANALYSIS ==========")

    cursor.execute("""
        SELECT
            COUNT(assessment_score),
            AVG(assessment_score),
            MAX(assessment_score),
            MIN(assessment_score)
        FROM training_enrollments
        WHERE assessment_score IS NOT NULL
    """)

    total, average, highest, lowest = cursor.fetchone()

    print("Assessments Recorded:", total)

    if total:
        print(f"Average Score: {average:.2f}")
        print(f"Highest Score: {highest:.2f}")
        print(f"Lowest Score: {lowest:.2f}")
    else:
        print("No assessment scores available.")

    cursor.execute("""
        SELECT
            CASE
                WHEN assessment_score >= 90 THEN '90-100'
                WHEN assessment_score >= 80 THEN '80-89'
                WHEN assessment_score >= 70 THEN '70-79'
                WHEN assessment_score >= 60 THEN '60-69'
                ELSE 'Below 60'
            END AS score_range,
            COUNT(*)
        FROM training_enrollments
        WHERE assessment_score IS NOT NULL
        GROUP BY score_range
        ORDER BY MIN(assessment_score) DESC
    """)

    print("\nScore Distribution:")

    for score_range, count in cursor.fetchall():
        print(f"{score_range}: {count}")

    connection.close()


# ==========================================
# PERFORMANCE ANALYTICS
# ==========================================

def performance_kpi_dashboard():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== PERFORMANCE KPI DASHBOARD ==========")

    cursor.execute("""
        SELECT
            COUNT(*),
            AVG(rating),
            MAX(rating),
            MIN(rating),
            COUNT(DISTINCT employee_id)
        FROM performance_reviews
    """)

    total, average, highest, lowest, employees = cursor.fetchone()

    print("Total Performance Reviews:", total)
    print("Employees Reviewed:", employees)

    if total:
        print(f"Average Performance Rating: {average:.2f}/10")
        print(f"Highest Rating: {highest}/10")
        print(f"Lowest Rating: {lowest}/10")
    else:
        print("No performance reviews available.")

    connection.close()


def department_performance_analytics():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== DEPARTMENT PERFORMANCE ANALYTICS ==========")

    cursor.execute("""
        SELECT
            e.department,
            COUNT(pr.id),
            COUNT(DISTINCT pr.employee_id),
            AVG(pr.rating),
            MAX(pr.rating),
            MIN(pr.rating)
        FROM employees e
        LEFT JOIN performance_reviews pr
            ON e.id = pr.employee_id
        GROUP BY e.department
        ORDER BY AVG(pr.rating) DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No department records found.")
    else:
        for record in records:
            department, reviews, employees, average, highest, lowest = record

            print("\nDepartment:", department)
            print("Total Reviews:", reviews)
            print("Employees Reviewed:", employees)

            if reviews:
                print(f"Average Rating: {average:.2f}/10")
                print("Highest Rating:", highest)
                print("Lowest Rating:", lowest)
            else:
                print("No performance reviews available.")

    connection.close()


def top_performance_employees():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== TOP PERFORMANCE EMPLOYEES ==========")

    cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.department,
            COUNT(pr.id),
            AVG(pr.rating)
        FROM employees e
        JOIN performance_reviews pr
            ON e.id = pr.employee_id
        GROUP BY e.id, e.name, e.department
        ORDER BY AVG(pr.rating) DESC
        LIMIT 10
    """)

    records = cursor.fetchall()

    if not records:
        print("No performance reviews found.")
    else:
        for record in records:
            employee_id, name, department, reviews, average = record

            print("\nEmployee ID:", employee_id)
            print("Name:", name)
            print("Department:", department)
            print("Total Reviews:", reviews)
            print(f"Average Rating: {average:.2f}/10")

    connection.close()


def performance_rating_distribution():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== PERFORMANCE RATING DISTRIBUTION ==========")

    cursor.execute("""
        SELECT rating, COUNT(*)
        FROM performance_reviews
        GROUP BY rating
        ORDER BY rating DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No performance ratings available.")
    else:
        for rating, count in records:
            print(f"Rating {rating}/10: {count} review(s)")

    connection.close()


def review_period_report():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== REVIEW PERIOD REPORT ==========")

    cursor.execute("""
        SELECT
            review_period,
            COUNT(*),
            AVG(rating),
            MAX(rating),
            MIN(rating)
        FROM performance_reviews
        GROUP BY review_period
        ORDER BY review_period DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No review period data found.")
    else:
        for period, total, average, highest, lowest in records:
            print("\nReview Period:", period)
            print("Total Reviews:", total)
            print(f"Average Rating: {average:.2f}/10")
            print("Highest Rating:", highest)
            print("Lowest Rating:", lowest)

    connection.close()


# ==========================================
# TRAINING & PERFORMANCE ANALYTICS MENU
# ==========================================

def training_performance_analytics_menu():

    while True:
        print("\n========================================")
        print("   TRAINING & PERFORMANCE ANALYTICS")
        print("========================================")
        print("1. Training KPI Dashboard")
        print("2. Course-Wise Training Report")
        print("3. Department Training Report")
        print("4. Training Assessment Analysis")
        print("5. Performance KPI Dashboard")
        print("6. Department Performance Analytics")
        print("7. Top Performance Employees")
        print("8. Performance Rating Distribution")
        print("9. Review Period Report")
        print("10. Back")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            training_kpi_dashboard()

        elif choice == "2":
            course_wise_training_report()

        elif choice == "3":
            department_training_report()

        elif choice == "4":
            training_assessment_analysis()

        elif choice == "5":
            performance_kpi_dashboard()

        elif choice == "6":
            department_performance_analytics()

        elif choice == "7":
            top_performance_employees()

        elif choice == "8":
            performance_rating_distribution()

        elif choice == "9":
            review_period_report()

        elif choice == "10":
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================
# V9.0 - STAGE 6
# ADVANCED REPORTS & CSV EXPORTS
# ==========================================


def executive_analytics_dashboard():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========================================")
    print("       EXECUTIVE HR ANALYTICS")
    print("========================================")

    # Employee KPIs
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(salary), 0)
        FROM employees
    """)
    salary_expense = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT department)
        FROM employees
    """)
    departments = cursor.fetchone()[0]

    # Recruitment KPIs
    cursor.execute("""
        SELECT COUNT(*)
        FROM job_openings
        WHERE status = 'Open'
    """)
    open_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM candidates")
    candidates = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM job_applications")
    applications = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM job_applications
        WHERE status = 'Hired'
    """)
    hired = cursor.fetchone()[0]

    # Attendance KPIs
    cursor.execute("SELECT COUNT(*) FROM attendance")
    attendance_records = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE status = 'Present'
    """)
    present = cursor.fetchone()[0]

    attendance_rate = (
        present / attendance_records * 100
        if attendance_records else 0
    )

    # Leave KPIs
    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_requests
        WHERE status = 'Pending'
    """)
    pending_leaves = cursor.fetchone()[0]

    # Payroll KPIs
    cursor.execute("""
        SELECT COALESCE(SUM(net_salary), 0)
        FROM payroll
    """)
    payroll_cost = cursor.fetchone()[0]

    # Training KPIs
    cursor.execute("SELECT COUNT(*) FROM training_enrollments")
    enrollments = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM training_enrollments
        WHERE status = 'Completed'
    """)
    completed_training = cursor.fetchone()[0]

    training_rate = (
        completed_training / enrollments * 100
        if enrollments else 0
    )

    # Performance KPIs
    cursor.execute("""
        SELECT AVG(rating)
        FROM performance_reviews
    """)
    average_rating = cursor.fetchone()[0] or 0

    print("\n--- EMPLOYEE OVERVIEW ---")
    print("Total Employees:", total_employees)
    print("Departments:", departments)
    print(f"Employee Salary Expense: {salary_expense:,.2f}")

    print("\n--- RECRUITMENT OVERVIEW ---")
    print("Open Job Positions:", open_jobs)
    print("Registered Candidates:", candidates)
    print("Total Applications:", applications)
    print("Hired Applications:", hired)

    print("\n--- ATTENDANCE OVERVIEW ---")
    print("Attendance Records:", attendance_records)
    print(f"Present Rate: {attendance_rate:.2f}%")

    print("\n--- LEAVE OVERVIEW ---")
    print("Pending Leave Requests:", pending_leaves)

    print("\n--- PAYROLL OVERVIEW ---")
    print(f"Total Net Payroll Cost: {payroll_cost:,.2f}")

    print("\n--- TRAINING OVERVIEW ---")
    print("Total Enrollments:", enrollments)
    print("Completed Trainings:", completed_training)
    print(f"Training Completion Rate: {training_rate:.2f}%")

    print("\n--- PERFORMANCE OVERVIEW ---")
    print(f"Average Performance Rating: {average_rating:.2f}/10")

    print("\n========================================")

    connection.close()


# ==========================================
# CSV EXPORT FUNCTIONS
# ==========================================

def export_analytics_report(report_name):

    import csv
    import os

    reports = {

        "employees": (
            "employee_analytics.csv",
            """
            SELECT
                id,
                name,
                department,
                salary,
                rating
            FROM employees
            ORDER BY id
            """
        ),

        "recruitment": (
            "recruitment_analytics.csv",
            """
            SELECT
                j.job_title,
                j.department,
                j.status AS job_status,
                c.candidate_name,
                c.email,
                a.status AS application_status,
                a.applied_on
            FROM job_applications a
            JOIN candidates c
                ON a.candidate_id = c.id
            JOIN job_openings j
                ON a.job_id = j.id
            ORDER BY a.applied_on DESC
            """
        ),

        "attendance": (
            "attendance_analytics.csv",
            """
            SELECT
                e.id AS employee_id,
                e.name,
                e.department,
                a.attendance_date,
                a.status
            FROM attendance a
            JOIN employees e
                ON a.employee_id = e.id
            ORDER BY a.attendance_date DESC
            """
        ),

        "leave": (
            "leave_analytics.csv",
            """
            SELECT
                e.id AS employee_id,
                e.name,
                e.department,
                l.leave_type,
                l.start_date,
                l.end_date,
                l.reason,
                l.status,
                l.applied_on
            FROM leave_requests l
            JOIN employees e
                ON l.employee_id = e.id
            ORDER BY l.applied_on DESC
            """
        ),

        "payroll": (
            "payroll_analytics.csv",
            """
            SELECT
                e.id AS employee_id,
                e.name,
                e.department,
                p.month,
                p.year,
                p.basic_salary,
                p.HRA,
                p.allowances,
                p.overtime,
                p.tax,
                p.PF,
                p.other_deductions,
                p.gross_salary,
                p.net_salary,
                p.payment_status
            FROM payroll p
            JOIN employees e
                ON p.employee_id = e.id
            ORDER BY p.year DESC, p.month DESC
            """
        ),

        "training": (
            "training_analytics.csv",
            """
            SELECT
                e.id AS employee_id,
                e.name,
                e.department,
                c.course_name,
                te.status,
                te.assessment_score,
                te.certificate_name,
                te.enrolled_on,
                te.completed_on
            FROM training_enrollments te
            JOIN employees e
                ON te.employee_id = e.id
            JOIN training_courses c
                ON te.course_id = c.id
            ORDER BY te.enrolled_on DESC
            """
        ),

        "performance": (
            "performance_analytics.csv",
            """
            SELECT
                e.id AS employee_id,
                e.name,
                e.department,
                pr.review_period,
                pr.reviewer,
                pr.rating,
                pr.strengths,
                pr.areas_to_improve,
                pr.comments,
                pr.review_date
            FROM performance_reviews pr
            JOIN employees e
                ON pr.employee_id = e.id
            ORDER BY pr.review_date DESC
            """
        )
    }

    if report_name not in reports:
        print("Invalid report name.")
        return

    filename, query = reports[report_name]

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        records = cursor.fetchall()

        headers = [column[0] for column in cursor.description]

        os.makedirs("exports/analytics", exist_ok=True)

        filepath = os.path.join("exports", "analytics", filename)

        with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(records)

        print("\nReport exported successfully!")
        print("Report:", filename)
        print("Records exported:", len(records))
        print("Location:", os.path.abspath(filepath))

    except sqlite3.Error as error:
        print("Database error:", error)

    except OSError as error:
        print("File error:", error)

    finally:
        connection.close()


def export_all_analytics_reports():

    print("\n========== EXPORT ALL ANALYTICS REPORTS ==========")

    report_names = [
        "employees",
        "recruitment",
        "attendance",
        "leave",
        "payroll",
        "training",
        "performance"
    ]

    for report in report_names:
        print("\nExporting:", report.upper())
        export_analytics_report(report)

    print("\nAll export attempts completed.")
    print("Check the exports/analytics folder.")


def analytics_export_menu():

    while True:
        print("\n========================================")
        print("       ANALYTICS EXPORT CENTER")
        print("========================================")
        print("1. Export Employee Report")
        print("2. Export Recruitment Report")
        print("3. Export Attendance Report")
        print("4. Export Leave Report")
        print("5. Export Payroll Report")
        print("6. Export Training Report")
        print("7. Export Performance Report")
        print("8. Export All Reports")
        print("9. Back")

        choice = input("\nChoose an option: ").strip()

        export_options = {
            "1": "employees",
            "2": "recruitment",
            "3": "attendance",
            "4": "leave",
            "5": "payroll",
            "6": "training",
            "7": "performance"
        }

        if choice in export_options:
            export_analytics_report(export_options[choice])

        elif choice == "8":
            export_all_analytics_reports()

        elif choice == "9":
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================
# UNIFIED ANALYTICS CENTER
# ==========================================

def analytics_center_menu():

    while True:
        print("\n========================================")
        print("          ANALYTICS CENTER")
        print("========================================")
        print("1. Executive HR Dashboard")
        print("2. Employee Analytics")
        print("3. Recruitment Analytics")
        print("4. Attendance & Leave Analytics")
        print("5. Payroll Cost Analysis")
        print("6. Training & Performance Analytics")
        print("7. Export Analytics Reports")
        print("8. Exit Analytics Center")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            executive_analytics_dashboard()

        elif choice == "2":
            employee_analytics_menu()

        elif choice == "3":
            recruitment_analytics_menu()

        elif choice == "4":
            attendance_leave_analytics_menu()

        elif choice == "5":
            payroll_analytics_menu()

        elif choice == "6":
            training_performance_analytics_menu()

        elif choice == "7":
            analytics_export_menu()

        elif choice == "8":
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================
# V9.0 - STAGE 6
# ADVANCED REPORTS & CSV EXPORTS
# ==========================================

def export_analytics_report(report_key):

    import csv
    import os

    reports = {
        "employees": {
            "filename": "employee_analytics.csv",
            "query": """
                SELECT
                    department,
                    COUNT(*) AS total_employees,
                    SUM(salary) AS total_salary,
                    AVG(salary) AS average_salary,
                    AVG(rating) AS average_rating
                FROM employees
                GROUP BY department
            """
        },

        "recruitment": {
            "filename": "recruitment_analytics.csv",
            "query": """
                SELECT
                    j.job_title,
                    j.department,
                    j.status AS job_status,
                    COUNT(a.id) AS total_applications,
                    SUM(CASE WHEN a.status = 'Hired' THEN 1 ELSE 0 END)
                        AS hired_candidates
                FROM job_openings j
                LEFT JOIN job_applications a ON j.id = a.job_id
                GROUP BY j.id, j.job_title, j.department, j.status
            """
        },

        "attendance": {
            "filename": "attendance_analytics.csv",
            "query": """
                SELECT
                    DATE(attendance_date) AS attendance_day,
                    status,
                    COUNT(*) AS total_records
                FROM attendance
                GROUP BY DATE(attendance_date), status
                ORDER BY attendance_day DESC
            """
        },

        "leave": {
            "filename": "leave_analytics.csv",
            "query": """
                SELECT
                    leave_type,
                    status,
                    COUNT(*) AS total_requests
                FROM leave_requests
                GROUP BY leave_type, status
                ORDER BY leave_type
            """
        },

        "payroll": {
            "filename": "payroll_analytics.csv",
            "query": """
                SELECT
                    month,
                    year,
                    COUNT(*) AS payroll_records,
                    SUM(gross_salary) AS gross_payroll,
                    SUM(net_salary) AS net_payroll,
                    payment_status
                FROM payroll
                GROUP BY year, month, payment_status
                ORDER BY year DESC, month DESC
            """
        },

        "training": {
            "filename": "training_analytics.csv",
            "query": """
                SELECT
                    c.course_name,
                    COUNT(e.id) AS total_enrollments,
                    SUM(CASE WHEN e.status = 'Completed' THEN 1 ELSE 0 END)
                        AS completed,
                    AVG(e.assessment_score) AS average_score
                FROM training_courses c
                LEFT JOIN training_enrollments e ON c.id = e.course_id
                GROUP BY c.id, c.course_name
            """
        },

        "performance": {
            "filename": "performance_analytics.csv",
            "query": """
                SELECT
                    e.name,
                    e.department,
                    COUNT(pr.id) AS total_reviews,
                    AVG(pr.rating) AS average_rating,
                    MAX(pr.rating) AS highest_rating
                FROM employees e
                LEFT JOIN performance_reviews pr ON e.id = pr.employee_id
                GROUP BY e.id, e.name, e.department
            """
        }
    }

    if report_key not in reports:
        print("Invalid report selection.")
        return

    report = reports[report_key]

    os.makedirs("exports", exist_ok=True)
    file_path = os.path.join("exports", report["filename"])

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(report["query"])
        records = cursor.fetchall()
        headers = [column[0] for column in cursor.description]

        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(records)

        print("\nReport exported successfully!")
        print("File:", os.path.abspath(file_path))
        print("Rows exported:", len(records))

    except sqlite3.Error as error:
        print("Database error while exporting:", error)

    except OSError as error:
        print("File error while exporting:", error)

    finally:
        connection.close()


def export_all_analytics_reports():

    print("\n========== EXPORTING ALL ANALYTICS REPORTS ==========")

    report_keys = [
        "employees",
        "recruitment",
        "attendance",
        "leave",
        "payroll",
        "training",
        "performance"
    ]

    for report_key in report_keys:
        print("\nExporting:", report_key.title())
        export_analytics_report(report_key)

    print("\nAll analytics export operations finished.")
    print("Check the exports folder inside C:\\Projects.")


def analytics_export_menu():

    while True:
        print("\n========================================")
        print("       ANALYTICS REPORT EXPORTS")
        print("========================================")
        print("1. Export Employee Analytics")
        print("2. Export Recruitment Analytics")
        print("3. Export Attendance Analytics")
        print("4. Export Leave Analytics")
        print("5. Export Payroll Analytics")
        print("6. Export Training Analytics")
        print("7. Export Performance Analytics")
        print("8. Export ALL Reports")
        print("9. Back")

        choice = input("\nChoose an option: ").strip()

        report_options = {
            "1": "employees",
            "2": "recruitment",
            "3": "attendance",
            "4": "leave",
            "5": "payroll",
            "6": "training",
            "7": "performance"
        }

        if choice in report_options:
            export_analytics_report(report_options[choice])

        elif choice == "8":
            export_all_analytics_reports()

        elif choice == "9":
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================
# COMPLETE V9.0 ANALYTICS DASHBOARD
# ==========================================

def advanced_analytics_menu():

    while True:
        print("\n")
        print("=" * 48)
        print("       ADVANCED HR ANALYTICS DASHBOARD")
        print("=" * 48)
        print("1. Employee Analytics")
        print("2. Recruitment Analytics")
        print("3. Attendance & Leave Analytics")
        print("4. Payroll Cost Analysis")
        print("5. Training & Performance Analytics")
        print("6. Export Analytics Reports")
        print("7. Exit Dashboard")
        print("=" * 48)

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            employee_analytics_menu()

        elif choice == "2":
            recruitment_analytics_menu()

        elif choice == "3":
            attendance_leave_analytics_menu()

        elif choice == "4":
            payroll_analytics_menu()

        elif choice == "5":
            training_performance_analytics_menu()

        elif choice == "6":
            analytics_export_menu()

        elif choice == "7":
            print("Returning to previous menu...")
            break

        else:
            print("Invalid choice. Please try again.")
