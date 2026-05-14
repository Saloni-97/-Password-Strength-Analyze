"""
"""

import re
import getpass
import sys
import os

#  ANSI Color Codes

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    RED     = "\033[91m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    WHITE   = "\033[97m"
    GREY    = "\033[90m"

#  Common / Weak Passwords Blacklist

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123",
    "password1", "111111", "123123", "admin", "letmein",
    "welcome", "monkey", "dragon", "master", "sunshine",
    "princess", "password123", "iloveyou", "1234567890",
    "qwertyuiop", "superman", "batman", "football", "baseball",
    "shadow", "michael", "jennifer", "thomas", "jordan",
    "hunter", "ranger", "harley", "rangers", "trustno1",
}


#  Analysis Engine

def analyse_password(password: str) -> dict:
    """
    Analyse a password and return a detailed report dict.
    """
    length = len(password)

    # --- Character-class checks ---
    has_lower   = bool(re.search(r'[a-z]', password))
    has_upper   = bool(re.search(r'[A-Z]', password))
    has_digit   = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?`~]', password))

    # --- Pattern / weakness checks ---
    is_common        = password.lower() in COMMON_PASSWORDS
    has_repeat_chars = bool(re.search(r'(.)\1{2,}', password))          # aaa, 111 …
    has_seq_digits   = bool(re.search(r'(012|123|234|345|456|567|678|789|890)', password))
    has_seq_letters  = bool(re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk'
                                      r'|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst'
                                      r'|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()))
    has_keyboard_run = bool(re.search(r'(qwerty|asdf|zxcv|qwer|asdfgh|zxcvbn)', password.lower()))
    is_all_digits    = password.isdigit()
    is_all_alpha     = password.isalpha()

    # Scoring
    score = 0

    # Length scoring
    if length >= 8:  score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    if length >= 20: score += 1

    # Character diversity
    if has_lower:   score += 1
    if has_upper:   score += 1
    if has_digit:   score += 1
    if has_special: score += 2   # special chars are worth more

    # Entropy bonus: unique character ratio
    unique_ratio = len(set(password)) / max(length, 1)
    if unique_ratio > 0.7: score += 1
    if unique_ratio > 0.9: score += 1

    # Penalties
    if is_common:        score -= 5
    if has_repeat_chars: score -= 1
    if has_seq_digits:   score -= 1
    if has_seq_letters:  score -= 1
    if has_keyboard_run: score -= 2
    if is_all_digits:    score -= 2
    if is_all_alpha:     score -= 1
    if length < 6:       score -= 3

    # Clamp score to 0–10
    score = max(0, min(score, 10))

    #  Strength label
    if score >= 9:
        strength = "Very Strong"
        color    = Color.GREEN
        bar_fill = 5
    elif score >= 7:
        strength = "Strong"
        color    = Color.CYAN
        bar_fill = 4
    elif score >= 5:
        strength = "Moderate"
        color    = Color.YELLOW
        bar_fill = 3
    elif score >= 3:
        strength = "Weak"
        color    = Color.RED
        bar_fill = 2
    else:
        strength = "Very Weak"
        color    = Color.RED + Color.BOLD
        bar_fill = 1

    # Suggestions 
    suggestions = []
    if is_common:
        suggestions.append(" This is an extremely common password — never use it.")
    if length < 8:
        suggestions.append(" Use at least 8 characters (12+ recommended).")
    elif length < 12:
        suggestions.append(" Consider extending to 12+ characters for better security.")
    if not has_upper:
        suggestions.append(" Add uppercase letters (A–Z).")
    if not has_lower:
        suggestions.append(" Add lowercase letters (a–z).")
    if not has_digit:
        suggestions.append(" Include numbers (0–9).")
    if not has_special:
        suggestions.append(" Add special characters (e.g. @, #, $, !, %).")
    if has_repeat_chars:
        suggestions.append(" Avoid repeating the same character 3+ times in a row.")
    if has_seq_digits or has_seq_letters:
        suggestions.append(" Avoid sequential patterns like '123' or 'abc'.")
    if has_keyboard_run:
        suggestions.append("  Avoid keyboard runs like 'qwerty' or 'asdf'.")
    if is_all_digits:
        suggestions.append("  A number-only password is very easy to crack.")
    if is_all_alpha:
        suggestions.append("  A letters-only password is weaker — mix in digits & symbols.")
    if not suggestions:
        suggestions.append(" Great password! No obvious weaknesses detected.")

    return {
        "password"       : password,
        "length"         : length,
        "score"          : score,
        "strength"       : strength,
        "color"          : color,
        "bar_fill"       : bar_fill,
        "has_lower"      : has_lower,
        "has_upper"      : has_upper,
        "has_digit"      : has_digit,
        "has_special"    : has_special,
        "is_common"      : is_common,
        "has_repeat"     : has_repeat_chars,
        "has_seq_digits" : has_seq_digits,
        "has_seq_letters": has_seq_letters,
        "has_kb_run"     : has_keyboard_run,
        "unique_chars"   : len(set(password)),
        "unique_ratio"   : round(unique_ratio, 2),
        "suggestions"    : suggestions,
    }


#  Display Helpers

SEGMENTS = 5   # total bar segments

def strength_bar(fill: int, color: str) -> str:
    filled = "█" * fill
    empty  = "░" * (SEGMENTS - fill)
    return f"{color}{Color.BOLD}{filled}{Color.RESET}{Color.GREY}{empty}{Color.RESET}"


def check_icon(flag: bool) -> str:
    return f"{Color.GREEN}✔{Color.RESET}" if flag else f"{Color.RED}✘{Color.RESET}"


def print_report(r: dict) -> None:
    c  = r["color"]
    w  = 54   # box width

    print()
    print(f"{Color.BOLD}{Color.WHITE}┌{'─'*w}┐{Color.RESET}")
    print(f"{Color.BOLD}{Color.WHITE}│{'PASSWORD STRENGTH REPORT':^{w}}│{Color.RESET}")
    print(f"{Color.BOLD}{Color.WHITE}└{'─'*w}┘{Color.RESET}")
    print()

    # Strength bar
    bar = strength_bar(r["bar_fill"], c)
    label = f"{c}{Color.BOLD}{r['strength']}{Color.RESET}"
    print(f"  Strength  :  {bar}  {label}")
    print(f"  Score     :  {c}{Color.BOLD}{r['score']} / 10{Color.RESET}")
    print(f"  Length    :  {Color.WHITE}{r['length']} characters{Color.RESET}")
    print(f"  Unique    :  {Color.WHITE}{r['unique_chars']} unique chars "
          f"({int(r['unique_ratio']*100)}% diversity){Color.RESET}")
    print()

    # Character checks table
    print(f"  {Color.BOLD}{Color.WHITE}{'CHARACTER ANALYSIS':─<{w-4}}{Color.RESET}")
    checks = [
        ("Lowercase letters (a–z)", r["has_lower"]),
        ("Uppercase letters (A–Z)", r["has_upper"]),
        ("Numeric digits   (0–9)", r["has_digit"]),
        ("Special symbols  (!@#…)", r["has_special"]),
    ]
    for label, flag in checks:
        print(f"    {check_icon(flag)}  {label}")
    print()

    # Pattern detection
    print(f"  {Color.BOLD}{Color.WHITE}{'PATTERN DETECTION':─<{w-4}}{Color.RESET}")
    patterns = [
        ("Common/blacklisted password",    not r["is_common"]),
        ("Repeated characters (aaa…)",     not r["has_repeat"]),
        ("Sequential digits (123…)",       not r["has_seq_digits"]),
        ("Sequential letters (abc…)",      not r["has_seq_letters"]),
        ("Keyboard runs (qwerty…)",        not r["has_kb_run"]),
    ]
    for label, safe in patterns:
        icon = f"{Color.GREEN}✔{Color.RESET}" if safe else f"{Color.RED}✘{Color.RESET}"
        status = f"{Color.GREEN}PASS{Color.RESET}" if safe else f"{Color.RED}FAIL{Color.RESET}"
        print(f"    {icon}  {label:<38} {status}")
    print()

    # Suggestions
    print(f"  {Color.BOLD}{Color.WHITE}{'RECOMMENDATIONS':─<{w-4}}{Color.RESET}")
    for tip in r["suggestions"]:
        print(f"    {tip}")
    print()
    print(f"  {Color.GREY}{'─'*w}{Color.RESET}")
    print()


#  Main Interactive Loop
# ─────────────────────────────────────────────────
def banner() -> None:
    print(f"""
{Color.CYAN}{Color.BOLD}
 ██████╗  █████╗ ███████╗███████╗
 ██╔══██╗██╔══██╗██╔════╝██╔════╝
 ██████╔╝███████║███████╗███████╗
 ██╔═══╝ ██╔══██║╚════██║╚════██║
 ██║     ██║  ██║███████║███████║
 ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
{Color.RESET}{Color.WHITE}      Password Strength Analyzer v1.0
      Cybersecurity Assessment Tool
{Color.GREY}      ─────────────────────────────{Color.RESET}
""")


def main() -> None:
    # Disable colors if output is not a terminal
    if not sys.stdout.isatty():
        for attr in vars(Color):
            if not attr.startswith("__"):
                setattr(Color, attr, "")

    banner()
    print(f"  {Color.GREY}Type your password to analyse it.")
    print(f"  Input is hidden while you type.")
    print(f"  Enter {Color.WHITE}quit{Color.GREY} or press Ctrl+C to exit.{Color.RESET}")
    print()

    while True:
        try:
            # Attempt hidden input; fall back to visible on Windows CI / non-tty
            try:
                pwd = getpass.getpass(
                    prompt=f"  {Color.BOLD}{Color.WHITE}Enter password: {Color.RESET}"
                )
            except Exception:
                pwd = input(f"  {Color.BOLD}{Color.WHITE}Enter password: {Color.RESET}")

            if pwd.strip().lower() in ("quit", "exit", "q"):
                print(f"\n  {Color.CYAN}Stay secure. Goodbye!{Color.RESET}\n")
                break

            if not pwd:
                print(f"  {Color.YELLOW}⚠  Please enter a password to analyse.{Color.RESET}\n")
                continue

            report = analyse_password(pwd)
            print_report(report)

            again = input(f"  {Color.GREY}Analyse another password? (y/n): {Color.RESET}").strip().lower()
            print()
            if again not in ("y", "yes"):
                print(f"  {Color.CYAN}Stay secure. Goodbye!{Color.RESET}\n")
                break

        except KeyboardInterrupt:
            print(f"\n\n  {Color.CYAN}Stay secure. Goodbye!{Color.RESET}\n")
            break


if __name__ == "__main__":
    main()
