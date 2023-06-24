from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController
from myrestmn import MininetRest
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

#net = Mininet(topo=SingleSwitchTopo(k=2),controller=OVSController,link=TCLink)
net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)
# todo:replace this with init config
c0 = net.addController('c0', controller=RemoteController,
                        ip='127.0.0.1', port=6653)
s1 = net.addSwitch('s1', protocols='OpenFlow13')
s2 = net.addSwitch('s2', protocols='OpenFlow13')
h1 = net.addHost('h1')
h2 = net.addHost('h2')
net.get()
net.addLink(h1, s1)
net.addLink(h2, s2)
net.addLink(s1, s2)
net.start()
mininet_rest = MininetRest(net)
# start server
mininet_rest.run()
net.stop()