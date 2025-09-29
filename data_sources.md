## Data Sources and Provenance

This project aggregates historical racing, timing, and weather data to build features and predictions for the Singapore Grand Prix.

### Primary Sources
- Ergast Developer API — historical F1 results and standings (no API key required)
  - Docs: https://ergast.com/mrd/
  - License: Free for non‑commercial use; see site terms
- FastF1 — timing data, telemetry, session info (cached locally)
  - Docs: https://theoehrly.github.io/Fast-F1/
  - Data usage subject to F1/Formula One Management terms
- Weather data — historical Singapore weather
  - Source file: `data/singapore_weather_2008_2024.csv`
  - Include original source/citation if externally obtained

### Local Cache and Artifacts
- FastF1 cache: `f1_cache/` (auto-populated by FastF1 on first load)
- Processed feature artifacts: `data/features/`
  - `best_model.pkl`, `feature_scaler.pkl`, `label_encoders.pkl`
  - `combined_features.csv`, `feature_importance.csv`, `prediction_summary.csv`
  - Train/test arrays: `X_*_scaled.npy`, `y_*_winner.npy`

### Reproduce / Refresh Data
1. Create and activate virtual environment; install dependencies from `requirements.txt`.
2. Collect raw/base data:
   - Ergast and FastF1 collectors in `src/`:
     - `python src/run_data_collection.py`
     - Refer to `src/DATA_COLLECTION_README.md` for troubleshooting
   - Weather: ensure `data/singapore_weather_2008_2024.csv` exists or update fetch script in `src/weather_data_collector.py`.
3. Generate features and models:
   - Open notebook: `notebooks/feature_engineering.ipynb`
   - Run all cells to produce artifacts in `data/features/`
4. Launch web app:
   - `python run_webapp.py` (checks required artifacts and starts Flask app)

### Data Quality and Caveats
- Missing sessions/years may be backfilled via nearest seasons or excluded.
- Weather values are historical averages; race‑day variability isn’t fully captured.
- Ensure consistency of driver/team naming across seasons before encoding.

### Versioning and Large Files
- Large artifacts under `data/features/` and `f1_cache/` are ignored by Git via `.gitignore`.
- If you need to version selected large files, enable Git LFS and track `*.pkl`, `*.npy`, and specific CSVs.

### Ethical and Legal Notes
- Use of timing and telemetry data should respect the terms of the respective rights holders.
- This repository is for educational use; do not redistribute proprietary datasets.


