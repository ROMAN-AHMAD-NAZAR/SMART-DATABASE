# app.py

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Import the database query function
from Agent import get_answer_from_database

# --- Create the Flask App (remains the same) ---
app = Flask(__name__)
CORS(app)


# --- [CHANGE #2] ---
# The entire fake "your_sql_agent_function" is now GONE.
# We have deleted it because we will use the real one.

# --- Create the API Endpoint (remains mostly the same) ---
@app.route("/query", methods=["POST"])
def handle_query():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"success": False, "error": "Invalid request: 'query' key missing."}), 400

        user_input = data['query']

        # --- [CHANGE #3] - The Core Change ---
        # Instead of calling the fake function, we now call the real, imported function.
        # This will trigger your entire LangGraph agent.
        agent_answer = get_answer_from_database(user_input)

        # The rest of this function is the same.
        return jsonify({"success": True, "answer": agent_answer})

    except Exception as e:
        print(f"An error occurred in the Flask app: {e}")
        return jsonify({"success": False, "error": "An internal server error occurred."}), 500


# --- Serving the HTML page ---
@app.route("/")
def serve_page():
    """This function runs when someone goes to the main page."""
    return render_template("index.html")


# --- Health Check Endpoint ---
@app.route("/health")
def health_check():
    """Health check endpoint for monitoring and deployment verification."""
    import sqlite3
    try:
        # Check database connection
        conn = sqlite3.connect('cars.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM cars')
        car_count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "car_count": car_count,
            "version": "1.0.0"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


# --- Running the App ---
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # Binding to 0.0.0.0 is intentional for cloud deployment compatibility
    app.run(host='0.0.0.0', port=port, debug=debug)  # nosec B104