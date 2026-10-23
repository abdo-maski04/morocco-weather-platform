from src.database import get_connection,load_weather_rows
import psycopg
import os
from dotenv import load_dotenv

load_dotenv

def test_double_creates_single_row():
    rows=[('taza','2026-08-08',29.0,18.0,22.0,10.0,16.1)]
    load_weather_rows(rows)
    load_weather_rows(rows)

    with get_connection() as con:
        with con.cursor() as cursor:
            res=cursor.execute("select count(*) from raw.weather_daily "
                           "where city = %s and date = %s ",('taza','2026-08-08')).fetchone()[0]
            assert res==1,"les doublans se crée dans votre bdd"