import requests as req
import pandas as pd
import json
import time

#constants
url_api = "https://archive-api.open-meteo.com/v1/archive"
daily = "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_max"
timezone = "Africa/Casablanca"

def fetch_city_weather(city_name,latitude,longitude,start_date,end_date):

        url = url_api
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": daily,
            "timezone": timezone
        }
        for att in range(3):
                try:
                        response = req.get(url, params=params, timeout=10)
                        if response.status_code not in (429,500,502,503,504):
                            break
                except req.exceptions.Timeout:
                        if att==2:
                                raise # sert à relancer l'exception si c'est la dernière tentative
                time.sleep(2)  # Wait for 2 seconds before retrying

        print("https status", response.status_code)
        response.raise_for_status()  # Raise an exception for HTTP errors

        city_data = response.json()
        
        df=pd.DataFrame(city_data["daily"])

        df.rename(columns=
        {
            "time": "date",
            "temperature_2m_max": "max_temperature",
            "temperature_2m_min": "min_temperature",
            "temperature_2m_mean": "mean_temperature",
            "precipitation_sum": "total_precipitation",
            "wind_speed_10m_max": "max_wind_speed",
        },inplace=True)

        df["city"]=city_name
        return df

