def parse_ifconfig(result):
        # 解析ifconfig输出并包装为字典
        """
        字典的形态如：
        {'RX packets': 2, 'RX errors': 0, 'TX packets': 1, 'TX errors': 0}
        """
        info_dict = {}
        lines = result.split('\n')
        for line in lines:
            if 'RX packets' in line:
                info_dict['RX packets'] = int(line.split()[2])
            elif 'RX errors' in line:
                info_dict['RX errors'] = int(line.split()[2])
            elif 'TX packets' in line:
                info_dict['TX packets'] = int(line.split()[2])
            elif 'TX errors' in line:
                info_dict['TX errors'] = int(line.split()[2])
        return info_dict