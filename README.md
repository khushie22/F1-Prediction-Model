# 🏁 F1 Singapore GP Winner Predictor

A machine learning project that predicts the winner of the 2025 Singapore Grand Prix using comprehensive historical F1 data analysis.

## 🎯 Project Overview

This project uses machine learning to predict F1 race winners by analyzing:
- **Historical Performance**: Singapore GP results from 2008-2024
- **Driver Statistics**: Track-specific performance, consistency, and recent form
- **Team Performance**: Constructor standings, reliability, and car characteristics
- **Environmental Factors**: Weather conditions, track characteristics, and race dynamics

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd f1-singapore-predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Data Collection
```bash
cd src
python run_data_collection.py
```

### 3. Train Model and Generate Predictions
```bash
# Open Jupyter notebook
jupyter notebook notebooks/feature_engineering.ipynb
# Run all cells to train models and generate predictions
```

### 4. Launch Web Application
```bash
python run_webapp.py
# Open browser to http://localhost:5000
```

## 📊 Features

### Data Collection
- **FastF1 API**: Real-time F1 data and race results
- **Ergast API**: Historical championship standings and statistics
- **Weather Data**: Singapore climate patterns and race conditions
- **Automated Caching**: Efficient data storage and retrieval

### Machine Learning Models
- **Random Forest**: Ensemble method for robust predictions
- **XGBoost**: Gradient boosting for complex pattern recognition
- **Logistic Regression**: Linear baseline model
- **Support Vector Machine**: Non-linear classification
- **Model Selection**: Automatic best model selection based on F1-score

### Feature Engineering
- **Driver Features**: Singapore GP history, recent form, consistency metrics
- **Team Features**: Constructor performance, reliability, car characteristics
- **Track Features**: Circuit specifications, overtaking difficulty, tire degradation
- **Weather Features**: Temperature, humidity, precipitation impact
- **Temporal Features**: Season progression, championship pressure

### Web Application
- **Interactive Dashboard**: Visual predictions with probability bars
- **Driver Details**: Individual driver analysis and statistics
- **Team Analysis**: Constructor performance comparison
- **Feature Importance**: Model interpretability and insights
- **Responsive Design**: Mobile-friendly interface


## 🔧 Technical Details

### Dependencies
- **Python 3.8+**
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning algorithms
- **fastf1**: F1 data API
- **flask**: Web application framework
- **xgboost**: Gradient boosting
- **matplotlib/seaborn**: Data visualization

### Versioning Large Files
If you plan to version model artifacts and large arrays, install Git LFS and track them:
```bash
git lfs install
git lfs track "*.pkl"
git lfs track "*.npy"
git lfs track "data/**/*.csv"
git add .gitattributes
```

### Model Performance
The model is evaluated using multiple metrics:
- **Accuracy**: Overall prediction correctness
- **Precision**: True positive rate for winner predictions
- **Recall**: Sensitivity to actual winners
- **F1-Score**: Harmonic mean of precision and recall
- **AUC**: Area under the ROC curve

### Data Sources
- **Ergast API**: Free F1 historical data (no API key required)
- **FastF1**: Official F1 timing data and telemetry
- **Weather APIs**: Singapore climate data
- **Synthetic Data**: Fallback for missing historical data

## 📈 Usage Examples

### Generate Predictions
```python
# Load trained model
import joblib
model = joblib.load('data/features/best_model.pkl')

# Make predictions for 2025 Singapore GP
predictions = model.predict_proba(X_2025)
```

### Web API
```bash
# Get all predictions
curl http://localhost:5000/api/predictions

# Get feature importance
curl http://localhost:5000/api/feature-importance
```

## ⚠️ Limitations

- Predictions based on historical data only
- Does not account for unexpected events (crashes, technical issues)
- Weather conditions are estimated from historical averages
- Driver transfers between seasons may affect accuracy
- Not suitable for betting or gambling purposes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please respect F1's intellectual property and terms of service when using their data.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section in `src/DATA_COLLECTION_README.md`
2. Verify all dependencies are installed correctly
3. Ensure you have internet connectivity for data collection
4. Review error messages for specific guidance

## 🏆 Disclaimer

This is a machine learning experiment for educational purposes. F1 is unpredictable, and many factors can influence race outcomes that are not captured in historical data. Predictions should not be used for betting or gambling.

