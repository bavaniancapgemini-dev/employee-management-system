
import sqlite3
import hashlib
import secrets


def create_auth_table():

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_accounts(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL,
            employee_id INTEGER,
            status TEXT DEFAULT 'Active',
            created_on TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    """)

    connection.commit()
    connection.close()


def hash_password(password, salt):

    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        200000
    ).hex()


def create_account(username, password, role, employee_id=None):

    allowed_roles = ["Admin", "HR Manager", "Employee"]

    if role not in allowed_roles:
        return False, "Invalid role."

    salt = secrets.token_hex(16)

    password_hash = hash_password(password, salt)

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO user_accounts
            (username, password_hash, salt, role, employee_id)
            VALUES (?, ?, ?, ?, ?)
        """, (username, password_hash, salt, role, employee_id))

        connection.commit()
        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "Username already exists."

    finally:

        connection.close()


def login_user(username, password):

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, password_hash, salt, role, employee_id, status
        FROM user_accounts
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    connection.close()

    if not user:
        return None

    user_id, stored_hash, salt, role, employee_id, status = user

    if status != "Active":
        return None

    entered_hash = hash_password(password, salt)

    if secrets.compare_digest(entered_hash, stored_hash):

        return {
            "id": user_id,
            "username": username,
            "role": role,
            "employee_id": employee_id
        }

    return None


def change_account_password(username, new_password):

    salt = secrets.token_hex(16)
    password_hash = hash_password(new_password, salt)

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE user_accounts
        SET password_hash = ?, salt = ?
        WHERE username = ?
    """, (password_hash, salt, username))

    connection.commit()
    updated = cursor.rowcount
    connection.close()

    return updated > 0


def update_account_status(user_id, status):

    if status not in ["Active", "Inactive"]:
        return False

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE user_accounts
        SET status = ?
        WHERE id = ?
    """, (status, user_id))

    connection.commit()
    updated = cursor.rowcount
    connection.close()

    return updated > 0


def view_accounts():

    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username, role, employee_id, status, created_on
        FROM user_accounts
        ORDER BY id
    """)

    accounts = cursor.fetchall()
    connection.close()

    return accounts
