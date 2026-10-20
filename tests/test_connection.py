from src.database import get_connection

conn=get_connection()
cursor=conn.cursor()
cursor.execute("select * from raw.weather_daily limit 5;")
result=cursor.fetchone()
print(result)
conn.close()