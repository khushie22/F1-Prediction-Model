#!/usr/bin/env python3
"""
Quick Data Collection Script for F1 Singapore GP Prediction

This script runs all data collection processes in sequence:
1. Singapore GP results from FastF1
2. Historical data from Ergast API
3. Weather data collection
4. Data validation and analysis
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append('.')

from ergast_data_collector import ErgastDataCollector
from weather_data_collector import WeatherDataCollector
import pandas as pd
import fastf1

def main():
    """Run complete data collection process"""
    
    print("🏁 F1 Singapore GP Data Collection")
    print("=" * 50)
    
    # Set up data directory
    data_dir = Path("../data")
    data_dir.mkdir(exist_ok=True)
    
    # Enable FastF1 cache
    fastf1.Cache.enable_cache('../f1_cache')
    
    # Step 1: Collect historical data from Ergast API
    print("\n📊 Step 1: Collecting historical F1 data from Ergast API...")
    ergast_collector = ErgastDataCollector(data_dir)
    historical_data = ergast_collector.collect_all_data()
    
    # Step 2: Collect weather data
    print("\n🌤️ Step 2: Collecting weather data...")
    weather_collector = WeatherDataCollector(data_dir)
    weather_data = weather_collector.collect_weather_data()
    
    # Step 3: Collect Singapore GP results from FastF1 (if not already collected)
    print("\n🏁 Step 3: Collecting Singapore GP results from FastF1...")
    singapore_results = collect_singapore_fastf1(data_dir)
    
    # Step 4: Data validation and summary
    print("\n📋 Step 4: Data validation and summary...")
    validate_and_summarize(data_dir)
    
    print("\n✅ Data collection complete!")
    print(f"All data saved to: {data_dir.absolute()}")

def collect_singapore_fastf1(data_dir):
    """Collect Singapore GP results from FastF1"""
    singapore_results = []
    
    for year in range(2008, 2025):
        try:
            print(f"  Collecting {year} Singapore GP from FastF1...")
            
            session = fastf1.get_session(year, 'Singapore', 'R')
            session.load()
            
            results = session.results
            results['Year'] = year
            results['Race'] = 'Singapore'
            results['Date'] = session.date
            
            # Select relevant columns
            cols_to_keep = ['Year', 'Race', 'Date', 'Abbreviation', 'FullName', 'TeamName', 
                          'Position', 'Points', 'GridPosition', 'Status', 'Time', 'FastestLapTime']
            
            available_cols = [col for col in cols_to_keep if col in results.columns]
            results_subset = results[available_cols].copy()
            
            singapore_results.append(results_subset)
            
        except Exception as e:
            print(f"  Error collecting {year}: {e}")
            continue
    
    if singapore_results:
        all_results = pd.concat(singapore_results, ignore_index=True)
        output_path = data_dir / 'singapore_gp_results_fastf1_2008_2024.csv'
        all_results.to_csv(output_path, index=False)
        print(f"  Saved FastF1 Singapore GP results: {output_path}")
        return all_results
    
    return None

def validate_and_summarize(data_dir):
    """Validate collected data and provide summary"""
    
    data_files = list(data_dir.glob('*.csv'))
    
    print(f"\n📁 Collected {len(data_files)} data files:")
    
    total_records = 0
    for file in data_files:
        try:
            df = pd.read_csv(file)
            records = len(df)
            total_records += records
            size_mb = file.stat().st_size / 1024 / 1024
            
            print(f"  ✓ {file.name}: {records:,} records ({size_mb:.2f} MB)")
            
        except Exception as e:
            print(f"  ✗ {file.name}: Error reading file - {e}")
    
    print(f"\n📊 Total records collected: {total_records:,}")
    
    # Check for key data files
    key_files = [
        'singapore_gp_results_ergast_2008_2024.csv',
        'driver_standings_2015_2024.csv',
        'constructor_standings_2015_2024.csv',
        'singapore_weather_2008_2024.csv'
    ]
    
    print(f"\n🔍 Key data files status:")
    for key_file in key_files:
        file_path = data_dir / key_file
        if file_path.exists():
            print(f"  ✓ {key_file}")
        else:
            print(f"  ✗ {key_file} (missing)")

if __name__ == "__main__":
    main()
