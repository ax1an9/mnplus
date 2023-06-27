import json
import utils.uuidtools as uuidtool
of_proto='OpenFlow15'
class network_parser:
    def __init__(self, net):
        self.net = net
    def parse(self,network_desc):
        switches={}
        ports={}
        hosts={}
        links={}
        associations={}
        for item in network_desc["items"]:
            if item["type"] == "switch":
                switches[item["id"]]=item
            elif item["type"] == "port":
                ports[item["id"]]=item
            elif item["type"] == "host":
                hosts[item["id"]]=item
            elif item["type"] == "link":
                links[item["id"]]=item
            elif item["type"] == "association":
                associations[item["id"]]=item
        # todo 利用mininet的功能创建网络。
        # print(associations)
        # 构建swi 和 host 与其port 的关系
        for ass in associations.values():
            if ass["from"] in switches:
                if 'ports' not in switches[ass['from']]:
                    switches[ass['from']]['ports']=[]
                switches[ass['from']]['ports'].append(ass['to'])
                ports[ass['to']]['mastertype']='switch'
            elif ass['from'] in hosts:
                if 'ports' not in hosts[ass['from']]:
                    hosts[ass['from']]['ports']=[]
                hosts[ass['from']]['ports'].append(ass['to'])
                ports[ass['to']]['mastertype']='host'
            ports[ass['to']]['masterid']=ass['from']
        # 构建swi
        for swi in switches.values():
            # 定义网卡名称的列表
            # intfNames = [ports[p]['hostname'] for p in swi['ports']]
            added=self.net.addSwitch(swi['hostname'],protocols=of_proto)
            added.uuid=swi['id']
            print(added)
        # 构建host
        for h in hosts.values():
            # 定义网卡名称的列表
            # intfNames = [ports[p]['hostname'] for p in h['ports']]
            added=self.net.addHost(h['hostname'])
            added.uuid=h['id']
            print(added)
        # 构建连接
        for l in links.values():
            n1 =(hosts[ports[l['from']]['masterid']]['hostname'] 
                 if ports[l['from']]['mastertype'] == 'host' 
                 else switches[ports[l['from']]['masterid']]['hostname'])
            n2=(hosts[ports[l['to']]['masterid']]['hostname'] 
                           if ports[l['to']]['mastertype'] == 'host' 
                           else switches[ports[l['to']]['masterid']]['hostname'])
            node1=self.net[n1]
            node2=self.net[n2]
            print(ports[l['from']]['hostname'])
            print(ports[l['to']]['hostname'])
            added=self.net.addLink(node1, node2,
                                   intfName1=n1+'-'+ports[l['from']]['hostname'],
                                   intfName2=n2+'-'+ports[l['to']]['hostname'])
            added.uuid=l['id']

        


                




