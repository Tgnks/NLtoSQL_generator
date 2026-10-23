import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Load environment variables from the project root.
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


def get_database_url() -> str:
    """Return the configured database URL."""
    url = os.getenv("DATABASE_URL")

    if not url:
        raise ValueError(
            "DATABASE_URL is missing. Check the .env file "
            "in the project root."
        )

    return url


def get_engine() -> Engine:
    """Create a SQLAlchemy engine for MySQL."""
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={"connect_timeout": 10},
    )


def check_connection() -> dict:
    """Test connectivity and return basic database information."""
    engine = get_engine()

    try:
        with engine.connect() as connection:
            database_name = connection.execute(
                text("SELECT DATABASE()")
            ).scalar_one()

            transaction_count = connection.execute(
                text("SELECT COUNT(*) FROM transactions")
            ).scalar_one()

            return {
                "status": "success",
                "database": database_name,
                "transaction_count": transaction_count,
            }
    finally:
        engine.dispose()


if __name__ == "__main__":
    print(check_connection())