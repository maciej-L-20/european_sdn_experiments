from mininet.net import Mininet
from mininet.topo import Topo
from prep import City
from mininet.topolib import TreeTopo

cityFile = open("cities", "r")


class MyTopo(Topo):

    def build(self):
        lineNumber = 0
        cityDict = {}
        cities = {}
        for line in cityFile:
            line = line.strip()
            apiInput = line.split(sep=",")
            cities[apiInput[0]] = City.api_call(apiInput[0], apiInput[1])
            tempHost = self.addHost(f'h{lineNumber}')
            tempSwitch = self.addSwitch(f's{lineNumber}')
            self.addLink(tempHost, tempSwitch)
            cityDict[apiInput[0]] = tempSwitch
            lineNumber += 1

        self.addLink(cityDict['Berlin'], cityDict['Warsaw'], delay=City.compute_delay(cities['Berlin'], cities['Warsaw']))
        self.addLink(cityDict['Berlin'], cityDict['Paris'], delay=City.compute_delay(cities['Berlin'], cities['Paris']))
        self.addLink(cityDict['Berlin'], cityDict['London'], delay=City.compute_delay(cities['Berlin'], cities['London']))
        self.addLink(cityDict['Vilnus'], cityDict['Warsaw'], delay=City.compute_delay(cities['Vilnus'], cities['Warsaw']))
        self.addLink(cityDict['Zagreb'], cityDict['Warsaw'], delay=City.compute_delay(cities['Zagreb'], cities['Warsaw']))
        self.addLink(cityDict['Monako'], cityDict['Paris'], delay=City.compute_delay(cities['Monako'], cities['Paris']))
        self.addLink(cityDict['Bern'], cityDict['Paris'], delay=City.compute_delay(cities['Bern'], cities['Paris']))
        self.addLink(cityDict['Dublin'], cityDict['London'], delay=City.compute_delay(cities['Dublin'], cities['London']))
        self.addLink(cityDict['Oslo'], cityDict['London'], delay=City.compute_delay(cities['Oslo'], cities['London']))


topos = {'mytopo': (lambda: MyTopo())}
