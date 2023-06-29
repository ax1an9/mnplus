import utils.uuidtools as uuidtool
from mininet.link import TCLink
from mininet.node import Controller, RemoteController, OVSKernelSwitch, CPULimitedHost
of_proto='OpenFlow15'
class network_parser:
    def __init__(self, net):
        self.net = net
        self.switches={}
        self.ports={}
        self.hosts={}
        self.links={}
        self.associations={} 
    def parse(self,network_desc):
        for item in network_desc["items"]:
            if item["type"] == "switch":
                self.switches[item["id"]]=item
            elif item["type"] == "port":
                self.ports[item["id"]]=item
            elif item["type"] == "host":
                self.hosts[item["id"]]=item
            elif item["type"] == "link":
                self.links[item["id"]]=item
            elif item["type"] == "association":
                self.associations[item["id"]]=item
        # todo 利用mininet的功能创建网络。
        # 构建swi 和 host 与其port 的关系
        for ass in self.associations.values():
            if ass["from"] in self.switches:
                if 'ports' not in self.switches[ass['from']]:
                    self.switches[ass['from']]['ports']=[]
                self.switches[ass['from']]['ports'].append(ass['to'])
                self.ports[ass['to']]['mastertype']='switch'
                self.ports[ass['to']]['masterid']=ass['from']
            elif ass['from'] in self.hosts:
                if 'ports' not in self.hosts[ass['from']]:
                    self.hosts[ass['from']]['ports']=[]
                self.hosts[ass['from']]['ports'].append(ass['to'])
                self.ports[ass['to']]['mastertype']='host'
                self.ports[ass['to']]['masterid']=ass['from']
        # 构建swi
        for swi in self.switches.values():
            added=self.net.addSwitch(swi['hostname'],protocols=of_proto, nodeID=swi['id'])
            added.uuid=swi['id']
            print(added)
        # 构建host
        for h in self.hosts.values():
            # 目前统一使用同种类型的host，包括CPU和资源LIMIT
            added=self.net.addHost(h['hostname'],cls=CPULimitedHost,mem=128,cpu=0.2, nodeID=h['id'])
            added.uuid=h['id']
        # 构建连接
        for l in self.links.values():
            n1 =(self.hosts[self.ports[l['from']]['masterid']]['hostname'] 
                 if self.ports[l['from']]['mastertype'] == 'host' 
                 else self.switches[self.ports[l['from']]['masterid']]['hostname'])
            n2=(self.hosts[self.ports[l['to']]['masterid']]['hostname'] 
                           if self.ports[l['to']]['mastertype'] == 'host' 
                           else self.switches[self.ports[l['to']]['masterid']]['hostname'])
            node1=self.net[n1]
            node2=self.net[n2]
            _bandwidth=l["bandwidth"] if "bandwidth" in l else None
            _delay=l['delay'] if 'delay' in l else None
            _loss=l['loss'] if 'loss' in l else None
            added=self.net.addLink(node1, node2,
                                   intfName1=n1+'-'+self.ports[l['from']]['hostname'],
                                   intfName2=n2+'-'+self.ports[l['to']]['hostname'],
                                     cls=TCLink, bw=_bandwidth, delay=_delay, loss=_loss,linkID=l['id'])
            # added=self.net.addLink(node1, node2,
            #                        intfName1=n1+'-'+self.ports[l['from']]['hostname'],
            #                        intfName2=n2+'-'+self.ports[l['to']]['hostname'])
            # added.uuid=l['id']

        


                




