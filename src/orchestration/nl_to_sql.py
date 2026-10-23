import re

from groq import Groq

from src.config import GROQ_API_KEY, GROQ_MODEL

SCHEMA = """
Table: transactions
Columns:
- transaction_id (VARCHAR, primary key)
- customer_id (VARCHAR)
- card_id (VARCHAR)
- merchant_id (VARCHAR)
- transaction_datetime (DATETIME)
- transaction_amount (DECIMAL)
- merchant_category (VARCHAR), e.g. 'Online Retail', 'Gas Station', 'Healthcare & Pharmacy'
- merchant_country (VARCHAR), e.g. 'USA', 'UK', 'Germany'
- transaction_hour (INT, 0-23)
- transaction_day_of_week (VARCHAR, e.g. 'Monday')
"""

SYSTEM_PROMPT = (
    "You are an expert MySQL query generator. Convert the user's question "
    "into one read-only SELECT statement against the table below. "
    "Use only the listed columns. Return only the SQL, with no markdown and no explanation.\n"
    + SCHEMA
)

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|rename|replace|"
    r"exec|execute|call|set|into|load_file|outfile|dumpfile|sleep|benchmark|"
    r"information_schema|lock|unlock)\b",
    re.IGNORECASE,
)

_FENCE_RE = re.compile(r"```(?:sql)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)

_client: Groq | None = None


def extract_sql(raw: str) -> str:
    """Return SQL from a model reply, removing markdown fences if present."""
    raw = raw or ""
    match = _FENCE_RE.search(raw)
    sql = match.group(1) if match else raw
    return sql.strip()


def _get_client() -> Groq:
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is missing from .env")
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def _ask(messages: list[dict]) -> str:
    response = _get_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0,
    )
    return extract_sql(response.choices[0].message.content or "")


def generate_sql_from_question(question: str) -> str:
    return _ask([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ])


def correct_sql(question: str, failed_sql: str, error_message: str) -> str:
    """Ask the model to fix a query that failed."""
    return _ask([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
        {"role": "assistant", "content": failed_sql},
        {
            "role": "user",
            "content": (
                f"That query failed with this error: {error_message}\n"
                "Return a corrected single read-only SELECT statement only."
            ),
        },
    ])


def is_safe_sql(sql: str) -> bool:
    """Allow only a single read-only SELECT with no comments."""
    if not isinstance(sql, str):
        return False
    cleaned = sql.strip().rstrip(";").strip()
    if not cleaned or ";" in cleaned:
        return False
    if any(marker in cleaned for marker in ("--", "/*", "#")):
        return False
    if not re.match(r"select\b", cleaned, re.IGNORECASE):
        return False
    return FORBIDDEN.search(cleaned) is None
