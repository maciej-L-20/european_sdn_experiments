import math

import requests
import geopy.distance

geoFile = open("cities", "r")


class City:
    def __init__(self, name, lat, longt):
        self.name = name
        self.latitude = lat
        self.longitude = longt

    def __str__(self):
        return f"{self.name}, {self.latitude}, {self.longitude}"

    @staticmethod
    def compute_distance(city1, city2):
        coords1 = (city1.latitude, city1.longitude)
        coords2 = (city2.latitude, city2.longitude)
        return geopy.distance.geodesic(coords1, coords2)

    @staticmethod
    def compute_price(city1, city2):
        return City.compute_distance(city1, city2) * math.sqrt(2)


cities = []

for line in geoFile:
    line = line.strip()
    apiInput = line.split(sep=",")
    api_url = f'https://api.api-ninjas.com/v1/geocoding?city={apiInput[0]}&country={apiInput[1]}'
    response = requests.get(api_url, headers={'X-Api-Key': 'w0qGONkv1CQxwMDfPwvLKQ==2ueGevHx4PUChvKk'})
    if response.status_code != requests.codes.ok or len(response.json()) == 0:
        print("Error:", response.status_code, response.text)
        exit(123)
    apiResponse = response.json()[0]
    cities.append(City(apiResponse["name"], apiResponse["latitude"], apiResponse["longitude"]))

citiesDict = {}

for city in cities:
    citiesDict[city.name] = cities
    print(city)

print(City.compute_distance(cities[0], cities[1]))
