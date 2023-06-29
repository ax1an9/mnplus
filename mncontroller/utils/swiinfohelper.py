import re
def parse_swi_interface_stat(interface_info):
    """
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