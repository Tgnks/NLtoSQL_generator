from flask import Flask, request, jsonify
from api_gateway.authentication import authenticate_user
from api_gateway.session_management import SessionManager
from orchestration.intent_classification import classify_intent
from orchestration.query_understanding import understand_query
from orchestration.retrieval.semantic_search import semantic_search
from orchestration.retrieval.vector_search import vector_search
from orchestration.retrieval.hybrid_search import hybrid_search
from orchestration.context_selection import select_context
from orchestration.sql_generation import generate_sql
from orchestration.sql_validation import validate_sql
from orchestration.error_correction import correct_errors
from orchestration.response_generation import generate_response

app = Flask(__name__)
session_manager = SessionManager()

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = authenticate_user(data['username'], data['password'])
    if user:
        return jsonify({"message": "Login successful", "token": user['token']}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/session', methods=['POST'])
def create_session():
    session_id = session_manager.create_session()
    return jsonify({"session_id": session_id}), 201

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.json
    session_id = data.get('session_id')
    user_query = data.get('query')

    session_manager.retrieve_session(session_id)
    intent = classify_intent(user_query)
    entities = understand_query(user_query)
    context = select_context(semantic_search(user_query), vector_search(user_query), hybrid_search(user_query))
    sql_query = generate_sql(context)
    
    if validate_sql(sql_query):
        response = generate_response(sql_query)
        return jsonify(response), 200
    else:
        corrected_sql = correct_errors(sql_query)
        response = generate_response(corrected_sql)
        return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)