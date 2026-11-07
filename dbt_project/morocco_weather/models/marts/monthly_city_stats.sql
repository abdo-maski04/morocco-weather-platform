select 
city_name,
Date_trunc('month', weather_date)::date as month,
count(*) as nbr_days,
sum(precipitation_mm) as total_precipitation_mm_month,
count(*) filter (where precipitation_mm >= 1) as nbr_days_with_precipitation,
round(avg(temp_mean_c),1) as avg_temp_c_month,
min(temp_min_c) as min_temp_c_month,
max(temp_max_c) as max_temp_c_month
from {{ ref('stg_weather_daily') }}
group by city_name,month
order by city_name, month