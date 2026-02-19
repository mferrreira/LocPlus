import os


def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://locplus:locplus@postgres:5432/locplus",
    )
