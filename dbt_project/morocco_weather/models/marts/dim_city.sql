select
city_name,
latitude,
longitude,
region
from {{ ref('cities')}}