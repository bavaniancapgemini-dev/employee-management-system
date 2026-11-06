from database import create_table
from auth import create_auth_table, create_account
from getpass import getpass


# Initialize database tables
create_table()
create_auth_table()

print("\n===================================")
print("       CREATE ADMIN ACCOUNT")
print("===================================")

username = input("Admin Username: ").strip()

password = getpass("Admin Password: ")
confirm_password = getpass("Confirm Password: ")

if not username:
    print("Username cannot be empty.")

elif len(password) < 8:
    print("Password must contain at least 8 characters.")

elif password != confirm_password:
    print("Passwords do not match.")

else:

    success, message = create_account(
        username,
        password,
        "Admin"
    )

    print(message)