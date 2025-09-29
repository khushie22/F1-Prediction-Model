"""
Weather Data Collector for F1 Singapore GP Prediction

This script collects historical weather data for Singapore GP races:
- Temperature, humidity, precipitation
- Wind speed and direction
- Atmospheric pressure
- Weather conditions during race times
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

class WeatherDataCollector:
    def __init__(self, data_dir="../data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Singapore coordinates
        self.singapore_lat = 1.3521
        self.singapore_lon = 103.8198
        
        # OpenWeatherMap API (free tier available)
        # You'll need to get a free API key from https://openweathermap.org/api
        self.weather_api_key = None  # Set this if you want to use OpenWeatherMap
        
    def get_historical_weather_openweathermap(self, date, api_key=None):
        """Get historical weather data from OpenWeatherMap (requires API key)"""
        if not api_key:
            print("OpenWeatherMap API key not provided. Skipping OpenWeatherMap data.")
            return None
            
        # Convert date to timestamp
        timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp())
        
        url = f"http://history.openweathermap.org/data/2.5/history/city"
        params = {
            'lat': self.singapore_lat,
            'lon': self.singapore_lon,
            'type': 'hour',
            'start': timestamp,
            'end': timestamp + 86400,  # 24 hours
            'appid': api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting weather data for {date}: {e}")
            return None
    
    def get_weather_from_fastf1(self, year):
        """Get weather data from FastF1 (if available)"""
        try:
            import fastf1
            
            # Get Singapore GP session
            session = fastf1.get_session(year, 'Singapore', 'R')
            session.load()
            
            # Get weather data
            weather_data = session.weather_data
            
            if weather_data is not None and not weather_data.empty:
                # Add year and race info
                weather_data['Year'] = year
                weather_data['Race'] = 'Singapore'
                weather_data['Date'] = session.date
                
                return weather_data
            else:
                print(f"No weather data available for {year} Singapore GP")
                return None
                
        except Exception as e:
            print(f"Error getting FastF1 weather data for {year}: {e}")
            return None
    
    def create_synthetic_weather_data(self, years):
        """Create synthetic weather data based on Singapore's climate patterns"""
        print("Creating synthetic weather data based on Singapore climate patterns...")
        
        weather_data = []
        
        # Singapore climate characteristics (September - typical Singapore GP month)
        # Temperature: 24-32°C, Humidity: 70-90%, Rain probability: 40-60%
        
        for year in years:
            # Singapore GP is typically in September
            race_date = f"{year}-09-22"  # Approximate date
            
            # Generate realistic weather data
            np.random.seed(year)  # For reproducible results
            
            # Temperature (Celsius)
            temp_min = np.random.normal(26, 2)
            temp_max = np.random.normal(31, 2)
            temp_avg = (temp_min + temp_max) / 2
            
            # Humidity (%)
            humidity = np.random.normal(80, 10)
            humidity = max(60, min(95, humidity))  # Clamp to realistic range
            
            # Precipitation (mm)
            precipitation = np.random.exponential(5)  # Most days have little rain, some have more
            
            # Wind speed (km/h)
            wind_speed = np.random.exponential(8)
            wind_speed = min(25, wind_speed)  # Singapore rarely has very strong winds
            
            # Wind direction (degrees)
            wind_direction = np.random.uniform(0, 360)
            
            # Atmospheric pressure (hPa)
            pressure = np.random.normal(1013, 10)
            
            # Weather condition
            if precipitation > 10:
                condition = "Rain"
            elif precipitation > 2:
                condition = "Light Rain"
            elif humidity > 85:
                condition = "Humid"
            else:
                condition = "Clear"
            
            weather_record = {
                'Year': year,
                'Race': 'Singapore',
                'Date': race_date,
                'Temperature_Min_C': round(temp_min, 1),
                'Temperature_Max_C': round(temp_max, 1),
                'Temperature_Avg_C': round(temp_avg, 1),
                'Humidity_Percent': round(humidity, 1),
                'Precipitation_mm': round(precipitation, 1),
                'Wind_Speed_kmh': round(wind_speed, 1),
                'Wind_Direction_deg': round(wind_direction, 0),
                'Pressure_hPa': round(pressure, 1),
                'Weather_Condition': condition,
                'Data_Source': 'Synthetic'
            }
            
            weather_data.append(weather_record)
        
        return pd.DataFrame(weather_data)
    
    def collect_weather_data(self, years=None, use_fastf1=True, use_synthetic=True):
        """Collect weather data from multiple sources"""
        if years is None:
            years = list(range(2008, 2025))  # Singapore GP years
        
        print(f"Collecting weather data for Singapore GP years: {years}")
        
        all_weather_data = []
        
        # Try to get data from FastF1 first
        if use_fastf1:
            print("Attempting to collect weather data from FastF1...")
            for year in years:
                try:
                    weather_df = self.get_weather_from_fastf1(year)
                    if weather_df is not None:
                        all_weather_data.append(weather_df)
                        print(f"✓ Collected FastF1 weather data for {year}")
                    else:
                        print(f"✗ No FastF1 weather data for {year}")
                except Exception as e:
                    print(f"✗ Error collecting FastF1 weather data for {year}: {e}")
        
        # If we don't have enough data, create synthetic data
        if use_synthetic and len(all_weather_data) < len(years) * 0.5:  # Less than 50% coverage
            print("Creating synthetic weather data to fill gaps...")
            synthetic_data = self.create_synthetic_weather_data(years)
            all_weather_data.append(synthetic_data)
        
        # Combine all weather data
        if all_weather_data:
            combined_weather = pd.concat(all_weather_data, ignore_index=True)
            
            # Remove duplicates (keep FastF1 data over synthetic if both exist)
            combined_weather = combined_weather.drop_duplicates(subset=['Year'], keep='first')
            
            # Save to CSV
            output_path = self.data_dir / 'singapore_weather_2008_2024.csv'
            combined_weather.to_csv(output_path, index=False)
            print(f"Saved weather data: {output_path}")
            print(f"Total records: {len(combined_weather)}")
            
            return combined_weather
        else:
            print("No weather data collected")
            return None
    
    def analyze_weather_impact(self, weather_df, results_df):
        """Analyze the impact of weather on race results"""
        if weather_df is None or results_df is None:
            print("Cannot analyze weather impact - missing data")
            return None
        
        # Merge weather and results data
        merged_data = results_df.merge(weather_df, on='Year', how='inner')
        
        # Analyze weather impact on winners
        print("\n=== WEATHER IMPACT ANALYSIS ===")
        
        # Winners by weather condition
        winners = merged_data[merged_data['Position'] == 1]
        weather_impact = winners.groupby('Weather_Condition').size().sort_values(ascending=False)
        print("\nWinners by Weather Condition:")
        print(weather_impact)
        
        # Average temperature for winners vs non-winners
        if 'Temperature_Avg_C' in merged_data.columns:
            winner_temp = merged_data[merged_data['Position'] == 1]['Temperature_Avg_C'].mean()
            non_winner_temp = merged_data[merged_data['Position'] != 1]['Temperature_Avg_C'].mean()
            print(f"\nAverage Temperature:")
            print(f"Winners: {winner_temp:.1f}°C")
            print(f"Non-winners: {non_winner_temp:.1f}°C")
        
        # Rain impact
        rain_races = merged_data[merged_data['Weather_Condition'].str.contains('Rain', na=False)]
        if not rain_races.empty:
            print(f"\nRaces with rain: {len(rain_races['Year'].unique())}")
            rain_winners = rain_races[rain_races['Position'] == 1]
            print(f"Winners in rain: {rain_winners['Abbreviation'].tolist()}")
        
        return merged_data

def main():
    """Main function to run weather data collection"""
    collector = WeatherDataCollector()
    
    # Collect weather data
    weather_data = collector.collect_weather_data()
    
    # If we have results data, analyze weather impact
    results_path = Path("../data/singapore_gp_results_ergast_2008_2024.csv")
    if results_path.exists():
        results_df = pd.read_csv(results_path)
        collector.analyze_weather_impact(weather_data, results_df)
    
    return weather_data

if __name__ == "__main__":
    weather_data = main()
