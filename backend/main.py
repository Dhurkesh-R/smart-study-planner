from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
from scheduler import calculate_next_interval
from quiz_generator import QuizGenerator
from calendar_sync import create_study_event
from utils import (
    validate_input_keys,
    iso_datetime_now,
    format_study_session,
    to_title_case
)

app = Flask(__name__)
CORS(app)

model = joblib.load("../model/model.pkl")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Smart Study Planner API is live",
        "timestamp": iso_datetime_now()
    })

@app.route("/predict", methods=["POST"])
def predict_next_session():
    data = request.json
    required_keys = ["subject", "time_spent", "recall_score", "previous_interval"]
    missing = validate_input_keys(data, required_keys)
    if missing:
        return jsonify({"error": f"Missing key: {missing}"}), 400

    try:
        subject = to_title_case(data["subject"])
        time_spent = float(data["time_spent"])
        recall_score = float(data["recall_score"])
        previous_interval = float(data["previous_interval"])

        # Define all possible subjects
        all_subjects = ["Biology", "CS", "Chemistry", "Geography", "History", 
                        "Literature", "Math", "Physics"]

        # Create one-hot encoding for subjects
        subject_features = [1 if subject == s else 0 for s in all_subjects]
        if sum(subject_features) == 0:
            return jsonify({"error": f"Invalid subject: {subject}"}), 400

        # Construct full feature vector
        feature_vector = np.array([[time_spent, recall_score, previous_interval] + subject_features])
        prediction = model.predict(feature_vector)
        interval = round(float(prediction[0]), 2)

        return jsonify({
            "subject": subject,
            "next_study_interval": interval,
            "message": format_study_session(subject, int(interval)),
            "timestamp": iso_datetime_now()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/spaced", methods=["POST"])
def spaced_repetition():
    data = request.json
    missing = validate_input_keys(data, ["previous_interval", "recall_score"])
    if missing:
        return jsonify({"error": f"Missing key: {missing}"}), 400

    try:
        prev_int = float(data["previous_interval"])
        recall_score = float(data["recall_score"])
        interval = calculate_next_interval(prev_int, recall_score)

        return jsonify({
            "spaced_interval": interval,
            "timestamp": iso_datetime_now()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    topic = request.json.get("topic", "")
    if not topic:
        return jsonify({"error": "Topic required"}), 400

    question = QuizGenerator().generate_quiz_question(topic)
    return jsonify({
        "question": question,
        "timestamp": iso_datetime_now()
    })

@app.route("/schedule-session", methods=["POST"])
def schedule_session():
    data = request.json
    missing = validate_input_keys(data, ["subject", "start_time", "duration_minutes"])
    if missing:
        return jsonify({"error": f"Missing key: {missing}"}), 400

    try:
        subject = to_title_case(data["subject"])
        link = create_study_event(subject, data["start_time"], int(data["duration_minutes"]))

        return jsonify({
            "message": f"Event scheduled for {subject}.",
            "event_link": link,
            "timestamp": iso_datetime_now()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
