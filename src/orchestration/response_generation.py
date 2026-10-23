from flask import jsonify

def generate_response(sql_results, user_query):
    """
    Generates a response based on SQL query results and user interactions.

    Args:
        sql_results (list): The results obtained from executing the SQL query.
        user_query (str): The original user query for context.

    Returns:
        dict: A structured response containing the results and any additional information.
    """
    if not sql_results:
        return {
            "status": "error",
            "message": "No results found for your query.",
            "query": user_query
        }

    return {
        "status": "success",
        "message": "Query executed successfully.",
        "query": user_query,
        "results": sql_results
    }