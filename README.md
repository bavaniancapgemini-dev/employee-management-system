# Employee Management System v2.0

A Python-based Employee Management System designed to manage employee records, attendance, performance ratings, reporting, and data exports using SQLite database integration.

This project demonstrates modular programming, database management, reporting, analytics, and GitHub workflow using Python.

---

## Version

### Current Version: v2.0

### Previous Versions

#### v1.0

* Add Employee
* View Employees
* Search Employee
* Delete Employee
* Update Salary
* Highest Salary Report
* Average Salary Report

#### v2.0

* Department Reports
* Attendance Tracking
* Performance Ratings
* Top Performer Report
* Dashboard Statistics
* JSON Export System

---

## Features

### Employee Management

* Add Employee
* View Employees
* Search Employee
* Delete Employee
* Update Salary

### Reports

* Highest Salary Report
* Average Salary Report
* Department-wise Employee Report
* Top Performer Report

### Attendance System

* Mark Attendance
* View Attendance Records

### Performance Management

* Employee Performance Rating
* Top Performer Identification

### Dashboard

* Total Employees
* Average Salary
* Top Performer Statistics

### Backup System

* Export Employee Data to JSON

---

## Project Structure

employee-management-system/

│── main.py
│── database.py
│── reports.py
│── attendance.py
│── backup.py
│── utils.py
│── employees.db
│── employees.json
│── README.md

---

## Technologies Used

* Python
* SQLite3
* VS Code
* Git
* GitHub

---

## Database Tables

### employees

* Employee ID
* Name
* Department
* Salary
* Performance Rating

### attendance

* Attendance ID
* Employee ID

---

## How to Run

### Clone Repository

git clone https://github.com/your-username/employee-management-system.git

### Run Application

python main.py

---

## Menu Options

1. Add Employee
2. View Employees
3. Highest Salary
4. Search Employee
5. Delete Employee
6. Update Salary
7. Average Salary
8. Department Report
9. Mark Attendance
10. View Attendance
11. Export JSON
12. Top Performer
13. Dashboard
14. Exit

---

## Learning Outcomes

This project helps in learning:

* Python Programming
* Modular Architecture
* SQLite Database
* CRUD Operations
* Reporting Systems
* Data Analytics Concepts
* JSON Export
* Attendance Management
* GitHub Workflow
* Problem Solving

---

## Future Roadmap

### Version 3.0

* Employee Login System
* Admin Authentication
* Role-Based Access Control
* Password Encryption

### Version 4.0

* Salary History Tracking
* Leave Management System
* Employee Promotion Tracking
* Performance Analytics Dashboard

### Version 5.0

* Flask Web Application
* Responsive UI
* Employee Self-Service Portal
* REST API Integration

### Version 6.0

* Data Visualization Charts
* PDF Report Generation
* CSV Export
* Email Notifications

### Version 7.0

* AI-Powered Employee Analytics
* Attendance Prediction
* Employee Attrition Analysis
* HR Dashboard

---

## GitHub Workflow

git add .
git commit -m "Updated Employee Management System v2.0"
git push

---

## Author

Bavani.Ch

GitHub:
https://github.com/bavaniancapgemini-dev


## Version 8.0 – Recruitment & Onboarding Management

Added a complete recruitment and onboarding module.

### Job Opening Management
- Add, view, search and update job openings.
- Manage vacancies and job status.
- Close job openings.

### Candidate Management
- Register candidates.
- Search, update and delete candidate records.
- Store candidate skills, experience and resume paths.

### Job Application Tracking
- Apply candidates for available jobs.
- Track application statuses.
- Prevent duplicate applications.

### Interview Management
- Schedule interviews.
- Record interviewer details and feedback.
- Track interview results.
- Automatically update application status.

### Offer Management
- Create job offers.
- Manage offered salary and joining dates.
- Accept or decline offers.
- Update application status based on offer decisions.

### Onboarding Management
- Convert candidates with accepted offers into employees.
- Prevent duplicate candidate-to-employee conversion.
- Create onboarding tasks.
- Track task progress.
- View onboarding completion summaries.

### Database Tables
- job_openings
- candidates
- job_applications
- interviews
- recruitment_offers
- onboarding_tasks
- candidate_employee_links

### Dashboard Integration
- Added Recruitment & Onboarding Management to Admin Dashboard.
- Added Recruitment & Onboarding Management to HR Manager Dashboard.

Version 8.0 expands the system into a more complete employee lifecycle management application.


## Version 9.0 – Advanced HR Analytics & Reporting

### New Features

- Employee KPI dashboard
- Department-wise employee analytics
- Recruitment KPI dashboard
- Application status and interview analytics
- Hiring conversion analysis
- Attendance analytics
- Employee-wise attendance reports
- Leave management analytics
- Payroll cost analysis
- Monthly and yearly payroll reports
- Department-wise payroll expenses
- Salary component analysis
- Training completion analytics
- Course-wise training reports
- Performance rating analytics
- Department performance comparisons
- Advanced HR Analytics dashboard
- CSV report exports
- Master export for all analytics reports
- Admin and HR dashboard integration

### CSV Reports

The system can export the following reports:

1. Employee Analytics
2. Recruitment Analytics
3. Attendance Analytics
4. Leave Analytics
5. Payroll Analytics
6. Training Analytics
7. Performance Analytics

All reports are saved in the `exports` folder and can be opened in Microsoft Excel.

### Technologies Used

- Python
- SQLite
- SQL
- CSV
- VS Code
- Git and GitHub

### Project Version

**Current Version: 9.0**
