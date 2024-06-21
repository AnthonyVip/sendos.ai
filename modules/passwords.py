from passlib.context import CryptContext
import re


class PasswordEncrypt:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, password, hash):
        return self.pwd_context.verify(password, hash)

    def validated_pass(self, password: str):
        return True if re.fullmatch(
            r'[A-Za-z0-9!@#$%^&*()]+', password
        ) else False
