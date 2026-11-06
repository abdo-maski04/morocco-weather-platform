select 
city as city_name,
date as weather_date,
max_temp as temp_max_c,
min_temp as temp_min_c,
mean_temp as temp_mean_c,
sum_precipitation as precipitation_mm,
max_wind_speed as wind_speed_max_kmh,
ingested_at 
from {{ source('raw', 'weather_daily') }}