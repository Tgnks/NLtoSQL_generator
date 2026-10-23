def validate_input(data):
    # Check if the required fields are present
    required_fields = ['user_id', 'query']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    # Validate user_id format (assuming it should be an integer)
    if not isinstance(data['user_id'], int):
        return False, "user_id must be an integer"

    # Validate query format (assuming it should be a non-empty string)
    if not isinstance(data['query'], str) or not data['query'].strip():
        return False, "query must be a non-empty string"

    return True, "Validation successful"

def validate_sql_query(sql_query):
    # Basic validation for SQL query (this can be expanded as needed)
    if not isinstance(sql_query, str) or not sql_query.strip():
        return False, "SQL query must be a non-empty string"

    # Here you could add more complex validation logic, such as checking for SQL injection patterns

    return True, "SQL query validation successful"