from src.database import get_connection,load_weather_rows
import psycopg
from dotenv import load_dotenv
import os

def test_connection_bdd():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            result=cursor.execute("select 1").fetchone()[0]
            assert result==1,"la connection avec bdd server est échoué"


def get_max_temp():
    with get_connection() as conn:
            with conn.cursor() as cursor:
                 result = cursor.execute("SELECT max_temp FROM raw.weather_daily "
                 "WHERE city = %s AND date = %s",("taza", "2026-08-08")).fetchone()[0]
                 return result 

def test_upsert_insert():
    rows=[('taza','2026-08-08',29.0,18.0,22.0,10.0,16.1)]
    load_weather_rows(rows)
    #on va changer juste max_temp à 30.0
    rows=[('taza','2026-08-08',30.0,18.0,22.0,10.0,16.1)]
    load_weather_rows(rows)
    max_temp=get_max_temp()
    with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("delete from raw.weather_daily "
                "where city = %s and date = %s ",("taza","2026-08-08"))
    assert max_temp==30.0 ,"upsert est échoué"