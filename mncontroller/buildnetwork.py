import json
import utils.uuidtools as uuidtool
of_proto='OpenFlow15'
class network_parser:
    def __init__(self, net):
        self.mymininet = net
    def parse(self,network_json):
        network_desc=json.loads(network_json)
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
        # 构建swi 和 host 与其port 的关系
        for ass in associations:
            if ass['from'] in switches:
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
        for swi in switches:
            # 定义网卡名称的列表
            intfNames = [ports[p]['hostname'] for p in swi['ports']]
            added=self.net.addSwitch(swi['hostname'],protocols=of_proto,intfName=intfNames)
            added.uuid=swi['id']
        # 构建host
        for h in hosts:
            # 定义网卡名称的列表
            intfNames = [ports[p]['hostname'] for p in h['ports']]
            added=self.net.addHost(swi['hostname'],intfName=intfNames)
            added.uuid=h['id']
        # 构建连接
        for l in links:
            node1=self.net[ports[l['from']]['masterid']]
            node2=self.net[ports[l['to']]['masterid']]
            added=self.net.addLink(node1, node2,
                                   intfName1=ports[l['from']]['hostname'],
                                   intfName2=ports[l['to']]['hostname'])
            added.uuid=l['id']

        


                




