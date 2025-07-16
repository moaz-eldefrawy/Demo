#!/usr/bin/env python3
"""
User management module with intentional bugs for demonstration.
"""

import hashlib
import sqlite3
import json
from typing import Dict, List, Optional

class UserManager:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT,
                is_admin INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash a password using MD5 (insecure)."""
        # Bug 6: Security vulnerability - using MD5 instead of secure hash
        return hashlib.md5(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, email: str, is_admin: bool = False) -> bool:
        """Create a new user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Fixed: Use parameterized query to prevent SQL injection
            query = "INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (username, self.hash_password(password), email, 1 if is_admin else 0))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Bug 8: Security vulnerability - SQL injection
            query = f"SELECT password FROM users WHERE username = '{username}'"
            cursor.execute(query)
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                stored_password = result[0]
                # Bug 9: Logic error - incorrect password comparison
                return stored_password == password  # Should compare hashed passwords
            return False
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return False
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Bug 10: Security vulnerability - SQL injection
            query = f"SELECT id, username, email, is_admin FROM users WHERE username = '{username}'"
            cursor.execute(query)
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'is_admin': bool(result[3])
                }
            return None
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None
    
    def update_user_email(self, username: str, new_email: str) -> bool:
        """Update user email."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Bug 11: Security vulnerability - SQL injection
            query = f"UPDATE users SET email = '{new_email}' WHERE username = '{username}'"
            cursor.execute(query)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user email: {e}")
            return False
    
    def delete_user(self, username: str) -> bool:
        """Delete a user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Bug 12: Security vulnerability - SQL injection
            query = f"DELETE FROM users WHERE username = '{username}'"
            cursor.execute(query)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def get_all_users(self) -> List[Dict]:
        """Get all users (admin only)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, username, email, is_admin FROM users")
            results = cursor.fetchall()
            
            conn.close()
            
            users = []
            for result in results:
                users.append({
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'is_admin': bool(result[3])
                })
            
            return users
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

def main():
    """Test the user manager with the bugs."""
    user_mgr = UserManager(":memory:")  # Use in-memory database for testing
    
    print("Testing UserManager...")
    
    # Test user creation
    success = user_mgr.create_user("testuser", "password123", "test@example.com")
    print(f"User creation: {success}")
    
    # Test authentication
    auth = user_mgr.authenticate_user("testuser", "password123")
    print(f"Authentication: {auth}")
    
    # Test getting user info
    user_info = user_mgr.get_user_info("testuser")
    print(f"User info: {user_info}")
    
    # Test SQL injection vulnerability
    malicious_input = "'; DROP TABLE users; --"
    user_mgr.create_user(malicious_input, "password", "test@example.com")
    print("SQL injection test completed")

if __name__ == "__main__":
    main()