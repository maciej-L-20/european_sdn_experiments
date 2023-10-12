from mininet.net import Mininet
from mininet.topo import Topo
from mininet.topolib import TreeTopo

cityFile = open("cities", "r")


class MyTopo(Topo):

    # Pętla na dodawanie switchy i hostów
    # Switche do zbioru

    def build(self):
        lineNumber = 0
        cityDict = {}
        for line in cityFile:
            line = line.strip()
            apiInput = line.split(sep=",")
            tempHost = self.addHost(f'h{lineNumber}')
            tempSwitch = self.addSwitch(f's{lineNumber}')
            self.addLink(tempHost, tempSwitch)
            cityDict[apiInput[0]] = tempSwitch
            lineNumber += 1

        self.addLink(cityDict['Berlin'], cityDict['Warsaw'])
        self.addLink(cityDict['Berlin'], cityDict['Paris'])
        self.addLink(cityDict['Berlin'], cityDict['London'])
        self.addLink(cityDict['Vilnus'], cityDict['Warsaw'])
        self.addLink(cityDict['Zagreb'], cityDict['Warsaw'])
        self.addLink(cityDict['Monako'], cityDict['Paris'])
        self.addLink(cityDict['Bern'], cityDict['Paris'])
        self.addLink(cityDict['Dublin'], cityDict['London'])
        self.addLink(cityDict['Oslo'], cityDict['London'])


topos = {'mytopo': (lambda: MyTopo())}
