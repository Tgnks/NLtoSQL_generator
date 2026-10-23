def validate_sql_query(sql_query):
    """
    Validates the generated SQL query for syntax correctness and safety.

    Args:
        sql_query (str): The SQL query to validate.

    Returns:
        bool: True if the query is valid, False otherwise.
    """
    # Basic syntax checks (this can be expanded with more sophisticated checks)
    if not sql_query.strip().lower().startswith("select"):
        return False

    # Additional checks can be implemented here (e.g., checking for SQL injection patterns)

    return True

def sanitize_sql_query(sql_query):
    """
    Sanitizes the SQL query to prevent SQL injection attacks.

    Args:
        sql_query (str): The SQL query to sanitize.

    Returns:
        str: The sanitized SQL query.
    """
    # Implement sanitization logic here (e.g., escaping special characters)
    return sql_query.replace("'", "''")  # Simple example of escaping single quotes

def validate_and_sanitize_query(sql_query):
    """
    Validates and sanitizes the SQL query.

    Args:
        sql_query (str): The SQL query to validate and sanitize.

    Returns:
        tuple: A tuple containing a boolean indicating validity and the sanitized query.
    """
    is_valid = validate_sql_query(sql_query)
    sanitized_query = sanitize_sql_query(sql_query)
    return is_valid, sanitized_query