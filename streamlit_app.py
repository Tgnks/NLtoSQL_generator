import os
import re
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
MODEL_NAME = "openai/gpt-oss-120b"

SCHEMA = """
Table: transactions
Columns:
- transaction_id (TEXT, primary key)
- customer_id (TEXT)
- card_id (TEXT)
- merchant_id (TEXT)
- transaction_datetime (TIMESTAMP)
- transaction_amount (NUMERIC)
- merchant_category (TEXT), e.g. 'Online Retail', 'Gas Station', 'Healthcare & Pharmacy'
- merchant_country (TEXT), e.g. 'USA', 'UK', 'Germany'
- transaction_hour (INTEGER, 0-23)
- transaction_day_of_week (TEXT, e.g. 'Monday')
"""

SYSTEM_PROMPT = (
    "You are an expert PostgreSQL query generator. Convert the user's question "
    "into one read-only SELECT statement against the table below. "
    "Use only the listed columns. Return only the SQL, with no markdown and no explanation.\n"
    + SCHEMA
)

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|attach|copy)\b",
    re.IGNORECASE,
)


def generate_sql(question: str) -> str:
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    sql = response.choices[0].message.content.strip()
    return sql.strip("`").replace("sql\n", "", 1).strip()


def is_safe(sql: str) -> bool:
    cleaned = sql.strip().rstrip(";")
    if ";" in cleaned:
        return False
    if not cleaned.lower().startswith("select"):
        return False
    return not FORBIDDEN.search(cleaned)


@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)


st.title("Credit Card Transactions: Ask in Plain English")
st.write("Ask a question about the transactions. The app generates SQL, runs it, and shows the results.")

question = st.text_input("Your question", placeholder="e.g. Total spend by merchant country in January")

if st.button("Generate and Run"):
    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY is missing from .env")
    elif not DATABASE_URL:
        st.error("DATABASE_URL is missing from .env")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating SQL..."):
            try:
                sql = generate_sql(question)
            except Exception as e:
                st.error(f"Groq error: {e}")
                st.stop()

        st.subheader("Generated SQL")
        st.code(sql, language="sql")

        if not is_safe(sql):
            st.error("Blocked: only a single read-only SELECT statement is allowed.")
        else:
            try:
                with get_engine().connect() as conn:
                    df = pd.read_sql(text(sql.rstrip(";")), conn)
                st.subheader("Results")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Query error: {e}")