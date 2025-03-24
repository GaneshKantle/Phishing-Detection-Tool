#importing required libraries
from flask import Flask, request, render_template, jsonify
import numpy as np
import pickle
import warnings
from feature import FeatureExtraction
from email_feature import extract_email_features

warnings.filterwarnings('ignore')

# Load URL Phishing Detection Model
try:
    with open("model.pkl", "rb") as url_model_file:
        gbc = pickle.load(url_model_file)
except Exception as e:
    print(f"Error loading URL model: {e}")
    gbc = None

# Load Email Phishing Detection Model
try:
    with open("email_model.pkl", "rb") as email_model_file:
        email_model = pickle.load(email_model_file)
except Exception as e:
    print(f"Error loading Email model: {e}")
    email_model = None

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "url" in request.form and gbc:  # URL Phishing Detection
            url = request.form["url"]
            obj = FeatureExtraction(url)
            x = np.array(obj.getFeaturesList()).reshape(1, -1)  # Reshape to 1 row, n columns

            y_pred = gbc.predict(x)[0]
            y_pro_phishing = gbc.predict_proba(x)[0, 0]
            y_pro_non_phishing = gbc.predict_proba(x)[0, 1]

            pred = "It is {0:.2f}% safe to go.".format(y_pro_phishing * 100)
            return render_template(
                "index.html",
                xx=round(y_pro_non_phishing, 2),
                url=url,
                email_result=None,
                email_confidence=None
            )

        elif "email_data" in request.form and email_model:  # Email Phishing Detection
            email_content = request.form["email_data"].strip()
            if not email_content:
                return jsonify({"error": "Email content cannot be empty."})

            email_features = extract_email_features(email_content)
            email_prediction = email_model.predict([email_features])[0]
            email_proba = email_model.predict_proba([email_features])[0, 1]

            email_result = (
                "✅ This email is likely SAFE."
                if email_prediction == 0
                else "⚠️ This email is PHISHING."
            )
            email_confidence = "Confidence: {0:.2f}%".format(email_proba * 100)

            return jsonify({
                "email_result": email_result,
                "email_confidence": email_confidence
            })

    return render_template("index.html", xx=-1, email_result=None, email_confidence=None)


if __name__ == "__main__":
    app.run(debug=True)
