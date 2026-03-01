from flask import Flask, render_template, request
import pickle
import numpy as np
import warnings
from datetime import datetime

# Initialize the Flask App
app = Flask(__name__)

# Load the models with exception handling to prevent unbound errors
model = None
scaler = None

try:
    with open('RF_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
except FileNotFoundError as fnf_error:
    print(f"Startup Warning: Could not load model files. Error: {fnf_error}")
except Exception as e:
    print(f"Startup Warning: Unexpected error loading models: {e}")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/evaluation')
def evaluation():
    return render_template('evaluation.html')


@app.route('/predict', methods=['POST'])
def predict():
    summary = {}
    try:
        if model is None or scaler is None:
            raise RuntimeError("The model or scaler files are missing. Backend cannot process predictions.")

        # Capture Data using .get() for safety
        user_name = request.form.get('name', 'Guest Patient')
        
        # User updated frontend to pass Age in Years. Model expects Age in Days.
        raw_age_years = request.form.get('age', '0').strip() or '0'
        raw_age_years = float(raw_age_years)
        raw_age_days = raw_age_years * 365.25
        
        gender_val = int(request.form.get('gender', 0))
        height = float(request.form.get('height', 0) or 0)
        weight = float(request.form.get('weight', 0) or 0)
        ap_hi = float(request.form.get('ap_hi', 0) or 0)
        ap_lo = float(request.form.get('ap_lo', 0) or 0)
        
        smoke = 1 if request.form.get('smoke') else 0
        alco = 1 if request.form.get('alco') else 0
        active = 1 if request.form.get('active') else 0
        chol_val = int(request.form.get('chol', 1))
        gluc_val = int(request.form.get('gluc', 1))
        
        # BMI Calculation
        bmi_calc = weight / ((height / 100) ** 2) if height > 0 else 0
        
        # Build Summary for the Report
        summary = {
            "Patient Name": user_name,
            "Age": f"{int(raw_age_years)} Years",
            "Gender": "Male" if gender_val == 2 else "Female",
            "Blood Pressure": f"{int(ap_hi)}/{int(ap_lo)} mmHg",
            "BMI": round(bmi_calc, 2),
            "Cholesterol": ["Normal", "Above Normal", "High"][chol_val-1],
            "Glucose": ["Normal", "Above Normal", "High"][gluc_val-1],
            "Lifestyle": f"{'Smoker' if smoke else 'Non-Smoker'}, {'Active' if active else 'Sedentary'}"
        }

        # Scaling numericals using a warning catch to suppress the lack of feature names complaint
        to_be_scaled = np.array([[raw_age_days, height, weight, ap_hi, ap_lo, bmi_calc]])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            scaled_values = scaler.transform(to_be_scaled)[0]

        # Construct final 14-feature vector
        features = [
            scaled_values[0], gender_val, scaled_values[1], scaled_values[2],
            scaled_values[3], scaled_values[4], smoke, alco, active,
            scaled_values[5], 
            1 if chol_val == 2 else 0, 1 if chol_val == 3 else 0,
            1 if gluc_val == 2 else 0, 1 if gluc_val == 3 else 0
        ]

        # Prediction - using Best Model (Gradient Boosting)
        prediction = model.predict([features])[0]
        
        return render_template('predict.html', 
                               prediction=prediction, 
                               summary=summary, 
                               now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    except Exception as e:
        return render_template('predict.html', 
                               error=str(e), 
                               summary=summary,
                               now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


import os

if __name__ == "__main__":
    # Get port from environment variables, defaults to 5000 
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 and disable debug mode for production
    app.run(host="0.0.0.0", port=port, debug=False)