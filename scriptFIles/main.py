import json

from mininet.net import Mininet
from mininet.topo import Topo
from prep import City
from mininet.topolib import TreeTopo

cityFile = open("cities", "r")
linksFile = open("links", "r")
class MyTopo(Topo):

    def add_links(self,switches,cities):
        for line in linksFile:
            line = line.strip()
            linkedCities = line.split(sep=",")
            linkBw = int(linkedCities[2])
            linkDelay = City.compute_delay(cities[linkedCities[0]],cities[linkedCities[1]])
            print(linkDelay)
            self.addLink(switches[linkedCities[0]],switches[linkedCities[1]],bw=linkBw,delay=f'{linkDelay}ms')
            cities[linkedCities[0]].ports.append(f's{cities[linkedCities[1]].index}')
            cities[linkedCities[1]].ports.append(f's{cities[linkedCities[0]].index}')
        file = open("portmap.json", 'w')
        citiesToJson=[]
        for city in cities.values():
            citiesToJson.append(city.do_json())
        json.dump(citiesToJson,file)


    def build(self):
        lineNumber = 1
        switches = {}
        cities = {}
        for line in cityFile:
            line = line.strip()
            apiInput = line.split(sep=",")
            cities[apiInput[0]] = City.api_call(apiInput[0], apiInput[1])
            city = cities[apiInput[0]]
            city.index=lineNumber
            city.ports.append("null")
            city.ports.append(f'h{city.index}')
            tempHost = self.addHost(f'h{lineNumber}')
            tempSwitch = self.addSwitch(f's{lineNumber}')
            self.addLink(tempHost, tempSwitch)

            switches[apiInput[0]] = tempSwitch
            lineNumber += 1

        self.add_links(switches,cities)


topos = {'mytopo': (lambda: MyTopo())}
