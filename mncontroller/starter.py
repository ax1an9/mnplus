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
from updateviewtask import ViewUpdater

# specify the openflow version
of_proto='OpenFlow15'
mn_pid = os.getpid()
print("mn's pid: "+str(mn_pid))
net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)
# todo:replace this with init config
c0 = net.addController('c0', controller=RemoteController,
                        ip='127.0.0.1', port=6653)
# 打开文件并读取 init topo JSON 数据
# /home/test/Desktop/mySDNnetwork/dev/resources/topos/moredetailbase.json
# /resources/topos/basetopo.json
with open('./resources/topos/moredetailbase.json', 'r') as file:
    data = json.load(file)
nparser=network_parser(net)
nparser.parse(data)
nv=Netview(net)
nv.switches=nparser.switches
nv.ports=nparser.ports
nv.hosts=nparser.hosts
nv.links=nparser.links
nv.associations=nparser.associations
# start net
net.start()
# use MininetRest as server
mininet_rest = MininetRest(net,nv)
update_task=ViewUpdater(nv)
print("mininet_rest.get_links():")
print(mininet_rest.get_links())
print("get node:")
print('haha' in net.hosts)


update_task.start()
# start server
mininet_rest.run()
update_task.stop()
# stop server
net.stop()