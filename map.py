import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import prep
from prep import City
linkFile = open("links","r")
def map_config():
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-12, 35, 33, 67], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    cities = prep.read_cities()
    for city in cities.values():
        ax.plot(city.longitude,city.latitude,marker='o', markersize=5, color='black',label=city.name)
        ax.text(city.longitude+0.5, city.latitude+0.5, city.name, transform=ccrs.PlateCarree(), fontsize=12, color='blue')
    for line in linkFile:
        line = line.strip()
        linkInput = line.split(sep=",")
        city1 = cities[linkInput[0]]
        city2 = cities[linkInput[1]]
        ax.plot([city1.longitude, city2.longitude], [city1.latitude, city2.latitude], 'k-',transform=ccrs.PlateCarree())
        delay = City.compute_delay(city1,city2)
        ax.text(0.5 * (city1.longitude+city2.longitude+0.5), 0.5 * (city1.latitude+city2.latitude),
                delay, ha='center', va='bottom', transform=ccrs.PlateCarree(), fontsize=8, color='red')
    plt.show()

map_config()