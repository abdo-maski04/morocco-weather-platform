import scripts.explore_cities as explore
import src.database as bdd

df= explore.explore_cities("2026-09-01","2026-09-02")
for city,city_df in df.groupby("city"):
    rows=bdd.convert_df_to_rows(city_df)
    last_loaded_date=city_df["date"].max()

    try:
        rows_loaded=bdd.load_weather_rows(rows)
    except Exception:
        bdd.log_ingestion(city, last_loaded_date, "failed", 0)
        raise
    else:
        bdd.log_ingestion(city, last_loaded_date, "success", rows_loaded)

print("loaded_terminated")