#!/usr/bin/env python3
"""
Run the F1 Singapore GP Prediction Web Application

This script starts the Flask web application for viewing predictions.
Make sure to run the feature engineering notebook first to generate the model and predictions.
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'data/features/best_model.pkl',
        'data/features/feature_scaler.pkl',
        'data/features/label_encoders.pkl',
        'data/features/singapore_gp_2025_predictions.csv',
        'data/features/feature_importance.csv',
        'data/features/prediction_summary.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n💡 Please run the feature engineering notebook first:")
        print("   jupyter notebook src/feature_engineering.ipynb")
        return False
    
    return True

def main():
    """Main function to run the web application"""
    print("🏁 F1 Singapore GP Prediction Web Application")
    print("=" * 50)
    
    # Check if required files exist
    if not check_requirements():
        sys.exit(1)
    
    print("✅ All required files found!")
    print("\n🚀 Starting web application...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Change to webapp directory and run Flask app
    os.chdir('webapp')
    os.system('python app.py')

if __name__ == "__main__":
    main()
