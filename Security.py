# Geraldine Whitaker
# This file authenticates and authorizes user via username and password for admin and customer role based access

import hashlib
from dataclasses import dataclass
from typing import Dict


# Store the information for an authenticated user.
@dataclass
class User:
    username: str
    role: str


# Convert a password string into an SHA-256 hash.
def hash_password_sha256(password: str):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# Store password hashes instead of plain passwords.
class AuthSystem:
    def __init__(self):
        self.user: Dict[str, dict] = {
            "admin": {
                "role": "admin",
                "password_hash": hash_password_sha256("AdminPass")
            },
            "customer": {
                "role": "customer",
                "password_hash": hash_password_sha256("CustomerPass")
            }
        }

    # Verify username/password and return the User object if correct
    def authenticate(self, username: str, password: str):
        username = username.strip()

        record = self.user.get(username)
        if not record:
            return

        # Hash the entered password and compare to stored hash
        attempt_hash = hash_password_sha256(password)
        if attempt_hash == record["password_hash"]:
            return User(username=username, role=record["role"])

        return

    # Prompt user to login and exit program after 3 failed attempts.
    def login_prompt(self, max_attempts: int = 3):
        print("\n--- Login Required ---")

        for attempt in range(1, max_attempts + 1):
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            user = self.authenticate(username, password)
            if user:
                print(f"\nLogin successful. Role: {user.role}\n")
                return user

            remaining = max_attempts - attempt
            print(f"Invalid credentials. Attempts remaining: {remaining}\n")

        print("Too many failed login attempts.")
        return
