select
    city_name,
    weather_date,
    temp_max_c,
    temp_min_c,
    temp_mean_c,
    precipitation_mm,
    wind_speed_max_kmh,
    avg(temp_mean_c) over (
        partition by city_name
        order by weather_date
        rows between 6 preceding and current row
    ) as temp_mean_7d_c,
    sum(precipitation_mm) over (
        partition by city_name
        order by weather_date
        rows between 6 preceding and current row
    ) as precipitation_7d_mm
from {{ ref('stg_weather_daily') }}