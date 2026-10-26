import json
import src.ingestion as ing
from datetime import datetime
import pandas as pd


def explore_cities(start_date, end_date):
    with open("config/cities.json", "r") as file:
        cities_infos = json.load(file)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dataframes = []

    if start.year == end.year:
        date_ranges = [(start_date, end_date)]
    else:
        date_ranges = [(start_date, f"{start.year}-12-31")]
        date_ranges.extend(
            (f"{year}-01-01", f"{year}-12-31")
            for year in range(start.year + 1, end.year)
        )
        date_ranges.append((f"{end.year}-01-01", end_date))

    for period_start, period_end in date_ranges:
        for city, coordinates in cities_infos.items():
            
            df = ing.fetch_city_weather(
                city,
                coordinates["latitude"],
                coordinates["longitude"],
                period_start,
                period_end,
            )
            dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)