"""
app.py
------
A small Flask web app that predicts salary using our trained neural network.

Pages / endpoints:
    GET  /            -> a simple form in the browser
    POST /predict     -> reads the form and shows the prediction
    POST /api/predict -> JSON in, JSON out  (for programs, not people)
    GET  /health      -> says "ok" (used to check the server is alive)
"""

import torch
from flask import Flask, request, jsonify, render_template_string

from model import load_model

app = Flask(__name__)

# Load the trained model ONCE when the server starts.
model = load_model()


# A simple HTML page with a form. {{ ... }} spots get filled in by Flask.
PAGE = """
<!doctype html>
<title>Salary Predictor</title>
<body style="font-family: sans-serif; max-width: 420px; margin: 40px auto;">
  <h1>Salary Predictor</h1>
  <p>A tiny neural network that guesses salary from years of experience.</p>

  <form method="post" action="/predict">
    Years of experience:
    <input type="number" name="experience" step="0.5" min="0" value="5">
    <button type="submit">Predict</button>
  </form>

  {% if salary %}
    <h2>Predicted salary: Rs {{ "{:,.0f}".format(salary) }}</h2>
  {% endif %}
</body>
"""


def predict_salary(experience):
    """Give the model one number and get the salary in rupees back."""
    x = torch.tensor([[float(experience)]])
    with torch.no_grad():
        salary_in_thousands = model(x).item()
    return salary_in_thousands * 1000


@app.route("/")
def index():
    return render_template_string(PAGE, salary=None)


@app.route("/predict", methods=["POST"])
def predict_form():
    experience = request.form["experience"]
    salary = predict_salary(experience)
    return render_template_string(PAGE, salary=salary)


@app.route("/api/predict", methods=["POST"])
def predict_api():
    data = request.get_json()
    salary = predict_salary(data["experience"])
    return jsonify({"experience": data["experience"], "salary": round(salary)})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # For running on your own computer. On the server we use gunicorn instead.
    app.run(host="0.0.0.0", port=8080, debug=True)
