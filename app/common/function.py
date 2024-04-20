import re


# 패스워드 생성규칙
def password_validation(password) -> bool:
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-+=]).{8,}$", password))