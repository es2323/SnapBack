from flask import Blueprint, request, jsonify
from models.game_session import GameSession

main = Blueprint('main', __name__)

@main.route('/submit_score', methods=['POST'])
def submit_score():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_email = data.get('user_email')
        reaction_time = data.get('reaction_time')

        if user_email is None or reaction_time is None:
            return jsonify({"error": "Missing user_email or reaction_time"}), 400

        # Simple fatigue score calculation
        fatigue_score = max(0, 100 - reaction_time // 10)

        # Save to database using your OOP model
        session = GameSession(user_email=user_email, fatigue_score=fatigue_score)
        session.save_to_db()

        return jsonify({"message": "Score submitted successfully."}), 200

    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500
