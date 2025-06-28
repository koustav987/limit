from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Global variables for model and data
model = None
sample_data = None
feature_info = {}

def load_or_train_model():
    """Load existing model or train a new one with sample data"""
    global model, sample_data, feature_info
    
    # Check if model file exists
    if os.path.exists('crop_yield_model.pkl'):
        try:
            model = joblib.load('crop_yield_model.pkl')
            print("✅ Loaded existing model")
            return True
        except:
            print("❌ Failed to load existing model, will train new one")
    
    # Create sample dataset for demonstration
    np.random.seed(42)
    n_samples = 1000
    
    areas = ['Punjab', 'Haryana', 'Uttar Pradesh', 'Maharashtra', 'Karnataka', 
             'Rajasthan', 'Gujarat', 'Madhya Pradesh', 'Bihar', 'West Bengal']
    crops = ['Wheat', 'Rice', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 
             'Barley', 'Mustard', 'Gram', 'Groundnut']
    soil_types = ['Loamy', 'Clay', 'Sandy', 'Black', 'Red', 'Alluvial']
    
    data = {
        'Area': np.random.choice(areas, n_samples),
        'Crop': np.random.choice(crops, n_samples),
        'Soil_Type': np.random.choice(soil_types, n_samples),
        'Temperature': np.random.normal(25, 5, n_samples),
        'Humidity': np.random.normal(65, 15, n_samples),
        'PH': np.random.normal(6.5, 1, n_samples),
        'Annual_Rainfall': np.random.normal(800, 200, n_samples),
    }
    
    # Create yield based on features (synthetic relationship)
    df = pd.DataFrame(data)
    
    # Create synthetic yield based on features
    yield_base = 2000
    df['Yield'] = (
        yield_base +
        (df['Temperature'] - 25) * 50 +
        (df['Humidity'] - 65) * 10 +
        (df['PH'] - 6.5) * 200 +
        (df['Annual_Rainfall'] - 800) * 2 +
        np.random.normal(0, 300, n_samples)
    )
    
    # Ensure positive yields
    df['Yield'] = np.maximum(df['Yield'], 100)
    
    sample_data = df
    
    # Store feature information
    feature_info = {
        'areas': sorted(df['Area'].unique().tolist()),
        'crops': sorted(df['Crop'].unique().tolist()),
        'soil_types': sorted(df['Soil_Type'].unique().tolist()),
        'temperature_range': [float(df['Temperature'].min()), float(df['Temperature'].max())],
        'humidity_range': [float(df['Humidity'].min()), float(df['Humidity'].max())],
        'ph_range': [float(df['PH'].min()), float(df['PH'].max())],
        'rainfall_range': [float(df['Annual_Rainfall'].min()), float(df['Annual_Rainfall'].max())]
    }
    
    # Train model
    target = 'Yield'
    X = df.drop(target, axis=1)
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    categorical_cols = X.select_dtypes(include='object').columns.tolist()
    numerical_cols = X.select_dtypes(include=np.number).columns.tolist()
    
    preprocessor = ColumnTransformer([
        ('ohe', OneHotEncoder(handle_unknown='ignore', drop='first'), categorical_cols),
        ('scale', StandardScaler(), numerical_cols)
    ])
    
    # Train multiple models and select best
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    best_r2 = -float('inf')
    best_model = None
    
    for name, model_algo in models.items():
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', model_algo)
        ])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        
        if r2 > best_r2:
            best_r2 = r2
            best_model = pipeline
    
    model = best_model
    
    # Save model
    joblib.dump(model, 'crop_yield_model.pkl')
    print("✅ Model trained and saved")
    return True

@app.route('/')
def home():
    return jsonify({
        "message": "Crop Yield Prediction API",
        "status": "active",
        "endpoints": {
            "/predict": "POST - Make yield predictions",
            "/features": "GET - Get available feature options",
            "/health": "GET - Health check"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

@app.route('/features')
def get_features():
    """Get available options for categorical features and ranges for numerical features"""
    if not feature_info:
        return jsonify({"error": "Feature information not available"}), 500
    
    return jsonify(feature_info)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['Area', 'Crop', 'Soil_Type', 'Temperature', 'Humidity', 'PH', 'Annual_Rainfall']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
        
        # Create input DataFrame
        input_df = pd.DataFrame([data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            "predicted_yield": float(round(prediction, 2)),
            "input_data": data,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/bulk_predict', methods=['POST'])
def bulk_predict():
    try:
        data = request.get_json()
        
        if not data or 'predictions' not in data:
            return jsonify({"error": "No prediction data provided"}), 400
        
        predictions_input = data['predictions']
        
        if not isinstance(predictions_input, list):
            return jsonify({"error": "Predictions must be a list"}), 400
        
        results = []
        
        for i, pred_data in enumerate(predictions_input):
            try:
                input_df = pd.DataFrame([pred_data])
                prediction = model.predict(input_df)[0]
                results.append({
                    "id": i,
                    "predicted_yield": float(round(prediction, 2)),
                    "input_data": pred_data,
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "id": i,
                    "error": str(e),
                    "input_data": pred_data,
                    "status": "error"
                })
        
        return jsonify({
            "results": results,
            "total_predictions": len(results),
            "successful_predictions": len([r for r in results if r["status"] == "success"])
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Crop Yield Prediction API...")
    
    # Load or train model
    if load_or_train_model():
        print("🌱 Model ready for predictions!")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize model")