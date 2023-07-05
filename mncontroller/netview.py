import utils.computepowertool as cpt
from utils.hostinfohelper import parse_ifconfig
from utils.swiinfohelper import parse_swi_interface_stat
import time
from subprocess import Popen, PIPE
import threading
class Netview:
    def __init__(self, net):
        self.net = net
        self.net_topo={}
        self.version=0
        # view的组成信息
        self.switches={}
        self.ports={}
        self.hosts={}
        self.links={}
        self.associations={} 
        self.view_lock=threading.Lock()

    def updatehosts(self,uuid,item):
        self.view_lock.acquire()
        try:
            self.hosts[uuid]=item
        finally:
            self.view_lock.release()

    def get_swi_interface_info(self,interface_name):
        """
        获取对应swtich网卡的详细信息
        解析后结果格式：
        {
            "collisions": 0,
            "rx_bytes": 90,
            "rx_crc_err": 0,
            "rx_dropped": 0,
            "rx_errors": 0,
            "rx_frame_err": 0,
            "rx_missed_errors": 0,
            "rx_over_err": 0,
            "rx_packets": 1,
            "tx_bytes": 176,
            "tx_dropped": 0,
            "tx_errors": 0,
            "tx_packets": 2
        }
        """
        cmd = ['ovs-vsctl', 'list', 'interface', interface_name]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            print("Error executing ovs-vsctl command: %s" % stderr.decode())
            return None
        else:
            return parse_swi_interface_stat(stdout.decode())


    def get_host_interfaceinfo(self,host_name,interface_name):
        """
        获取某host节点的某个网卡的丢包率信息
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
            'rx_loss_rate': 0.0 if (rx_diff + rx_err_diff)==0 else rx_err_diff / (rx_diff + rx_err_diff),
            'tx_loss_rate' : 0.0 if (tx_diff + tx_err_diff)==0 else  tx_err_diff / (tx_diff + tx_err_diff)
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

    def host_info_update(self):
        """
        更新view中的所有虚拟host的信息:算力+网络
        """
        for h in self.hosts.values():
            host_name=h['hostname']
            compute_power_info=self.get_compute_power(host_name)
            h['compute_power_info']=compute_power_info
            intfNames=self.net[host_name].intfNames()
            for intfN in intfNames:
                interfaceinfo=self.get_host_interfaceinfo(host_name,intfN)
                if 'interfaceinfo' not in h:
                    h['interfaceinfo']={}
                h['interfaceinfo'][intfN]={"intfName":intfN,"info":interfaceinfo}
        return 
    
    def swi_info_compute_power_update(self):
        """
        更新view中的所有switch的网络信息
        """
        for s in self.switches.values():
            swi_name=s['hostname']
            intfNames=self.net[swi_name].intfNames()
            for intfN in intfNames:
                if intfN == 'lo':
                    continue
                interface_info=self.get_swi_interface_info(intfN)
                if 'interfaceinfo' not in s:
                    s['interfaceinfo']={}
                s['interfaceinfo'][intfN]={"intfName":intfN,"info":interface_info}


    def all_update(self):
        """
        视图更新
        """
        self.view_lock.acquire()
        try:
            self.host_info_update()
            self.swi_info_compute_power_update()
            self.wirte_topo()
        finally:
            self.view_lock.release()
        

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
        
        

    def get_topo(self):
        self.view_lock.acquire()
        try:
            ret=self.net_topo
            return ret
        finally:
            self.view_lock.release()
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
    