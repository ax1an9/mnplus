import utils.computepowertool as cpt
from utils.hostinfohelper import parse_ifconfig
class Netview:
    def __init__(self, net):
        self.net = net
        self.net_topo={}
        self.version=0
        self.switches={}
        self.ports={}
        self.hosts={}
        self.links={}
        self.associations={} 

    def get_host_interfaceinfo(self,host_name,interface_name):
        """
        获取某节点的某个网卡的丢包率信息
        """
        host=self.net[host_name]
        output = host.cmd('ifconfig',interface_name)
        net_info=parse_ifconfig(output) # form:{'RX packets': 3, 'RX errors': 0, 'TX packets': 3, 'TX errors': 0}
        # 上一次的信息被写入到host’s params
        pre_net_info={'RX packets': 0, 'RX errors': 0, 'TX packets': 0, 'TX errors': 0}
        if 'net_info' in host.params:
            pre_net_info=host.params['net_info']
        # 计算数据包数量和错误数据包数量的差异
        rx_diff = net_info['RX packets'] -pre_net_info['RX packets']
        rx_err_diff = net_info['RX errors'] -pre_net_info['RX errors']
        tx_diff =net_info['TX packets'] -pre_net_info['TX packets']
        tx_err_diff =net_info['TX errors'] -pre_net_info['TX errors']
        res={
            'rx_loss_rate':rx_err_diff / (rx_diff + rx_err_diff),
            'tx_loss_rate' : tx_err_diff / (tx_diff + tx_err_diff)
        }
        # update pre
        pre_net_info=host.params['net_info']=net_info
        return res

    def get_compute_power(self,host_name):
        """
        获取节点的算力信息
        模板结果：
        {'mem_usage_rate': 0.027618408203125,
        'cpu_usage_rate': 0.1767578125}
        """
        host=self.net[host_name]
        pid=host.pid
        # 根据 pid 获取 所有所有子进程的pid ，然后统计每个pid的使用情况
        res=cpt.get_process_info(pid)
        # 获取基础分配量
        constraints={}
        constraints['cpu']=host.params['cpu']
        constraints['mem']=host.params['mem']

        return cpt.result2vview(res,constraints)

    def host_info_cpu_update(self):
        for h in self.hosts.value():
            host_name=h['hostname']
            compute_power_info=self.get_compute_power(host_name)
            h['compute_power_info']=compute_power_info
            
        return 

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
        # new
        
        return self.net_topo
    def parse_ifconfig(self):
        # RX packets         ：接受到的总包数
        # RX bytes             ：接受到的总字节数
        # RX errors            ：接收时，产生错误的数据包数
        # RX dropped        ：接收时，丢弃的数据包数
        # RX overruns       ：接收时，由于速度过快而丢失的数据包数
        # RX frame (框架)  ：接收时，发生frame错误而丢失的数据包数
        
        return 

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
    