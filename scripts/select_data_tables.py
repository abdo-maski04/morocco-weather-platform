import psycopg as ps
import src.database as db


def select():
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            result=cur.execute("select * from raw.weather_daily").fetchall()
    print(result)


if __name__ == "__main__":
    select()

