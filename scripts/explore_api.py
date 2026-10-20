import requests
url="https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 33.58823,
    "longitude": -7.6114,
    "start_date": "2026-10-01",
    "end_date": "2026-10-07",
    "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_max",
    "timezone": "Africa/Casablanca"
}

response = requests.get(url, params=params, timeout=20) # sert à

print("https status",response.status_code)

response.raise_for_status()  # Raise an exception for HTTP errors

data=response.json()

print("city : Casablanca")
print("dates:",data["daily"]["time"])
print("max temperature:",data["daily"]["temperature_2m_max"])