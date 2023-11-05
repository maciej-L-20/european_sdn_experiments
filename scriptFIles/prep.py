import math

import requests
import geopy.distance

geoFile = open("cities", "r")

#TODO metoda do przekształcania pliku links na plik z indeksami i bw
class City:
    net_velocity = 200_000

    def __init__(self, name, lat, longt):
        self.name = name
        self.latitude = lat
        self.longitude = longt
        self.index = 0
        self.ports=[]

    def do_json(self):
        # Tworzymy kopię słownika __dict__ obiektu i usuwamy niechciane atrybuty
        serializable_dict = self.__dict__.copy()
        del serializable_dict['latitude']
        del serializable_dict['longitude']
        return serializable_dict

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

    # returns in miliseconds
    @staticmethod
    def compute_delay(city1, city2):
        s = City.compute_price(city1, city2)
        v = City.net_velocity
        result = s / v * 1000
        return round(float(result.kilometers), 2)

    @staticmethod
    def api_call(city_name, country):
        api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city_name}&country={country}'
        response = requests.get(api_url, headers={'X-Api-Key': 'w0qGONkv1CQxwMDfPwvLKQ==2ueGevHx4PUChvKk'})
        if response.status_code != requests.codes.ok or len(response.json()) == 0:
            print("Error:", response.status_code, response.text)
            exit(123)
        apiResponse = response.json()[0]
        return City(apiResponse["name"], apiResponse["latitude"], apiResponse["longitude"])


def read_cities():
    cities = {}
    for line in geoFile:
        line = line.strip()
        apiInput = line.split(sep=",")
        api_url = f'https://api.api-ninjas.com/v1/geocoding?city={apiInput[0]}&country={apiInput[1]}'
        response = requests.get(api_url, headers={'X-Api-Key': 'w0qGONkv1CQxwMDfPwvLKQ==2ueGevHx4PUChvKk'})
        if response.status_code != requests.codes.ok or len(response.json()) == 0:
            print("Error:", response.status_code, response.text)
            exit(123)
        apiResponse = response.json()[0]
        cities[apiResponse["name"]] = City(apiResponse["name"], apiResponse["latitude"], apiResponse["longitude"])
    return cities