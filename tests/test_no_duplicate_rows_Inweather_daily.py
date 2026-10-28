
import src.database as bdd

def test_no_duplicate_rows_Inweather_daily():
    with bdd.get_connection() as conn:
        with conn.cursor() as cursor:
            counter=cursor.execute("select city,date,count(*) from raw.weather_daily "
                                   "group by city,date having count(*)>1 ").fetchall()
            assert counter == []," dans la table des données il existe des doublons"
                                   