#!/usr/bin/env python3
"""
Simple calculator module with intentional bugs for demonstration.
"""

import math
import re

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        """Add two numbers."""
        result = a + b  # Fixed: Changed from a - b to a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def divide(self, a, b):
        """Divide a by b."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def calculate_expression(self, expression):
        """Calculate a mathematical expression from string."""
        # Bug 3: Security vulnerability - eval() without sanitization
        try:
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
        except Exception as e:
            return f"Error: {e}"
    
    def get_history(self):
        """Get calculation history."""
        return self.history
    
    def clear_history(self):
        """Clear calculation history."""
        # Bug 4: Performance issue - inefficient list clearing
        for i in range(len(self.history)):
            self.history.pop(0)  # Should use self.history.clear()
    
    def validate_input(self, value):
        """Validate numeric input."""
        # Bug 5: Logic error - incorrect validation
        if isinstance(value, (int, float)):
            return True
        if isinstance(value, str):
            # This regex is too permissive and allows dangerous input
            return bool(re.match(r'.*', value))  # Should be more restrictive
        return False

def main():
    calc = Calculator()
    
    # Test the bugs
    print("Testing calculator...")
    
    # Test Bug 1: Incorrect addition
    result = calc.add(5, 3)
    print(f"5 + 3 = {result}")  # Will print 2 instead of 8
    
    # Test Bug 2: Division by zero
    try:
        result = calc.divide(10, 0)
        print(f"10 / 0 = {result}")  # Will crash
    except ZeroDivisionError:
        print("Division by zero error caught")
    
    # Test Bug 3: Dangerous eval
    result = calc.calculate_expression("__import__('os').system('echo dangerous')")
    print(f"Eval result: {result}")
    
    # Test Bug 4: Inefficient history clearing
    calc.clear_history()
    
    # Test Bug 5: Incorrect validation
    is_valid = calc.validate_input("'; DROP TABLE users; --")
    print(f"Is '; DROP TABLE users; --' valid? {is_valid}")

if __name__ == "__main__":
    main()