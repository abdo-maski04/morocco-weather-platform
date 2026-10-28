import src.ingestion as ingestion
import src.database as bdd
from datetime import date, timedelta
import pandas as pd
import json

initial_start_date = date(2025, 1, 1)
end_date = date.today() - timedelta(5)


def get_start_date(city):
    with bdd.get_connection() as conn:
        with conn.cursor() as cursor:
            last_date = cursor.execute("select Max(last_loaded_date) from raw.ingestion_log"
                                       " where city=%s"
                                       " and status='success'", (city,)).fetchone()[0]

    if last_date is None:
        return initial_start_date
    return last_date + timedelta(days=1)

def work():
    with open("config/cities.json", "r") as file:
        cities = json.load(file)

    for city, coordinates in cities.items():
        start_date = get_start_date(city)
        if start_date > end_date:
            continue

        df = ingestion.fetch_city_weather(city, coordinates["latitude"], coordinates["longitude"],
                                        start_date.isoformat(), end_date.isoformat())
        if df.empty:
            continue

        rows = bdd.convert_df_to_rows(df)

        try:
            sum_rows = bdd.load_weather_rows(rows)
        except Exception:
            bdd.log_ingestion(city, start_date, "failed", 0)
            raise
        else:
            last_loaded = pd.to_datetime(df["date"]).max().date()
            bdd.log_ingestion(city, last_loaded, "success", sum_rows)


if __name__ == "__main__":
    work()

