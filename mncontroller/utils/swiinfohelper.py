import re
from subprocess import Popen, PIPE
def parse_swi_interface_stat(interface_info):
    match = re.search(r'{([^}]+)}', interface_info)
    if match:
        statistics_str = match.group(1)
        statistics = {}
        for match2 in re.finditer(r'(\w+)\s*=\s*([\d]+)', statistics_str):
            statistics[match2.group(1)] = int(match2.group(2))
        return statistics
    else:
        print('No statistics found.')
        return {}