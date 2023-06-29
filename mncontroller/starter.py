from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController
from myrestmn import MininetRest
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, CPULimitedHost
from mininet.cli import CLI
from mininet.log import setLogLevel
import utils.uuidtools as uuidtool
from mininet.util import quietRun
import os
from netview import Netview
from buildnetwork import network_parser
import json

def update_switch_params(swi):
    swi.params["uuid"]=swi.uuid
    swi.params["type"]=swi.switch
    swi.params["uuid"]=swi.uuid
    swi.params["uuid"]=swi.uuid
    swi.params["uuid"]=swi.uuid

# specify the openflow version
of_proto='OpenFlow15'
mn_pid = os.getpid()
print("mn's pid: "+str(mn_pid))
net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)
# todo:replace this with init config
c0 = net.addController('c0', controller=RemoteController,
                        ip='127.0.0.1', port=6653)
# 打开文件并读取 init topo JSON 数据
with open('./resources/topos/basetopo.json', 'r') as file:
    data = json.load(file)
nparser=network_parser(net)
nparser.parse(data)
# start net
net.start()
# use MininetRest as server
mininet_rest = MininetRest(net)
nv=Netview(net)
nv.switches=nparser.switches
nv.ports=nparser.ports
nv.hosts=nparser.hosts
nv.links=nparser.links
nv.associations=nparser.associations
print("mininet_rest.get_links():")
print(mininet_rest.get_links())
while input():
    nv.all_update()
    print(nv.get_topo())
# print(nv.get_compute_power("h1"))
# print(r'print(nv.get_host_interfaceinfo("h1","h1-haha"))')
# print(nv.get_host_interfaceinfo("h1","h1-haha"))
# links
print("mininet_rest.get_links():")
print(mininet_rest.get_links())


# start server
mininet_rest.run()
# stop server
net.stop()