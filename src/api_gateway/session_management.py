from flask import session, jsonify
import uuid
import time

class SessionManager:
    def create_session(self, user_id):
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        session['user_id'] = user_id
        session['created_at'] = time.time()
        return session_id

    def get_session(self):
        return {
            'session_id': session.get('session_id'),
            'user_id': session.get('user_id'),
            'created_at': session.get('created_at')
        }

    def terminate_session(self):
        session.clear()
        return jsonify({"message": "Session terminated successfully."}), 200

session_manager = SessionManager()