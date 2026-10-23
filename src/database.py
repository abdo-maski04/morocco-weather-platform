import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    conn=psycopg.connect(
        host="localhost",
        port=5433,
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        connect_timeout=10
    )
    return conn

upsert_query = """
insert into raw.weather_daily
(city,date,max_temp,min_temp,mean_temp,sum_precipitation,max_wind_speed)
values
(
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)
on conflict (city, date)
do update set
    max_temp          = excluded.max_temp,
    min_temp          = excluded.min_temp,
    mean_temp         = excluded.mean_temp,
    sum_precipitation = excluded.sum_precipitation,
    max_wind_speed    = excluded.max_wind_speed,
    ingested_at       = now();
    """

def load_weather_rows(rows):
    with get_connection() as conn:
        with conn.cursor() as cursor: # sert à 
            cursor.executemany(upsert_query, rows)
            conn.commit()
    return len(rows)