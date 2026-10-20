create schema if not exists raw;

create table if not exists raw.weather_daily (
    city              varchar(255) not null,
    date              date         not null,
    max_temp          numeric(5,2),
    min_temp          numeric(5,2),
    mean_temp         numeric(5,2),
    sum_precipitation numeric(6,2),
    max_wind_speed    numeric(5,2),
    ingested_at       timestamptz  not null default now(),
    primary key (city, date)
);

create table if not exists raw.ingestion_log (
    id               serial primary key,
    city             varchar(255) not null,
    last_loaded_date date,
    status           varchar(50)  not null check (status in ('success', 'failed')),
    rows_loaded      int          not null default 0,
    logged_at        timestamptz  not null default now()
);


    