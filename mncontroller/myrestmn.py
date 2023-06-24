from bottle import Bottle, request
from bottle import route, run, template, error
import time

class MininetRest(Bottle):
    def __init__(self, net):
        super(MininetRest, self).__init__()
        self.net = net # mininet
        # routes
        self.route('/nodes', callback=self.get_nodes)
        self.route('/nodes/<node_name>', callback=self.get_node)
        self.route('/nodes/<node_name>', method='POST', callback=self.post_node)
        self.route('/hosts', method='GET', callback=self.get_hosts)
        self.route('/switches', method='GET', callback=self.get_switches)
        self.route('/links', method='GET', callback=self.get_links)
        self.route('/addnode/<node_name>', callback=self.add_node)

    def add_node(self, node_name):
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
        return {'links': [dict(name=l.intf1.node.name + '-' + l.intf2.node.name,
                               node1=l.intf1.node.name, node2=l.intf2.node.name,
                               intf1=l.intf1.name, intf2=l.intf2.name) for l in self.net.links]}
