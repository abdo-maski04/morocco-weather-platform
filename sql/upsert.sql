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