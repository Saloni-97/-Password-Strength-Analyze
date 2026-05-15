import re
 
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
 
common_passwords = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "password1", "111111", "123123", "admin", "letmein",
    "welcome", "monkey", "dragon", "iloveyou", "sunshine",
    "superman", "batman", "football", "shadow", "trustno1"
]
 
def check_password(password):
    score = 0
    feedback = []
 
    length = len(password)
 
    if length < 6:
        feedback.append("Your password is too short. Use at least 8 characters.")
    elif length < 8:
        feedback.append("Try to use at least 8 characters for better safety.")
        score += 1
    elif length < 12:
        score += 2
    else:
        score += 3
 
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add some lowercase letters (like a, b, c).")
 
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add some uppercase letters (like A, B, C).")
 
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add some numbers (like 1, 2, 3).")
 
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|,.<>?]', password):
        score += 2  
    else:
        feedback.append("Add special characters like @, #, $, or !.")
 
    if password.lower() in common_passwords:
        score = 0
        feedback.append("WARNING: This is one of the most common passwords. Change it!")
 
    if re.search(r'(.)\1\1', password):
        score -= 1
        feedback.append("Avoid repeating the same letter 3 times in a row (like 'aaa').")
 
    if re.search(r'(123|234|345|456|abc|bcd)', password.lower()):
        score -= 1
        feedback.append("Avoid easy sequences like '123' or 'abc'.")

