import json

with open("config/cities.json","r") as file:
    cities=json.load(file)

for city,coordinates in cities.items():
    print(f'{city}+" latitude:"+{coordinates["latitude"]}+" longitude:"+{coordinates["longitude"]}+"\n"')
    print("-------------------------")