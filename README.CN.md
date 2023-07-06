# mysdn project

本项目是基于mininet的网络仿真平台，提供便捷的拓扑导入功能，同时可以方便地进行资源监控以及网络监控。

## 运行前准备

> 安装依赖:

在特定虚拟机的基础上：

```shell
sudo pip install bottle

sudo pip install psutil
```

**OR** 从零开始：

```shell
sudo pip install -r requirements.txt
```

## 常见问题

> 缺乏权限：

由于虚拟网络涉及许多需要root权限的操作，启动本平台请使用sudo

```
sudo
```

> 清理minnet网络

如果关于mininet的进程没有被正常关闭，就可能需要手动清理之前的虚拟网络的信息:

```
sudo mn -c
```


## 运行

> **在starter.py内指定controller端口和拓扑文件！**

```python
# in starter.py
# 打开文件并读取 init topo JSON 数据
with open('./resources/topos/moredetailbase.json', 'r') as file:
    data = json.load(file)
```

> 指定controller的信息

```python
# in starter.py
c0 = net.addController('c0', controller=RemoteController,
                        ip='127.0.0.1', port=6653)
```

> 运行网络平台的controller来启动网络仿真平台:

```shell
sudo python mncontroller/stater.py
```

