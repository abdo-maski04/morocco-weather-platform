import json
from pathlib import Path

config_path= Path(__file__).resolve().parent.parent / "config" / "cities.json"

def load_cities():
    with open(config_path,"r") as file:
        return json.load(file)

def test_there_are_six_cities():
    assert len(load_cities())==6

def test_coordinates_are_in_morocco():
    for city,coords in load_cities().items():
        lat=coords["latitude"]
        lon=coords["longitude"]
        assert 27.0 <=lat<= 36.0 , f"{city} : latitude: {lat} hors du maroc"
        assert -14.0 <=lon<= -1.0 , f"{city} : longitude: {lon} hors du maroc"

    