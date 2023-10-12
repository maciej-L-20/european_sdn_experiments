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

        self.addLink(cityDict['Berlin'], cityDict['Warsaw'],bw=10, delay=f'{City.compute_delay(cities["Berlin"], cities["Warsaw"])}ms')
        self.addLink(cityDict['Berlin'], cityDict['Paris'],bw=10, delay=f'{City.compute_delay(cities["Berlin"], cities["Paris"])}ms')
        self.addLink(cityDict['Berlin'], cityDict['London'],bw=10, delay=f'{City.compute_delay(cities["Berlin"], cities["London"])}ms')
        self.addLink(cityDict['Vilnus'], cityDict['Warsaw'],bw=10, delay=f'{City.compute_delay(cities["Vilnus"], cities["Warsaw"])}ms')
        self.addLink(cityDict['Zagreb'], cityDict['Warsaw'],bw=10, delay=f'{City.compute_delay(cities["Zagreb"], cities["Warsaw"])}ms')
        self.addLink(cityDict['Monako'], cityDict['Paris'],bw=10, delay=f'{City.compute_delay(cities["Monako"], cities["Paris"])}ms')
        self.addLink(cityDict['Bern'], cityDict['Paris'],bw=10, delay=f'{City.compute_delay(cities["Bern"], cities["Paris"])}ms')
        self.addLink(cityDict['Dublin'], cityDict['London'],bw=10, delay=f'{City.compute_delay(cities["Dublin"], cities["London"])}ms')
        self.addLink(cityDict['Oslo'], cityDict['London'],bw=10, delay=f'{City.compute_delay(cities["Oslo"], cities["London"])}ms')


topos = {'mytopo': (lambda: MyTopo())}
