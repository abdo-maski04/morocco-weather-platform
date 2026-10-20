from src.ingestion import fetch_city_weather
from src.database import load_weather, get_connection

df=fetch_city_weather("Casablanca", 33.58823, -7.6114, "2026-10-01", "2026-10-07")

columns = ["city", "date", "max_temperature", "min_temperature",
           "mean_temperature", "total_precipitation", "max_wind_speed"]
rows=list(df[columns].itertuples(index=False, name=None)) # sert à convertir le DataFrame en une liste de tuples pour l'insertion dans la base de données

print(rows)


print(load_weather(rows))
print(load_weather(rows))   # deuxième fois, mêmes données

with get_connection() as conn:
    print(conn.execute("select count(*) from raw.weather_daily").fetchone())
