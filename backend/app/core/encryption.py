from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("FERNET_SECRET_KEY")
fernet = Fernet(SECRET_KEY.encode())

def encrypt_token(token: str) -> str:
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    return fernet.decrypt(encrypted_token.encode()).decode()