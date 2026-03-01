import pickle
import numpy as np
try:
    with open('RF_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded.")
    # test inference with 14 features (same as app.py uses)
    dummy_features = [0.5, 1, 0.5, 0.5, 0.5, 0.5, 0, 0, 1, 0.5, 0, 1, 0, 0]
    pred = model.predict([dummy_features])
    print(f"Prediction success! Result: {pred[0]}")
except Exception as e:
    print(f"Error: {e}")
