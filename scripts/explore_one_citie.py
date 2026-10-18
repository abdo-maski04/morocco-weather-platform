import json
import pandas as pd
import requests as req
import src.ingestion as ing

with open("config/cities.json", "r") as file:
    cities_data =json.load(file)

for city, coordinates in cities_data.items():
    print(ing.fetch_city_weather(city, coordinates["latitude"], coordinates["longitude"], "2026-10-01", "2026-10-07"))
    
