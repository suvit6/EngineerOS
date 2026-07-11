import base64
import hashlib
import hmac
import os
import secrets

from dotenv import load_dotenv
from psycopg import connect
from psycopg.errors import UniqueViolation

load_dotenv()


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    salt_b64 = base64.b64encode(salt).decode("utf-8")
    dk_b64 = base64.b64encode(dk).decode("utf-8")
    return f"pbkdf2_sha256$100000${salt_b64}${dk_b64}"


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt_b64, hash_b64 = stored_hash.split("$")
        if algorithm != "pbkdf2_sha256":
            return False

        salt = base64.b64decode(salt_b64.encode("utf-8"))
        stored_dk = base64.b64decode(hash_b64.encode("utf-8"))
        computed_dk = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, int(iterations)
        )
        return hmac.compare_digest(stored_dk, computed_dk)
    except Exception:
        return False


def create_user(email: str, password: str, full_name: str) -> tuple[bool, str]:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return False, "DATABASE_URL not set"

    password_hash = _hash_password(password)

    try:
        with connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (email, password_hash, full_name)
                    VALUES (%s, %s, %s)
                    """,
                    (email, password_hash, full_name),
                )
            conn.commit()
        return True, "User registered successfully"
    except UniqueViolation:
        return False, "Email already registered"
    except Exception as exc:
        return False, str(exc)


def authenticate_user(email: str, password: str) -> tuple[bool, str]:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return False, "DATABASE_URL not set"

    try:
        with connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT password_hash FROM users WHERE email = %s",
                    (email,),
                )
                row = cur.fetchone()

        if not row:
            return False, "Invalid email or password"

        stored_hash = row[0]
        if not _verify_password(password, stored_hash):
            return False, "Invalid email or password"

        return True, "Login successful"
    except Exception as exc:
        return False, str(exc)