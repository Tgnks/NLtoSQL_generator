import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[3]
load_dotenv(ROOT / ".env")

CSV_PATH = ROOT / "NLtoSQL" / "credit_card_fraud_detection_2026-selected-columns.csv"
DATABASE_URL = os.getenv("DATABASE_URL")

CREATE_TABLE_SQL = """
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
    transaction_id          TEXT PRIMARY KEY,
    customer_id             TEXT NOT NULL,
    card_id                 TEXT NOT NULL,
    merchant_id             TEXT NOT NULL,
    transaction_datetime    TIMESTAMP NOT NULL,
    transaction_amount      NUMERIC(12, 2) NOT NULL,
    merchant_category       TEXT NOT NULL,
    merchant_country        TEXT NOT NULL,
    transaction_hour        INTEGER NOT NULL CHECK (transaction_hour BETWEEN 0 AND 23),
    transaction_day_of_week TEXT NOT NULL
);
"""


def main():
    if not DATABASE_URL:
        raise SystemExit("DATABASE_URL is not set in .env")

    df = pd.read_csv(CSV_PATH, parse_dates=["transaction_datetime"])
    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        for statement in CREATE_TABLE_SQL.split(";"):
            if statement.strip():
                conn.execute(text(statement))

    df.to_sql("transactions", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into transactions")


if __name__ == "__main__":
    main()