"""
Ergast API Data Collector for F1 Singapore GP Prediction

This script collects comprehensive historical F1 data using the Ergast API:
- Historical race results
- Driver standings
- Constructor standings
- Circuit information
- Weather data (where available)
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime
from pathlib import Path
import numpy as np

class ErgastDataCollector:
    def __init__(self, data_dir="../data"):
        self.base_url = "http://ergast.com/api/f1"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def make_request(self, endpoint, params=None):
        """Make a request to the Ergast API with rate limiting"""
        url = f"{self.base_url}/{endpoint}.json"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Rate limiting - be respectful
            time.sleep(0.5)
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None
    
    def collect_singapore_gp_results(self):
        """Collect all Singapore GP results from Ergast API"""
        print("Collecting Singapore GP results from Ergast API...")
        
        all_results = []
        
        # Singapore GP started in 2008
        for year in range(2008, 2025):
            print(f"Collecting {year} Singapore GP...")
            
            # Get race results
            data = self.make_request(f"{year}/Singapore/results")
            
            if data and 'MRData' in data:
                races = data['MRData']['RaceTable']['Races']
                
                for race in races:
                    race_info = {
                        'Year': year,
                        'Race': 'Singapore',
                        'Date': race['date'],
                        'Round': race['round'],
                        'RaceName': race['raceName']
                    }
                    
                    # Get results for this race
                    if 'Results' in race:
                        for result in race['Results']:
                            result_data = race_info.copy()
                            result_data.update({
                                'Position': result['position'],
                                'PositionText': result['positionText'],
                                'Points': result['points'],
                                'DriverNumber': result['Driver']['permanentNumber'] if 'permanentNumber' in result['Driver'] else None,
                                'DriverCode': result['Driver']['code'],
                                'DriverGivenName': result['Driver']['givenName'],
                                'DriverFamilyName': result['Driver']['familyName'],
                                'ConstructorName': result['Constructor']['name'],
                                'ConstructorId': result['Constructor']['constructorId'],
                                'Grid': result['Grid'],
                                'Laps': result['Laps'],
                                'Status': result['Status'],
                                'Time': result['Time']['time'] if 'Time' in result else None,
                                'FastestLapRank': result['FastestLap']['rank'] if 'FastestLap' in result else None,
                                'FastestLapTime': result['FastestLap']['Time']['time'] if 'FastestLap' in result and 'Time' in result['FastestLap'] else None,
                                'FastestLapAvgSpeed': result['FastestLap']['AverageSpeed']['speed'] if 'FastestLap' in result and 'AverageSpeed' in result['FastestLap'] else None
                            })
                            
                            all_results.append(result_data)
        
        if all_results:
            df = pd.DataFrame(all_results)
            
            # Save to CSV
            output_path = self.data_dir / 'singapore_gp_results_ergast_2008_2024.csv'
            df.to_csv(output_path, index=False)
            print(f"Saved Singapore GP results: {output_path}")
            print(f"Total records: {len(df)}")
            
            return df
        else:
            print("No Singapore GP results collected")
            return None
    
    def collect_driver_standings(self, years=None):
        """Collect driver standings for specified years"""
        if years is None:
            years = list(range(2015, 2025))  # Recent years for comprehensive data
        
        print(f"Collecting driver standings for years: {years}")
        
        all_standings = []
        
        for year in years:
            print(f"Collecting {year} driver standings...")
            
            data = self.make_request(f"{year}/driverStandings")
            
            if data and 'MRData' in data:
                standings_table = data['MRData']['StandingsTable']
                
                for standings_list in standings_table['StandingsLists']:
                    year_data = standings_list['season']
                    
                    for standing in standings_list['DriverStandings']:
                        standing_data = {
                            'Year': int(year_data),
                            'Position': standing['position'],
                            'Points': standing['points'],
                            'Wins': standing['wins'],
                            'DriverCode': standing['Driver']['code'],
                            'DriverGivenName': standing['Driver']['givenName'],
                            'DriverFamilyName': standing['Driver']['familyName'],
                            'ConstructorName': standing['Constructors'][0]['name'] if standing['Constructors'] else None,
                            'ConstructorId': standing['Constructors'][0]['constructorId'] if standing['Constructors'] else None
                        }
                        
                        all_standings.append(standing_data)
        
        if all_standings:
            df = pd.DataFrame(all_standings)
            
            # Save to CSV
            output_path = self.data_dir / 'driver_standings_2015_2024.csv'
            df.to_csv(output_path, index=False)
            print(f"Saved driver standings: {output_path}")
            print(f"Total records: {len(df)}")
            
            return df
        else:
            print("No driver standings collected")
            return None
    
    def collect_constructor_standings(self, years=None):
        """Collect constructor standings for specified years"""
        if years is None:
            years = list(range(2015, 2025))
        
        print(f"Collecting constructor standings for years: {years}")
        
        all_standings = []
        
        for year in years:
            print(f"Collecting {year} constructor standings...")
            
            data = self.make_request(f"{year}/constructorStandings")
            
            if data and 'MRData' in data:
                standings_table = data['MRData']['StandingsTable']
                
                for standings_list in standings_table['StandingsLists']:
                    year_data = standings_list['season']
                    
                    for standing in standings_list['ConstructorStandings']:
                        standing_data = {
                            'Year': int(year_data),
                            'Position': standing['position'],
                            'Points': standing['points'],
                            'Wins': standing['wins'],
                            'ConstructorName': standing['Constructor']['name'],
                            'ConstructorId': standing['Constructor']['constructorId']
                        }
                        
                        all_standings.append(standing_data)
        
        if all_standings:
            df = pd.DataFrame(all_standings)
            
            # Save to CSV
            output_path = self.data_dir / 'constructor_standings_2015_2024.csv'
            df.to_csv(output_path, index=False)
            print(f"Saved constructor standings: {output_path}")
            print(f"Total records: {len(df)}")
            
            return df
        else:
            print("No constructor standings collected")
            return None
    
    def collect_circuit_info(self):
        """Collect circuit information"""
        print("Collecting circuit information...")
        
        data = self.make_request("circuits")
        
        if data and 'MRData' in data:
            circuits = data['MRData']['CircuitTable']['Circuits']
            
            circuit_data = []
            for circuit in circuits:
                circuit_info = {
                    'CircuitId': circuit['circuitId'],
                    'CircuitName': circuit['circuitName'],
                    'Country': circuit['Location']['country'],
                    'Latitude': circuit['Location']['lat'],
                    'Longitude': circuit['Location']['long'],
                    'Locality': circuit['Location']['locality']
                }
                circuit_data.append(circuit_info)
            
            df = pd.DataFrame(circuit_data)
            
            # Save to CSV
            output_path = self.data_dir / 'circuits_info.csv'
            df.to_csv(output_path, index=False)
            print(f"Saved circuit information: {output_path}")
            print(f"Total circuits: {len(df)}")
            
            return df
        else:
            print("No circuit information collected")
            return None
    
    def collect_season_schedules(self, years=None):
        """Collect season schedules"""
        if years is None:
            years = list(range(2015, 2025))
        
        print(f"Collecting season schedules for years: {years}")
        
        all_schedules = []
        
        for year in years:
            print(f"Collecting {year} schedule...")
            
            data = self.make_request(f"{year}")
            
            if data and 'MRData' in data:
                races = data['MRData']['RaceTable']['Races']
                
                for race in races:
                    schedule_data = {
                        'Year': year,
                        'Round': race['round'],
                        'RaceName': race['raceName'],
                        'CircuitName': race['Circuit']['circuitName'],
                        'CircuitId': race['Circuit']['circuitId'],
                        'Date': race['date'],
                        'Time': race['time'] if 'time' in race else None,
                        'Country': race['Circuit']['Location']['country'],
                        'Locality': race['Circuit']['Location']['locality']
                    }
                    
                    all_schedules.append(schedule_data)
        
        if all_schedules:
            df = pd.DataFrame(all_schedules)
            
            # Save to CSV
            output_path = self.data_dir / 'season_schedules_2015_2024.csv'
            df.to_csv(output_path, index=False)
            print(f"Saved season schedules: {output_path}")
            print(f"Total races: {len(df)}")
            
            return df
        else:
            print("No season schedules collected")
            return None
    
    def collect_all_data(self):
        """Collect all available data"""
        print("Starting comprehensive data collection...")
        
        # Collect all data types
        singapore_results = self.collect_singapore_gp_results()
        driver_standings = self.collect_driver_standings()
        constructor_standings = self.collect_constructor_standings()
        circuit_info = self.collect_circuit_info()
        season_schedules = self.collect_season_schedules()
        
        print("\n=== DATA COLLECTION COMPLETE ===")
        print(f"Data saved to: {self.data_dir}")
        
        return {
            'singapore_results': singapore_results,
            'driver_standings': driver_standings,
            'constructor_standings': constructor_standings,
            'circuit_info': circuit_info,
            'season_schedules': season_schedules
        }

def main():
    """Main function to run data collection"""
    collector = ErgastDataCollector()
    data = collector.collect_all_data()
    
    # Print summary
    print("\n=== COLLECTION SUMMARY ===")
    for data_type, df in data.items():
        if df is not None:
            print(f"{data_type}: {len(df)} records")
        else:
            print(f"{data_type}: No data collected")

if __name__ == "__main__":
    main()
