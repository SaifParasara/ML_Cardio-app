import pickle
import os

models = ['DT_model.pkl', 'LR_Model.pkl', 'RF_model.pkl', 'cardio_model.pkl']

for m in models:
    if os.path.exists(m):
        print(f"--- Loading {m} ---")
        try:
            with open(m, 'rb') as f:
                data = pickle.load(f)
            print(f"Type: {type(data)}")
            if isinstance(data, dict):
                print(f"Keys: {data.keys()}")
            elif hasattr(data, 'get_params'):
                print(f"Params: {data.get_params()}")
            if hasattr(data, 'classes_'):
                print(f"Classes: {data.classes_}")
            if hasattr(data, 'feature_importances_'):
                print(f"Has feature_importances_: Yes")
            if hasattr(data, 'coef_'):
                print(f"Has coef_: Yes")
        except Exception as e:
            print(f"Error loading {m}: {e}")
    else:
        print(f"File {m} not found.")
