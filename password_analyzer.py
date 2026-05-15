# Password Strength Analyzer
# Made by: [Your Name]

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
        score += 2  # special characters are worth more points
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

    # keep score between 0 and 10
    score = max(0, min(score, 10))

    return score, feedback


def show_result(password, score, feedback):

    print()
    print("=" * 45)
    print("         YOUR PASSWORD REPORT")
    print("=" * 45)

    print(f"\n  Password Length : {len(password)} characters")
    print(f"  Score          : {score} out of 10")

    bar = "[" + "#" * score + "-" * (10 - score) + "]"

    if score >= 8:
        color    = GREEN
        strength = "VERY STRONG  :)"
    elif score >= 6:
        color    = BLUE
        strength = "STRONG"
    elif score >= 4:
        color    = YELLOW
        strength = "MODERATE"
    else:
        color    = RED
        strength = "WEAK  :("

    print(f"  Strength Bar   : {color}{bar}{RESET}")
    print(f"  Strength Level : {color}{strength}{RESET}")

    print()
    print("  What your password contains:")

    if re.search(r'[a-z]', password):
        print(f"  {GREEN}[YES]{RESET} Lowercase letters")
    else:
        print(f"  {RED}[NO] {RESET} Lowercase letters")

    if re.search(r'[A-Z]', password):
        print(f"  {GREEN}[YES]{RESET} Uppercase letters")
    else:
        print(f"  {RED}[NO] {RESET} Uppercase letters")

    if re.search(r'[0-9]', password):
        print(f"  {GREEN}[YES]{RESET} Numbers")
    else:
        print(f"  {RED}[NO] {RESET} Numbers")

    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|,.<>?]', password):
        print(f"  {GREEN}[YES]{RESET} Special characters (!@#...)")
    else:
        print(f"  {RED}[NO] {RESET} Special characters (!@#...)")

    if feedback:
        print()
        print("  Tips to make it stronger:")
        for tip in feedback:
            print(f"  {YELLOW}  -> {tip}{RESET}")
    else:
        print()
        print(f"  {GREEN}  Great job! No weaknesses found!{RESET}")

    print()
    print("=" * 45)
    print()


def main():

    print()
    print("=" * 45)
    print("     PASSWORD STRENGTH ANALYZER")
    print("     Check how strong your password is!")
    print("=" * 45)
    print()
    print("  Type 'quit' at any time to exit.")
    print()

    while True:

        password = input("  Enter a password to check: ")

        if password.lower() == "quit":
            print()
            print("  Thanks for using the analyzer. Stay safe!")
            print()
            break

        if password == "":
            print(f"\n  {YELLOW}Oops! You didn't type anything. Try again.{RESET}\n")
            continue

        score, feedback = check_password(password)
        show_result(password, score, feedback)

        again = input("  Want to check another password? (yes / no): ")
        print()

        if again.lower() not in ("yes", "y"):
            print("  Thanks for using the analyzer. Stay safe!")
            print()
            break


if __name__ == "__main__":
    main()
