"""
F1 Singapore GP Prediction Web Application

A Flask web app that displays predictions for the 2025 Singapore Grand Prix
based on historical data and machine learning models.
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import os

app = Flask(__name__)

# Load model and data
def load_model_and_data():
    """Load the trained model and prediction data"""
    try:
        # Paths
        features_dir = Path('../data/features')
        
        # Load model
        model = joblib.load(features_dir / 'best_model.pkl')
        
        # Load scaler and encoders
        scaler = joblib.load(features_dir / 'feature_scaler.pkl')
        label_encoders = joblib.load(features_dir / 'label_encoders.pkl')
        
        # Load predictions
        predictions_df = pd.read_csv(features_dir / 'singapore_gp_2025_predictions.csv')
        
        # Load feature importance
        feature_importance_df = pd.read_csv(features_dir / 'feature_importance.csv')
        
        # Load prediction summary
        summary_df = pd.read_csv(features_dir / 'prediction_summary.csv')
        
        return {
            'model': model,
            'scaler': scaler,
            'label_encoders': label_encoders,
            'predictions': predictions_df,
            'feature_importance': feature_importance_df,
            'summary': summary_df.iloc[0].to_dict()
        }
    except Exception as e:
        print(f"Error loading model and data: {e}")
        return None

# Load data on startup
model_data = load_model_and_data()

@app.route('/')
def index():
    """Main page showing predictions"""
    if model_data is None:
        return render_template('error.html', 
                             error="Model data not found. Please run the feature engineering notebook first.")
    
    # Get top 10 predictions
    top_predictions = model_data['predictions'].head(10)
    
    # Get team analysis
    team_analysis = model_data['predictions'].groupby('Team').agg({
        'Win_Probability': 'sum',
        'Driver': 'count'
    }).sort_values('Win_Probability', ascending=False)
    team_analysis.columns = ['Total_Win_Probability', 'Drivers']
    
    return render_template('index.html',
                         predictions=top_predictions,
                         team_analysis=team_analysis,
                         summary=model_data['summary'])

@app.route('/api/predictions')
def api_predictions():
    """API endpoint for predictions data"""
    if model_data is None:
        return jsonify({'error': 'Model data not found'}), 500
    
    return jsonify({
        'predictions': model_data['predictions'].to_dict('records'),
        'summary': model_data['summary']
    })

@app.route('/api/feature-importance')
def api_feature_importance():
    """API endpoint for feature importance data"""
    if model_data is None:
        return jsonify({'error': 'Model data not found'}), 500
    
    return jsonify(model_data['feature_importance'].to_dict('records'))

@app.route('/driver/<driver_code>')
def driver_detail(driver_code):
    """Driver detail page"""
    if model_data is None:
        return render_template('error.html', 
                             error="Model data not found. Please run the feature engineering notebook first.")
    
    # Find driver in predictions
    driver_data = model_data['predictions'][
        model_data['predictions']['Driver'] == driver_code.upper()
    ]
    
    if driver_data.empty:
        return render_template('error.html', 
                             error=f"Driver {driver_code} not found in predictions.")
    
    driver_info = driver_data.iloc[0]
    
    return render_template('driver_detail.html', driver=driver_info)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
