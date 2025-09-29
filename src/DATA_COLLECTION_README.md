# F1 Singapore GP Data Collection Guide

This guide explains how to collect comprehensive historical F1 data for predicting the Singapore Grand Prix winner.

## 🎯 What Data We Collect

### 1. Singapore GP Results (2008-2024)
- **Source**: FastF1 API + Ergast API
- **Data**: Race results, positions, points, fastest laps, grid positions
- **Files**: 
  - `singapore_gp_results_ergast_2008_2024.csv`
  - `singapore_gp_results_fastf1_2008_2024.csv`

### 2. Driver Performance (2015-2024)
- **Source**: Ergast API
- **Data**: Championship standings, points, wins, consistency metrics
- **File**: `driver_standings_2015_2024.csv`

### 3. Constructor Performance (2015-2024)
- **Source**: Ergast API
- **Data**: Team standings, points, wins, car performance trends
- **File**: `constructor_standings_2015_2024.csv`

### 4. Weather Data (2008-2024)
- **Source**: FastF1 API + Synthetic data
- **Data**: Temperature, humidity, precipitation, wind, conditions
- **File**: `singapore_weather_2008_2024.csv`

### 5. Circuit Information
- **Source**: Ergast API
- **Data**: Track characteristics, location, specifications
- **File**: `circuits_info.csv`

### 6. Season Schedules (2015-2024)
- **Source**: Ergast API
- **Data**: Race calendar, dates, locations
- **File**: `season_schedules_2015_2024.csv`

## 🚀 How to Run Data Collection

### Option 1: Run Everything at Once
```bash
cd src
python run_data_collection.py
```

### Option 2: Run Individual Components

#### Using Jupyter Notebook
```bash
cd src
jupyter notebook data_collection.ipynb
```
Then run each cell in sequence.

#### Using Python Scripts
```bash
cd src

# Collect historical data from Ergast API
python ergast_data_collector.py

# Collect weather data
python weather_data_collector.py
```

## 📊 Data Collection Process

### Step 1: Setup
- Install required packages: `pip install -r requirements.txt`
- Enable FastF1 cache for faster subsequent runs
- Create data directory structure

### Step 2: Historical Data Collection
- **Ergast API**: Free, no API key required
- **Rate Limiting**: Built-in delays to be respectful
- **Error Handling**: Continues if individual years fail

### Step 3: Weather Data Collection
- **FastF1**: Primary source for weather data
- **Synthetic Data**: Fallback for missing years
- **Climate Patterns**: Based on Singapore's tropical climate

### Step 4: Data Validation
- Check data completeness
- Validate data quality
- Generate summary statistics

## 🔧 Configuration

### FastF1 Cache
```python
fastf1.Cache.enable_cache('../f1_cache')
```

### Data Directory
```python
data_dir = Path('../data')
```

### Rate Limiting
- Ergast API: 0.5 second delay between requests
- FastF1: 1 second delay between sessions

## 📈 Expected Data Volumes

| Data Type | Records | File Size |
|-----------|---------|-----------|
| Singapore GP Results | ~340 | ~50 KB |
| Driver Standings | ~200 | ~30 KB |
| Constructor Standings | ~100 | ~20 KB |
| Weather Data | ~17 | ~5 KB |
| Circuit Info | ~80 | ~10 KB |
| Season Schedules | ~200 | ~30 KB |

**Total**: ~850 records, ~145 KB

## 🐛 Troubleshooting

### Common Issues

1. **FastF1 Connection Errors**
   - Check internet connection
   - Verify FastF1 installation: `pip install fastf1`
   - Clear cache if corrupted

2. **Ergast API Timeouts**
   - Increase timeout values
   - Check internet connection
   - API is free but may have rate limits

3. **Missing Data**
   - Some years may not have complete data
   - Synthetic data fills gaps for weather
   - Check data validation output

### Data Quality Checks

```python
# Check for missing data
df.isnull().sum()

# Check data types
df.dtypes

# Check for duplicates
df.duplicated().sum()
```

## 📋 Data Schema

### Singapore GP Results
- `Year`: Race year
- `DriverCode`: 3-letter driver code
- `Position`: Final race position
- `Points`: Points scored
- `GridPosition`: Starting position
- `ConstructorName`: Team name
- `Time`: Race time
- `Status`: Finish status

### Driver Standings
- `Year`: Championship year
- `Position`: Final championship position
- `Points`: Total points
- `Wins`: Number of wins
- `DriverCode`: Driver identifier

### Weather Data
- `Year`: Race year
- `Temperature_Avg_C`: Average temperature
- `Humidity_Percent`: Humidity percentage
- `Precipitation_mm`: Rainfall amount
- `Weather_Condition`: Weather description
