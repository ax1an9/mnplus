# mysdn project

本项目是基于mininet的网络仿真平台，提供便捷的拓扑导入功能，同时可以方便地进行资源监控以及网络监控。

## 目录结构

```shell
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          7/6/2023   4:50 PM                .git
d-----          7/2/2023  11:56 PM                mncontroller
d-----          7/2/2023  11:56 PM                resources
d-----          7/2/2023  11:56 PM                ryucontroller
-a----          7/2/2023  11:56 PM            268 .gitignore
-a----          7/5/2023   9:15 PM           1192 README.CN.md
-a----          7/2/2023  11:56 PM            369 README.md
-a----          7/2/2023  11:56 PM           1592 requirements.txt
```

1. mncontroller：mininet网络控制

   1. ```shell
      Mode                 LastWriteTime         Length Name
      ----                 -------------         ------ ----
      d-----          7/2/2023  11:56 PM                utils #网络感知工具类
      d-----          7/2/2023  11:56 PM                __pycache__
      -a----          7/2/2023  11:56 PM           3613 buildnetwork.py # 根据静态结构来构建网络拓扑
      -a----          7/5/2023  11:40 AM           3614 myrestmn.py # restful 接口：提供一些网络修改的能力，以及感知的网络信息
      -a----          7/5/2023  11:41 AM           6486 netview.py # 网络视图类
      -a----          7/5/2023  11:41 AM           1650 starter.py # 仿真网络启动启动脚本
      -a----          7/2/2023  11:56 PM            611 updateviewtask.py # 定时感知任务
      ```

      

2. ryucontroller：sdn控制器，此处采用ryu作为控制器

   1. ​	

      ```shell
      Mode                 LastWriteTime         Length Name
      ----                 -------------         ------ ----
      d-----          7/2/2023  11:56 PM                __pycache__
      -a----          7/2/2023  11:56 PM           5304 l3swi.py # 控制器样本，模拟3层交换机 
      -a----          7/2/2023  11:56 PM           7202 l4swi.py # 控制器样本，模拟4层交换机
      ```

      

3. resources：常见的一些拓扑结构的表达，可以读入来初始化网络

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
