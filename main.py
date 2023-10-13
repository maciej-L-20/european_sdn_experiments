from mininet.net import Mininet
from mininet.topo import Topo
from prep import City
from mininet.topolib import TreeTopo

cityFile = open("cities", "r")
linksFile = open("links","r")
class MyTopo(Topo):

    def add_links(self,switches,cities):
        for line in linksFile:
            line = line.strip()
            linkedCities = line.split(sep=",")
            linkBw = int(linkedCities[2])
            linkDelay = City.compute_delay(cities[linkedCities[0]],cities[linkedCities[1]])
            self.addLink(switches[linkedCities[0]],switches[linkedCities[1]],bw=linkBw,delay=f'{linkDelay}ms')


    def build(self):
        lineNumber = 0
        switches = {}
        cities = {}
        for line in cityFile:
            line = line.strip()
            apiInput = line.split(sep=",")
            cities[apiInput[0]] = City.api_call(apiInput[0], apiInput[1])
            tempHost = self.addHost(f'h{lineNumber}')
            tempSwitch = self.addSwitch(f's{lineNumber}')
            self.addLink(tempHost, tempSwitch)
            switches[apiInput[0]] = tempSwitch
            lineNumber += 1

        self.add_links(switches,cities)

topos = {'mytopo': (lambda: MyTopo())}
