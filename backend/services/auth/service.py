import os

from dotenv import load_dotenv
from psycopg import connect
from psycopg.errors import UniqueViolation

load_dotenv()


def create_user(email: str, password_hash: str, full_name: str) -> tuple[bool, str]:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return False, "DATABASE_URL not set"

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