import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import prep
from prep import City
linkFile = open("links", "r")
def map_config():
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-12, 35, 33, 67], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND,)
    ax.add_feature(cfeature.BORDERS, linestyle=':',alpha=0.3)
    cities = prep.read_cities()

    for city in cities.values():
        ax.plot(city.longitude,city.latitude,marker='o', markersize=5, color='black')
        ax.text(city.longitude-1, city.latitude+0.5, f'{city.index}.{city.name}', transform=ccrs.PlateCarree(), fontsize=12, color='black',label=f'{city.index}.{city.name}')

    lineIndex=1
    for line in linkFile:
        line = line.strip()
        linkInput = line.split(sep=",")
        city1 = cities[linkInput[0]]
        city2 = cities[linkInput[1]]
        color = lambda lineIndex: "green" if lineIndex > 9 else "black"
        ax.plot([city1.longitude, city2.longitude], [city1.latitude, city2.latitude], alpha = 0.4,transform=ccrs.PlateCarree(),color=color(lineIndex))
        delay = City.compute_delay(city1,city2)
        if lineIndex == 16:
            ax.text(0.5 * (city1.longitude+city2.longitude-2), 0.5 * (city1.latitude+city2.latitude-1)+0.2, delay, transform=ccrs.PlateCarree(), fontsize=8,weight='bold', color='red')
        else:
            ax.text(0.5 * (city1.longitude+city2.longitude), 0.5 * (city1.latitude+city2.latitude)+0.2, delay, transform=ccrs.PlateCarree(), fontsize=8,weight='bold', color='red')
        lineIndex+=1
    plt.savefig('mapa.png')

map_config()