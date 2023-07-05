from bottle import Bottle, request
from bottle import route, run, template, error
from mininet.node import Controller, RemoteController, OVSKernelSwitch, CPULimitedHost
from utils.uuidtools import gen_uuid 
import time

class MininetRest(Bottle):
    def __init__(self, net,netview):
        super(MininetRest, self).__init__()
        self.net = net # mininet
        self.netview = netview # mininet
        # routes
        self.route('/nodes', callback=self.get_nodes)
        self.route('/topos', callback=self.get_topos)
        self.route('/nodes/<node_name>', callback=self.get_node)
        self.route('/nodes/<node_name>', method='POST', callback=self.post_node)
        self.route('/hosts', method='GET', callback=self.get_hosts)
        self.route('/switches', method='GET', callback=self.get_switches)
        self.route('/links', method='GET', callback=self.get_links)
        self.route('/addnode1', method='POST', callback=self.add_node)

    def get_topos(self):
        """
        获取当前算力网络拓扑
        """
        return self.netview.get_topo()

    def add_node(self):
        """
        动态增加节点
        request.json:{
            'hostname': h1,
            'mem':512,
            'cpu':0.2
        }
        """
        req=request.json
        condition=(req['hostname'] not in self.net.hosts )and(req['cpu']<=1 and req['cpu']>0)and(req['mem']>0)
        if condition:
            uuid=gen_uuid()
            self.net.addHost(req['hostname'],
                                cls=CPULimitedHost,
                                mem=req['mem'],
                                cpu=req['cpu'], 
                                nodeID=uuid)
            # update net view
            self.netview.updatehosts(uuid,{
                    'id':uuid,
                    'hostname':req['hostname'],
                    'type':"host",
                    "cpuLimit": req['cpu'],
                    'mem':req['mem']
                    })
            #     uuid:{
            #         'id':uuid,
            #         'type':"host",
            #         "cpuLimit": req['cpu'],
            #         'mem':req['mem']
            #         }
            # })
            # updatehosts({
            #     uuid:{
            #         'id':uuid,
            #         'type':"host",
            #         "cpuLimit": req['cpu'],
            #         'mem':req['mem']
            #         }
            # })
        return {"code":200,"info":"success" if condition else "fail to add"}
    
    def add_link(self, node_name):
        h1 = self.net.addHost(node_name)
        return {'nodes': [n for n in self.net]}

    def get_nodes(self):
        print({'nodes': [n for n in self.net]})
        return {'nodes': [n for n in self.net]}

    def get_node(self, node_name):
        node = self.net[node_name]
        return {'intfs': [i.name for i in node.intfList()], 'params': node.params}

    def post_node(self, node_name):
        node = self.net[node_name]
        node.params.update(request.json['params'])
        return {"code":200,"info":"success"}

    def get_hosts(self):
        return {'hosts': [h.name for h in self.net.hosts]}

    def get_switches(self):
        return {'switches': [s.name for s in self.net.switches]}

    def get_links(self):
        return {'nodes': [n for n in self.net],
                'links': [dict(name=l.intf1.node.name + '-' + l.intf2.node.name,
                               node1=l.intf1.node.name, node2=l.intf2.node.name,
                               intf1=l.intf1.name, intf2=l.intf2.name) for l in self.net.links]}
