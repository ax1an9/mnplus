import psutil


def get_process_info(pid):
    """
    获取进程及其子进程的CPU和内存使用情况
    返回实例：
    'pid': pid, 
    'cpu_percent': 百分数 like 99.8 代表 99.8%,
    'mem_rss':MB 为单位
    'mem_vms':MB 为单位
    'children': children_info
    """
    # 获取进程对象
    process = psutil.Process(pid)
    # 获取进程及其所有子进程的CPU使用情况
    cpu_percent = process.cpu_percent(interval=1)
    # 获取进程及其所有子进程的内存使用情况
    mem_info = process.memory_info()
    # 获取所有子进程的CPU和内存使用情况
    children_info = []
    for child in process.children():
        if child.is_running():
            child_info = get_process_info(child.pid)
            children_info.append(child_info)
    # 构造结果字典
    result = {'pid': pid,
              'cpu_percent': cpu_percent,
              'mem_rss': mem_info.rss/ 1024 / 1024,
              'mem_vms': mem_info.vms/ 1024 / 1024,
              'children': children_info}
    return result

def result2vview(result,constraints):
    """
    将结果转为类似一个虚拟计算机节点的算力视图.
    :param result: 实时获取的结果
    :param constraints: 节点自带的资源限制
    返回：虚拟计算机节点的算力视图
    like：
    {
                "mem_usage_rate": 0.02752685546875,
                "cpu_usage_rate": 0.0880859375
            }

    """
    cnt=psutil.cpu_count()
    tot_used_cpu_percent=result['cpu_percent']
    tot_used_mem=result['mem_rss']
    for childitem in result['children']:
        tot_used_cpu_percent+=childitem['cpu_percent']
        tot_used_mem+=result['mem_rss']
    mem_usage_rate=0.0
    cpu_usage_rate=0.0
    if constraints['mem'] and constraints['mem']!=0 :
        mem_usage_rate=float(tot_used_mem)/constraints['mem']
    if cnt!=0 and constraints['cpu'] and constraints['cpu']!=0:
        cpu_usage_rate=float(tot_used_mem)/cnt/(constraints['cpu']*100)
    ret={}
    ret['mem_usage_rate']=mem_usage_rate
    ret['cpu_usage_rate']=cpu_usage_rate
    return ret


