
import sqlite3
from datetime import date, datetime

DATABASE_NAME = "employees.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_recruitment_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_openings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            department TEXT NOT NULL,
            description TEXT,
            employment_type TEXT,
            vacancies INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Open',
            created_on TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            skills TEXT,
            experience_years REAL DEFAULT 0,
            resume_path TEXT,
            registered_on TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Applied',
            applied_on TEXT,
            FOREIGN KEY (candidate_id)
                REFERENCES candidates(id),
            FOREIGN KEY (job_id)
                REFERENCES job_openings(id),
            UNIQUE(candidate_id, job_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            interview_date TEXT NOT NULL,
            interview_type TEXT,
            interviewer TEXT,
            feedback TEXT,
            result TEXT DEFAULT 'Pending',
            FOREIGN KEY (application_id)
                REFERENCES job_applications(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recruitment_offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL UNIQUE,
            offered_salary REAL NOT NULL,
            offer_date TEXT,
            joining_date TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (application_id)
                REFERENCES job_applications(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS onboarding_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            task_name TEXT NOT NULL,
            assigned_to TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            completed_on TEXT,
            FOREIGN KEY (employee_id)
                REFERENCES employees(id)
        )
    """)

    connection.commit()
    connection.close()

    print("Recruitment and onboarding tables created successfully!")


if __name__ == "__main__":
    create_recruitment_tables()



def add_job_opening():

    print("\n========== ADD JOB OPENING ==========")

    job_title = input("Job Title: ").strip()
    department = input("Department: ").strip()
    description = input("Job Description: ").strip()
    employment_type = input(
        "Employment Type (Full-time/Part-time/Contract): "
    ).strip()

    try:
        vacancies = int(input("Number of Vacancies: "))
        if vacancies <= 0:
            print("Vacancies must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    if not job_title or not department:
        print("Job title and department are required.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO job_openings (
            job_title,
            department,
            description,
            employment_type,
            vacancies,
            status,
            created_on
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        job_title,
        department,
        description,
        employment_type,
        vacancies,
        "Open",
        date.today().isoformat()
    ))

    connection.commit()
    connection.close()

    print("\nJob opening added successfully!")


def view_job_openings():

    print("\n========== JOB OPENINGS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, job_title, department,
               employment_type, vacancies, status
        FROM job_openings
        ORDER BY id DESC
    """)

    jobs = cursor.fetchall()
    connection.close()

    if not jobs:
        print("No job openings found.")
        return

    for job in jobs:
        print("\nJob ID:", job[0])
        print("Title:", job[1])
        print("Department:", job[2])
        print("Employment Type:", job[3])
        print("Vacancies:", job[4])
        print("Status:", job[5])
        print("-" * 40)


def search_job_opening():

    print("\n========== SEARCH JOB ==========")

    keyword = input("Enter job title or department: ").strip()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, job_title, department,
               employment_type, vacancies, status
        FROM job_openings
        WHERE job_title LIKE ? OR department LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    jobs = cursor.fetchall()
    connection.close()

    if not jobs:
        print("No matching jobs found.")
        return

    for job in jobs:
        print("\nJob ID:", job[0])
        print("Title:", job[1])
        print("Department:", job[2])
        print("Employment Type:", job[3])
        print("Vacancies:", job[4])
        print("Status:", job[5])


def update_job_opening():

    print("\n========== UPDATE JOB ==========")

    view_job_openings()

    try:
        job_id = int(input("\nEnter Job ID to update: "))
    except ValueError:
        print("Invalid Job ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT job_title, department, description,
               employment_type, vacancies
        FROM job_openings
        WHERE id = ?
    """, (job_id,))

    job = cursor.fetchone()

    if not job:
        connection.close()
        print("Job not found.")
        return

    print("Press Enter to keep the existing value.")

    title = input(f"Job Title [{job[0]}]: ").strip() or job[0]
    department = input(
        f"Department [{job[1]}]: "
    ).strip() or job[1]

    description = input(
        f"Description [{job[2]}]: "
    ).strip() or job[2]

    employment_type = input(
        f"Employment Type [{job[3]}]: "
    ).strip() or job[3]

    vacancies_input = input(
        f"Vacancies [{job[4]}]: "
    ).strip()

    try:
        vacancies = int(vacancies_input) if vacancies_input else job[4]

        if vacancies <= 0:
            print("Vacancies must be greater than zero.")
            connection.close()
            return

    except ValueError:
        print("Invalid vacancy number.")
        connection.close()
        return

    cursor.execute("""
        UPDATE job_openings
        SET job_title = ?,
            department = ?,
            description = ?,
            employment_type = ?,
            vacancies = ?
        WHERE id = ?
    """, (
        title, department, description,
        employment_type, vacancies, job_id
    ))

    connection.commit()
    connection.close()

    print("Job opening updated successfully!")


def close_job_opening():

    print("\n========== CLOSE JOB ==========")

    view_job_openings()

    try:
        job_id = int(input("\nEnter Job ID to close: "))
    except ValueError:
        print("Invalid Job ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id FROM job_openings WHERE id = ?
    """, (job_id,))

    if not cursor.fetchone():
        connection.close()
        print("Job not found.")
        return

    cursor.execute("""
        UPDATE job_openings
        SET status = 'Closed'
        WHERE id = ?
    """, (job_id,))

    connection.commit()
    connection.close()

    print("Job opening closed successfully!")


def job_opening_menu():

    while True:

        print("\n========== JOB OPENING MANAGEMENT ==========")
        print("1. Add Job Opening")
        print("2. View Job Openings")
        print("3. Search Job Opening")
        print("4. Update Job Opening")
        print("5. Close Job Opening")
        print("6. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_job_opening()

        elif choice == "2":
            view_job_openings()

        elif choice == "3":
            search_job_opening()

        elif choice == "4":
            update_job_opening()

        elif choice == "5":
            close_job_opening()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


def register_candidate():

    print("\n========== CANDIDATE REGISTRATION ==========")

    name = input("Candidate Name: ").strip()
    email = input("Email: ").strip().lower()
    phone = input("Phone Number: ").strip()
    skills = input("Skills (comma separated): ").strip()

    try:
        experience = float(input("Experience in Years: "))
        if experience < 0:
            print("Experience cannot be negative.")
            return
    except ValueError:
        print("Enter a valid experience value.")
        return

    resume_path = input(
        "Resume File Path (optional): "
    ).strip()

    if not name or not email:
        print("Name and email are required.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO candidates (
                candidate_name,
                email,
                phone,
                skills,
                experience_years,
                resume_path,
                registered_on
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            phone,
            skills,
            experience,
            resume_path,
            date.today().isoformat()
        ))

        connection.commit()
        print("\nCandidate registered successfully!")

    except sqlite3.IntegrityError:
        print("A candidate with this email already exists.")

    finally:
        connection.close()


def view_candidates():

    print("\n========== ALL CANDIDATES ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, candidate_name, email, phone,
               skills, experience_years, registered_on
        FROM candidates
        ORDER BY id DESC
    """)

    candidates = cursor.fetchall()
    connection.close()

    if not candidates:
        print("No candidates registered.")
        return

    for candidate in candidates:

        print("\nCandidate ID:", candidate[0])
        print("Name:", candidate[1])
        print("Email:", candidate[2])
        print("Phone:", candidate[3])
        print("Skills:", candidate[4])
        print("Experience:", candidate[5], "years")
        print("Registered On:", candidate[6])
        print("-" * 45)


def search_candidate():

    print("\n========== SEARCH CANDIDATE ==========")

    keyword = input(
        "Enter candidate name or email: "
    ).strip()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, candidate_name, email,
               phone, skills, experience_years
        FROM candidates
        WHERE candidate_name LIKE ?
           OR email LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    candidates = cursor.fetchall()
    connection.close()

    if not candidates:
        print("No matching candidates found.")
        return

    for candidate in candidates:

        print("\nCandidate ID:", candidate[0])
        print("Name:", candidate[1])
        print("Email:", candidate[2])
        print("Phone:", candidate[3])
        print("Skills:", candidate[4])
        print("Experience:", candidate[5], "years")


def update_candidate():

    print("\n========== UPDATE CANDIDATE ==========")

    view_candidates()

    try:
        candidate_id = int(input("\nEnter Candidate ID: "))
    except ValueError:
        print("Invalid Candidate ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT candidate_name, email, phone,
               skills, experience_years, resume_path
        FROM candidates
        WHERE id = ?
    """, (candidate_id,))

    candidate = cursor.fetchone()

    if not candidate:
        connection.close()
        print("Candidate not found.")
        return

    print("\nPress Enter to keep existing values.")

    name = input(
        f"Name [{candidate[0]}]: "
    ).strip() or candidate[0]

    email = input(
        f"Email [{candidate[1]}]: "
    ).strip().lower() or candidate[1]

    phone = input(
        f"Phone [{candidate[2]}]: "
    ).strip() or candidate[2]

    skills = input(
        f"Skills [{candidate[3]}]: "
    ).strip() or candidate[3]

    experience_input = input(
        f"Experience [{candidate[4]}]: "
    ).strip()

    try:
        experience = (
            float(experience_input)
            if experience_input else candidate[4]
        )

        if experience < 0:
            print("Experience cannot be negative.")
            connection.close()
            return

    except ValueError:
        print("Invalid experience value.")
        connection.close()
        return

    resume_path = input(
        f"Resume Path [{candidate[5]}]: "
    ).strip() or candidate[5]

    try:
        cursor.execute("""
            UPDATE candidates
            SET candidate_name = ?,
                email = ?,
                phone = ?,
                skills = ?,
                experience_years = ?,
                resume_path = ?
            WHERE id = ?
        """, (
            name, email, phone, skills,
            experience, resume_path, candidate_id
        ))

        connection.commit()
        print("Candidate updated successfully!")

    except sqlite3.IntegrityError:
        print("Another candidate already uses this email.")

    finally:
        connection.close()


def delete_candidate():

    print("\n========== DELETE CANDIDATE ==========")

    view_candidates()

    try:
        candidate_id = int(input("\nEnter Candidate ID: "))
    except ValueError:
        print("Invalid Candidate ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id FROM candidates WHERE id = ?
    """, (candidate_id,))

    if not cursor.fetchone():
        connection.close()
        print("Candidate not found.")
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM job_applications
        WHERE candidate_id = ?
    """, (candidate_id,))

    application_count = cursor.fetchone()[0]

    if application_count > 0:
        connection.close()
        print(
            "Cannot delete this candidate because "
            "job applications are linked to them."
        )
        return

    cursor.execute("""
        DELETE FROM candidates WHERE id = ?
    """, (candidate_id,))

    connection.commit()
    connection.close()

    print("Candidate deleted successfully!")


def candidate_management_menu():

    while True:

        print("\n========== CANDIDATE MANAGEMENT ==========")
        print("1. Register Candidate")
        print("2. View Candidates")
        print("3. Search Candidate")
        print("4. Update Candidate")
        print("5. Delete Candidate")
        print("6. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_candidate()

        elif choice == "2":
            view_candidates()

        elif choice == "3":
            search_candidate()

        elif choice == "4":
            update_candidate()

        elif choice == "5":
            delete_candidate()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


APPLICATION_STATUSES = [
    "Applied",
    "Shortlisted",
    "Rejected",
    "Interview Scheduled",
    "Selected",
    "Offer Released",
    "Hired"
]


def apply_candidate_for_job():

    print("\n========== APPLY CANDIDATE FOR JOB ==========")

    view_candidates()
    view_job_openings()

    try:
        candidate_id = int(input("\nEnter Candidate ID: "))
        job_id = int(input("Enter Job ID: "))
    except ValueError:
        print("Please enter valid IDs.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id FROM candidates WHERE id = ?
    """, (candidate_id,))

    if not cursor.fetchone():
        connection.close()
        print("Candidate not found.")
        return

    cursor.execute("""
        SELECT status FROM job_openings WHERE id = ?
    """, (job_id,))

    job = cursor.fetchone()

    if not job:
        connection.close()
        print("Job opening not found.")
        return

    if job[0] != "Open":
        connection.close()
        print("This job opening is closed.")
        return

    try:
        cursor.execute("""
            INSERT INTO job_applications (
                candidate_id,
                job_id,
                status,
                applied_on
            )
            VALUES (?, ?, ?, ?)
        """, (
            candidate_id,
            job_id,
            "Applied",
            date.today().isoformat()
        ))

        connection.commit()
        print("Candidate successfully applied for the job!")

    except sqlite3.IntegrityError:
        print("This candidate has already applied for this job.")

    finally:
        connection.close()


def view_job_applications():

    print("\n========== JOB APPLICATIONS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            ja.id,
            c.candidate_name,
            jo.job_title,
            jo.department,
            ja.status,
            ja.applied_on
        FROM job_applications ja
        JOIN candidates c ON ja.candidate_id = c.id
        JOIN job_openings jo ON ja.job_id = jo.id
        ORDER BY ja.id DESC
    """)

    applications = cursor.fetchall()
    connection.close()

    if not applications:
        print("No applications found.")
        return

    for application in applications:

        print("\nApplication ID:", application[0])
        print("Candidate:", application[1])
        print("Job:", application[2])
        print("Department:", application[3])
        print("Status:", application[4])
        print("Applied On:", application[5])
        print("-" * 45)


def search_job_application():

    print("\n========== SEARCH APPLICATION ==========")

    keyword = input(
        "Enter candidate name or job title: "
    ).strip()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            ja.id,
            c.candidate_name,
            jo.job_title,
            ja.status,
            ja.applied_on
        FROM job_applications ja
        JOIN candidates c ON ja.candidate_id = c.id
        JOIN job_openings jo ON ja.job_id = jo.id
        WHERE c.candidate_name LIKE ?
           OR jo.job_title LIKE ?
        ORDER BY ja.id DESC
    """, (f"%{keyword}%", f"%{keyword}%"))

    applications = cursor.fetchall()
    connection.close()

    if not applications:
        print("No matching applications found.")
        return

    for application in applications:

        print("\nApplication ID:", application[0])
        print("Candidate:", application[1])
        print("Job:", application[2])
        print("Status:", application[3])
        print("Applied On:", application[4])


def update_application_status():

    print("\n========== UPDATE APPLICATION STATUS ==========")

    view_job_applications()

    try:
        application_id = int(
            input("\nEnter Application ID: ")
        )
    except ValueError:
        print("Invalid Application ID.")
        return

    print("\nAvailable Statuses:")

    for index, status in enumerate(APPLICATION_STATUSES, start=1):
        print(f"{index}. {status}")

    try:
        status_choice = int(input("Select new status: "))

        if status_choice < 1 or status_choice > len(APPLICATION_STATUSES):
            print("Invalid status choice.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    new_status = APPLICATION_STATUSES[status_choice - 1]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE job_applications
        SET status = ?
        WHERE id = ?
    """, (new_status, application_id))

    if cursor.rowcount == 0:
        connection.close()
        print("Application not found.")
        return

    connection.commit()
    connection.close()

    print("Application status updated successfully!")


def application_tracking_menu():

    while True:

        print("\n========== APPLICATION TRACKING ==========")
        print("1. Apply Candidate for Job")
        print("2. View All Applications")
        print("3. Search Application")
        print("4. Update Application Status")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            apply_candidate_for_job()

        elif choice == "2":
            view_job_applications()

        elif choice == "3":
            search_job_application()

        elif choice == "4":
            update_application_status()

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")


INTERVIEW_RESULTS = [
    "Pending",
    "Passed",
    "Failed",
    "Rescheduled"
]


def schedule_interview():

    print("\n========== SCHEDULE INTERVIEW ==========")

    view_job_applications()

    try:
        application_id = int(input("\nEnter Application ID: "))
    except ValueError:
        print("Invalid Application ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, status
        FROM job_applications
        WHERE id = ?
    """, (application_id,))

    application = cursor.fetchone()

    if not application:
        connection.close()
        print("Application not found.")
        return

    if application[1] in ("Rejected", "Hired"):
        connection.close()
        print("An interview cannot be scheduled for this application.")
        return

    interview_date = input(
        "Interview Date (YYYY-MM-DD): "
    ).strip()

    try:
        datetime.strptime(interview_date, "%Y-%m-%d")
    except ValueError:
        connection.close()
        print("Invalid date. Use YYYY-MM-DD.")
        return

    interview_type = input(
        "Interview Type (Online/Offline/Technical/HR): "
    ).strip()

    interviewer = input("Interviewer Name: ").strip()

    if not interview_type or not interviewer:
        connection.close()
        print("Interview type and interviewer are required.")
        return

    cursor.execute("""
        INSERT INTO interviews (
            application_id,
            interview_date,
            interview_type,
            interviewer,
            feedback,
            result
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        application_id,
        interview_date,
        interview_type,
        interviewer,
        "",
        "Pending"
    ))

    cursor.execute("""
        UPDATE job_applications
        SET status = 'Interview Scheduled'
        WHERE id = ?
    """, (application_id,))

    connection.commit()
    connection.close()

    print("\nInterview scheduled successfully!")


def view_interviews():

    print("\n========== INTERVIEW SCHEDULE ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            i.id,
            c.candidate_name,
            jo.job_title,
            i.interview_date,
            i.interview_type,
            i.interviewer,
            i.feedback,
            i.result
        FROM interviews i
        JOIN job_applications ja
            ON i.application_id = ja.id
        JOIN candidates c
            ON ja.candidate_id = c.id
        JOIN job_openings jo
            ON ja.job_id = jo.id
        ORDER BY i.interview_date DESC
    """)

    interviews = cursor.fetchall()
    connection.close()

    if not interviews:
        print("No interviews scheduled.")
        return

    for interview in interviews:

        print("\nInterview ID:", interview[0])
        print("Candidate:", interview[1])
        print("Job Title:", interview[2])
        print("Interview Date:", interview[3])
        print("Interview Type:", interview[4])
        print("Interviewer:", interview[5])
        print("Feedback:", interview[6] or "Not recorded")
        print("Result:", interview[7])
        print("-" * 45)


def update_interview_feedback():

    print("\n========== UPDATE INTERVIEW FEEDBACK ==========")

    view_interviews()

    try:
        interview_id = int(input("\nEnter Interview ID: "))
    except ValueError:
        print("Invalid Interview ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT application_id
        FROM interviews
        WHERE id = ?
    """, (interview_id,))

    interview = cursor.fetchone()

    if not interview:
        connection.close()
        print("Interview not found.")
        return

    feedback = input("Enter Interview Feedback: ").strip()

    print("\nInterview Results:")

    for index, result in enumerate(INTERVIEW_RESULTS, start=1):
        print(f"{index}. {result}")

    try:
        choice = int(input("Choose Result: "))

        if choice < 1 or choice > len(INTERVIEW_RESULTS):
            print("Invalid result choice.")
            connection.close()
            return

    except ValueError:
        print("Please enter a valid number.")
        connection.close()
        return

    result = INTERVIEW_RESULTS[choice - 1]

    cursor.execute("""
        UPDATE interviews
        SET feedback = ?,
            result = ?
        WHERE id = ?
    """, (feedback, result, interview_id))

    application_id = interview[0]

    if result == "Passed":
        application_status = "Selected"
    elif result == "Failed":
        application_status = "Rejected"
    else:
        application_status = "Interview Scheduled"

    cursor.execute("""
        UPDATE job_applications
        SET status = ?
        WHERE id = ?
    """, (application_status, application_id))

    connection.commit()
    connection.close()

    print("\nInterview feedback saved successfully!")


def interview_management_menu():

    while True:

        print("\n========== INTERVIEW MANAGEMENT ==========")
        print("1. Schedule Interview")
        print("2. View All Interviews")
        print("3. Update Interview Feedback")
        print("4. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            schedule_interview()

        elif choice == "2":
            view_interviews()

        elif choice == "3":
            update_interview_feedback()

        elif choice == "4":
            break

        else:
            print("Invalid choice. Try again.")


OFFER_STATUSES = [
    "Pending",
    "Accepted",
    "Declined"
]


def create_job_offer():

    print("\n========== CREATE JOB OFFER ==========")

    view_job_applications()

    try:
        application_id = int(input("\nEnter Application ID: "))
    except ValueError:
        print("Invalid Application ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status
        FROM job_applications
        WHERE id = ?
    """, (application_id,))

    application = cursor.fetchone()

    if not application:
        connection.close()
        print("Application not found.")
        return

    if application[0] not in ("Selected", "Offer Released"):
        connection.close()
        print("Only selected candidates can receive an offer.")
        return

    cursor.execute("""
        SELECT id
        FROM recruitment_offers
        WHERE application_id = ?
    """, (application_id,))

    if cursor.fetchone():
        connection.close()
        print("An offer already exists for this application.")
        return

    try:
        offered_salary = float(input("Offered Annual Salary: "))

        if offered_salary <= 0:
            print("Salary must be greater than zero.")
            connection.close()
            return

    except ValueError:
        print("Enter a valid salary.")
        connection.close()
        return

    offer_date = input("Offer Date (YYYY-MM-DD): ").strip()
    joining_date = input("Joining Date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(offer_date, "%Y-%m-%d")
        datetime.strptime(joining_date, "%Y-%m-%d")

        if joining_date < offer_date:
            print("Joining date cannot be before offer date.")
            connection.close()
            return

    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO recruitment_offers (
            application_id,
            offered_salary,
            offer_date,
            joining_date,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        application_id,
        offered_salary,
        offer_date,
        joining_date,
        "Pending"
    ))

    cursor.execute("""
        UPDATE job_applications
        SET status = 'Offer Released'
        WHERE id = ?
    """, (application_id,))

    connection.commit()
    connection.close()

    print("\nJob offer created successfully!")


def view_job_offers():

    print("\n========== JOB OFFERS ==========")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            ro.id,
            c.candidate_name,
            jo.job_title,
            ro.offered_salary,
            ro.offer_date,
            ro.joining_date,
            ro.status
        FROM recruitment_offers ro
        JOIN job_applications ja
            ON ro.application_id = ja.id
        JOIN candidates c
            ON ja.candidate_id = c.id
        JOIN job_openings jo
            ON ja.job_id = jo.id
        ORDER BY ro.id DESC
    """)

    offers = cursor.fetchall()
    connection.close()

    if not offers:
        print("No job offers found.")
        return

    for offer in offers:

        print("\nOffer ID:", offer[0])
        print("Candidate:", offer[1])
        print("Job Title:", offer[2])
        print("Offered Salary:", offer[3])
        print("Offer Date:", offer[4])
        print("Joining Date:", offer[5])
        print("Offer Status:", offer[6])
        print("-" * 45)


def update_offer_status():

    print("\n========== UPDATE OFFER STATUS ==========")

    view_job_offers()

    try:
        offer_id = int(input("\nEnter Offer ID: "))
    except ValueError:
        print("Invalid Offer ID.")
        return

    print("\nOffer Status Options:")

    for index, status in enumerate(OFFER_STATUSES, start=1):
        print(f"{index}. {status}")

    try:
        choice = int(input("Choose new status: "))

        if choice < 1 or choice > len(OFFER_STATUSES):
            print("Invalid choice.")
            return

    except ValueError:
        print("Enter a valid number.")
        return

    new_status = OFFER_STATUSES[choice - 1]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT application_id
        FROM recruitment_offers
        WHERE id = ?
    """, (offer_id,))

    offer = cursor.fetchone()

    if not offer:
        connection.close()
        print("Offer not found.")
        return

    application_id = offer[0]

    cursor.execute("""
        UPDATE recruitment_offers
        SET status = ?
        WHERE id = ?
    """, (new_status, offer_id))

    if new_status == "Accepted":
        application_status = "Hired"

    elif new_status == "Declined":
        application_status = "Offer Declined"

    else:
        application_status = "Offer Released"

    cursor.execute("""
        UPDATE job_applications
        SET status = ?
        WHERE id = ?
    """, (application_status, application_id))

    connection.commit()
    connection.close()

    print("\nOffer status updated successfully!")

    if new_status == "Accepted":
        print("Candidate application marked as Hired.")


def offer_management_menu():

    while True:

        print("\n========== OFFER MANAGEMENT ==========")
        print("1. Create Job Offer")
        print("2. View Job Offers")
        print("3. Update Offer Status")
        print("4. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_job_offer()

        elif choice == "2":
            view_job_offers()

        elif choice == "3":
            update_offer_status()

        elif choice == "4":
            break

        else:
            print("Invalid choice. Try again.")


# ==========================================
# V8.0 STAGE 7 - ONBOARDING MANAGEMENT
# ==========================================

ONBOARDING_STATUSES = ["Pending", "In Progress", "Completed"]


def create_candidate_employee_link_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidate_employee_links (
            candidate_id INTEGER PRIMARY KEY,
            employee_id INTEGER UNIQUE NOT NULL,
            created_on TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    """)

    connection.commit()
    connection.close()


def convert_hired_candidate_to_employee():

    create_candidate_employee_link_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            a.id,
            c.id,
            c.candidate_name,
            c.email,
            j.department,
            o.offered_salary
        FROM job_applications a
        JOIN candidates c ON a.candidate_id = c.id
        JOIN job_openings j ON a.job_id = j.id
        JOIN recruitment_offers o ON o.application_id = a.id
        WHERE a.status = 'Hired'
        AND o.status = 'Accepted'
        ORDER BY a.id
    """)

    candidates_list = cursor.fetchall()

    if not candidates_list:
        print("\nNo candidates with accepted offers are available.")
        connection.close()
        return

    print("\n========== HIRED CANDIDATES ==========")

    for candidate in candidates_list:
        print(
            f"Application ID: {candidate[0]} | "
            f"Candidate ID: {candidate[1]} | "
            f"Name: {candidate[2]} | "
            f"Department: {candidate[4]} | "
            f"Salary: {candidate[5]:,.2f}"
        )

    try:
        application_id = int(input("\nEnter Application ID to convert: "))
    except ValueError:
        print("Please enter a valid application ID.")
        connection.close()
        return

    selected = next(
        (candidate for candidate in candidates_list
         if candidate[0] == application_id),
        None
    )

    if selected is None:
        print("Invalid application ID or offer not accepted.")
        connection.close()
        return

    _, candidate_id, name, email, department, salary = selected

    cursor.execute("""
        SELECT employee_id
        FROM candidate_employee_links
        WHERE candidate_id = ?
    """, (candidate_id,))

    existing_link = cursor.fetchone()

    if existing_link:
        print(
            f"This candidate is already an employee. "
            f"Employee ID: {existing_link[0]}"
        )
        connection.close()
        return

    try:
        cursor.execute("""
            INSERT INTO employees (name, department, salary, rating)
            VALUES (?, ?, ?, ?)
        """, (name, department, salary, 0))

        employee_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO candidate_employee_links
            (candidate_id, employee_id, created_on)
            VALUES (?, ?, ?)
        """, (candidate_id, employee_id, date.today().isoformat()))

        connection.commit()

        print("\nCandidate successfully converted into an employee!")
        print("Employee ID:", employee_id)
        print("Employee Name:", name)
        print("Department:", department)
        print("Salary:", f"{salary:,.2f}")

    except sqlite3.Error as error:
        connection.rollback()
        print("Could not convert candidate:", error)

    finally:
        connection.close()


def add_onboarding_task():

    create_candidate_employee_link_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, department
        FROM employees
        ORDER BY id
    """)

    employees = cursor.fetchall()

    if not employees:
        print("\nNo employees found.")
        connection.close()
        return

    print("\n========== EMPLOYEE LIST ==========")

    for employee in employees:
        print(
            f"ID: {employee[0]} | "
            f"Name: {employee[1]} | "
            f"Department: {employee[2]}"
        )

    try:
        employee_id = int(input("\nEnter Employee ID: "))
    except ValueError:
        print("Invalid employee ID.")
        connection.close()
        return

    cursor.execute(
        "SELECT id FROM employees WHERE id = ?",
        (employee_id,)
    )

    if cursor.fetchone() is None:
        print("Employee not found.")
        connection.close()
        return

    task_name = input("Enter onboarding task name: ").strip()
    assigned_to = input("Assigned to: ").strip()
    due_date = input("Due date (YYYY-MM-DD): ").strip()

    if not task_name:
        print("Task name cannot be empty.")
        connection.close()
        return

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO onboarding_tasks
        (employee_id, task_name, assigned_to, due_date, status)
        VALUES (?, ?, ?, ?, 'Pending')
    """, (employee_id, task_name, assigned_to, due_date))

    connection.commit()
    connection.close()

    print("\nOnboarding task added successfully!")


def view_onboarding_tasks():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            t.id,
            e.name,
            e.department,
            t.task_name,
            t.assigned_to,
            t.due_date,
            t.status,
            t.completed_on
        FROM onboarding_tasks t
        JOIN employees e ON t.employee_id = e.id
        ORDER BY t.id DESC
    """)

    tasks = cursor.fetchall()
    connection.close()

    print("\n========== ONBOARDING TASKS ==========")

    if not tasks:
        print("No onboarding tasks found.")
        return

    for task in tasks:
        print("-" * 55)
        print("Task ID:", task[0])
        print("Employee:", task[1])
        print("Department:", task[2])
        print("Task:", task[3])
        print("Assigned To:", task[4])
        print("Due Date:", task[5])
        print("Status:", task[6])
        print("Completed On:", task[7] or "Not completed")

    print("-" * 55)


def update_onboarding_task():

    view_onboarding_tasks()

    try:
        task_id = int(input("\nEnter Task ID to update: "))
    except ValueError:
        print("Invalid task ID.")
        return

    print("\nAvailable Statuses:")

    for index, status in enumerate(ONBOARDING_STATUSES, start=1):
        print(f"{index}. {status}")

    try:
        choice = int(input("Choose status: "))

        if choice < 1 or choice > len(ONBOARDING_STATUSES):
            print("Invalid choice.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    new_status = ONBOARDING_STATUSES[choice - 1]

    completed_on = (
        date.today().isoformat()
        if new_status == "Completed"
        else None
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE onboarding_tasks
        SET status = ?, completed_on = ?
        WHERE id = ?
    """, (new_status, completed_on, task_id))

    if cursor.rowcount == 0:
        print("Task ID not found.")
    else:
        print("Onboarding task updated successfully!")

    connection.commit()
    connection.close()


def onboarding_summary():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END)
        FROM onboarding_tasks
    """)

    result = cursor.fetchone()
    connection.close()

    total = result[0] or 0
    pending = result[1] or 0
    in_progress = result[2] or 0
    completed = result[3] or 0

    completion_rate = (
        completed / total * 100
        if total > 0 else 0
    )

    print("\n========== ONBOARDING SUMMARY ==========")
    print("Total Tasks:", total)
    print("Pending Tasks:", pending)
    print("In Progress Tasks:", in_progress)
    print("Completed Tasks:", completed)
    print(f"Completion Rate: {completion_rate:.2f}%")


def onboarding_management_menu():

    create_candidate_employee_link_table()

    while True:

        print("\n===================================")
        print("      ONBOARDING MANAGEMENT")
        print("===================================")
        print("1. Convert Hired Candidate to Employee")
        print("2. Add Onboarding Task")
        print("3. View Onboarding Tasks")
        print("4. Update Onboarding Task")
        print("5. Onboarding Summary")
        print("6. Back")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            convert_hired_candidate_to_employee()

        elif choice == "2":
            add_onboarding_task()

        elif choice == "3":
            view_onboarding_tasks()

        elif choice == "4":
            update_onboarding_task()

        elif choice == "5":
            onboarding_summary()

        elif choice == "6":
            print("Returning to previous menu...")
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================
# RECRUITMENT AND ONBOARDING MAIN MENU
# ==========================================

def recruitment_management_menu():

    while True:

        print("\n===================================")
        print("   RECRUITMENT & ONBOARDING")
        print("===================================")
        print("1. Job Opening Management")
        print("2. Candidate Management")
        print("3. Job Application Tracking")
        print("4. Interview Management")
        print("5. Offer Management")
        print("6. Onboarding Management")
        print("7. Back to Dashboard")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            job_opening_menu()

        elif choice == "2":
            candidate_management_menu()

        elif choice == "3":
            application_tracking_menu()

        elif choice == "4":
            interview_management_menu()

        elif choice == "5":
            offer_management_menu()

        elif choice == "6":
            onboarding_management_menu()

        elif choice == "7":
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================
# V8.0 - COMPLETE RECRUITMENT MENU
# ==========================================

def recruitment_management_menu():

    while True:

        print("\n===================================")
        print("       RECRUITMENT MANAGEMENT")
        print("===================================")
        print("1. Job Opening Management")
        print("2. Candidate Management")
        print("3. Job Application Tracking")
        print("4. Interview Management")
        print("5. Offer Management")
        print("6. Onboarding Management")
        print("7. Back")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            job_opening_menu()

        elif choice == "2":
            candidate_management_menu()

        elif choice == "3":
            application_tracking_menu()

        elif choice == "4":
            interview_management_menu()

        elif choice == "5":
            offer_management_menu()

        elif choice == "6":
            onboarding_management_menu()

        elif choice == "7":
            print("Returning to dashboard...")
            break

        else:
            print("Invalid choice. Please try again.")
