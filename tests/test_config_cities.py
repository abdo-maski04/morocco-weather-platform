import json

with open("config/cities.json", "r") as file:
    cities_data = json.load(file)

    for city,coordinates in cities_data.items():
        print(f"City: {city}, latitude: {coordinates['latitude']}, longitude: {coordinates['longitude']}")
        print("---------------------")