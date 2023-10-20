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
    ax.add_feature(cfeature.LAND,)
    ax.add_feature(cfeature.BORDERS, linestyle=':',alpha=0.3)
    cities = prep.read_cities()

    index = 0
    for city in cities.values():
        ax.plot(city.longitude,city.latitude,marker='o', markersize=5, color='black')
        ax.text(city.longitude-1, city.latitude+0.5, f'{index}.{city.name}', transform=ccrs.PlateCarree(), fontsize=12, color='black',label=f'{index}.{city.name}')
        index+=1

    for line in linkFile:
        line = line.strip()
        linkInput = line.split(sep=",")
        city1 = cities[linkInput[0]]
        city2 = cities[linkInput[1]]
        ax.plot([city1.longitude, city2.longitude], [city1.latitude, city2.latitude], 'k-',alpha = 0.2,transform=ccrs.PlateCarree())
        delay = City.compute_delay(city1,city2)
        ax.text(0.5 * (city1.longitude+city2.longitude), 0.5 * (city1.latitude+city2.latitude)+0.2, delay, transform=ccrs.PlateCarree(), fontsize=8,weight='bold', color='red')

    plt.savefig('mapa.png')

map_config()