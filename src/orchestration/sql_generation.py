def generate_sql(context):
    """
    Generates an SQL query based on the provided context.

    Parameters:
    context (dict): A dictionary containing the necessary information to generate the SQL query.
                    Expected keys include 'table', 'fields', 'conditions', and 'order_by'.

    Returns:
    str: The generated SQL query.
    """
    table = context.get('table')
    fields = context.get('fields', '*')
    conditions = context.get('conditions', '')
    order_by = context.get('order_by', '')

    sql_query = f"SELECT {fields} FROM {table}"

    if conditions:
        sql_query += f" WHERE {conditions}"

    if order_by:
        sql_query += f" ORDER BY {order_by}"

    sql_query += ";"
    
    return sql_query

def main():
    # Example context for SQL generation
    context = {
        'table': 'customers',
        'fields': 'id, name, email',
        'conditions': 'active = 1',
        'order_by': 'name ASC'
    }

    sql = generate_sql(context)
    print(sql)

if __name__ == "__main__":
    main()