import re
import subprocess
NIC ="enp0s3"
# 调用 ifconfig 命令获取网络接口信息
output = subprocess.check_output(["ifconfig", NIC])
print(output.decode())
# 输出匹配到的 RX 和 TX 信息
pattern = r"RX packets (\d+)"
match = re.search(pattern, output.decode())
rx_packets = match.group(1)
print("RX packets:", rx_packets)
pattern = r"RX errors (\d+)"
match = re.search(pattern, output.decode())
rx_errors = match.group(1)
print("RX errors:", rx_errors)
pattern = r"TX packets (\d+)"
match = re.search(pattern, output.decode())
tx_packets = match.group(1)
print("TX packets:", tx_packets)
pattern = r"TX errors (\d+)"
match = re.search(pattern, output.decode())
tx_errors = match.group(1)
print("TX errors:", tx_errors)
