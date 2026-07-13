import joblib
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from train_model import train_and_save_model

app = Flask(__name__)

MODEL_PATH = Path(__file__).with_name("model.joblib")

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)
else:
    train_and_save_model()
    model = joblib.load(MODEL_PATH)

FEATURE_NAMES = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not trained yet. Run train_model.py first."}), 500

    payload = request.get_json(silent=True) or {}
    try:
        features = [float(payload[name]) for name in FEATURE_NAMES]
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Please provide all four measurements."}), 400

    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    classes = model.classes_

    top_index = int(probabilities.argmax())
    top_class = classes[top_index]
    confidence = float(probabilities[top_index] * 100)

    return jsonify(
        {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "classes": [str(item) for item in classes],
            "probabilities": [round(float(p) * 100, 2) for p in probabilities],
        }
    )


if __name__ == "__main__":
    host = "127.0.0.1"
    port = int(os.environ.get("PORT", 5000))
    print(f"Open this URL in your browser: http://{host}:{port}", flush=True)
    app.run(debug=True, host=host, port=port, use_reloader=False)
