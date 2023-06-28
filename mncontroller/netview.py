class Netview:
    def __init__(self, net):
        self.mymininet = net
        self.net_topo={}
        self.version=0
        self.switches={}
        self.ports={}
        self.hosts={}
        self.links={}
        self.associations={} 


    def wirte_topo(self):
        self.net_topo={}
        self.version+=1
        self.net_topo['version']=self.version
        self.net_topo['items']=[]
        # todo: 添加实时的网卡信息、cpu占用、mem
        # 可能需要额外的dpid
        for s in self.switches.values():
            self.net_topo['items'].append(s)
        for s in self.ports.values():
            self.net_topo['items'].append(s)
        for s in self.hosts.values():
            self.net_topo['items'].append(s)
        for s in self.links.values():
            self.net_topo['items'].append(s)
        for s in self.associations.values():
            self.net_topo['items'].append(s)
        return self.net_topo


    def get_topo(self):
        return self.net_topo
        # switches=[s for s in self.net.switches]
        # hosts=[h for h in self.net.hosts]
        # links=[l for l in self.net.links]
        # to_update={}
        # version=self.version+1
        # to_update["version"]=version
        # items=[]
        # for s in switches:
        #     s_view={
        #         "id":s.uuid,
        #         "type":"switch",
        #         "hostname":s.name,
        #         "switchType":"",
        #         "dpid":s.dpid
        #     }
        #     items.append(s_view)
        # for h in hosts:
