from mininet.net import Mininet
from mininet.topolib import TreeTopo

tree_depth = 2
tree_fanout = 2

tree = TreeTopo(depth=tree_depth, fanout=tree_fanout)
net = Mininet(topo=tree)
net.start()

#To access different hosts you access the net.hosts array containing mininet.node.Host
print(type(net.hosts[0]))

h1, h4 = net.hosts[0], net.hosts[3]
print(h1.cmd('ping -c1 %s' % h4.IP()))
net.stop()