import json
import src.ingestion as ing
import pandas as pd
import requests as req

with open("config/cities.json","r") as file:
    cities_infos=json.load(file)


for city,coordinates in cities_infos.items():
    print(ing.fetch_city_weather(city,coordinates["latitude"],coordinates["longitude"],"2026-10-01","2026-10-07"))