#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2020/4/25 4:29 下午
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : deploy_sealos.py
# 本脚本需要在当前区域只有有 4 台刚创建的前提下执行

import datetime
import json
import telnetlib

import paramiko
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from scp import SCPClient

aliyun_password = '4 台阿里云服务器的密码'


class Sealos(object):
    def __init__(self, region_id):
        self.access_id = ''
        self.access_secret = ''
        self.region_id = region_id
        self.ssh_client = None
        self.private_ip_list = []

        self.client = AcsClient(self.access_id, self.access_secret, self.region_id)

    @staticmethod
    def listen_server_status(ip, port=22):
        """检测服务器 22 端口是否开启"""
        is_on = False
        try:
            telnetlib.Telnet(host=ip, port=port, timeout=2)
            is_on = True
        except Exception as e:
            print(f'server {ip}:{port}: {e}')
        finally:
            return is_on

    def install_docker(self):
        """
        初始化 ECS
        SSH 连接服务器
        安装并启动 docker
        """
        instances = self.get_instances()
        for instance in instances:
            public_ip = self.get_instance_public_ip(instance)
            # 判断服务器的 22 端口是否启动
            while True:
                server_status = self.listen_server_status(public_ip)
                if server_status:
                    break
            print(f'服务器 {public_ip} 已经准备好')

            self.ssh_ecs(public_ip, 'root', aliyun_password)
            self.exec_cmd('yum install -y docker && systemctl start docker')  # 安装并启动 docker
            self.exec_cmd('docker -v && docker ps -a')  # 检查 docker 是否安装成功
            self.ssh_client.close()

    def get_instances(self):
        """
        获取 ECS 实例
        :return 按照内网 IP 的顺序返回实例列表
        """
        request = DescribeInstancesRequest()
        request.set_accept_format('json')

        response = self.client.do_action_with_exception(request)
        # print(str(response, encoding='utf-8'))
        response = json.loads(response)
        instances = response['Instances']['Instance']
        # 按照内网地址为ECS实例排序
        instances.sort(key=lambda k: k['VpcAttributes']['PrivateIpAddress']['IpAddress'][0])
        for instance in instances:
            private_ip = self.get_instance_private_ip(instance)
            self.private_ip_list.append(private_ip)
        return instances

    @staticmethod
    def get_instance_public_ip(instance):
        """获取 ECS 实例的公网 IP"""
        return instance['PublicIpAddress']['IpAddress'][0]

    @staticmethod
    def get_instance_private_ip(instance):
        """获取 ECS 实例的内网 IP"""
        return instance['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]

    def ssh_ecs(self, hostname, user, pwd):
        """SSH 连接到 ECS 实例"""
        # 实例化SSHClient
        self.ssh_client = paramiko.SSHClient()
        # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接SSH服务端，以用户名和密码进行认证
        try:
            self.ssh_client.connect(hostname=hostname, port=22, username=user, password=pwd, auth_timeout=60,
                                    banner_timeout=300)
        except Exception as e:
            print(f'服务器 {hostname} SSH 连接失败：{e}')

    def exec_cmd(self, cmd):
        if self.ssh_client:
            print(f'Executing: {cmd}')
            # 打开一个Channel并执行命令
            # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            # 打印执行结果
            print(stdout.read().decode('utf-8'))
            print(f'Executed: {cmd}')
        else:
            print('未登录 ECS')

    def login_master_1(self):
        instances = self.get_instances()
        if len(instances) > 0:
            public_ip = self.get_instance_public_ip(instances[0])
            self.ssh_ecs(public_ip, 'root', aliyun_password)
        else:
            print(f'{self.region_id} 无 ECS 实例')

    def upload(self, local_path, remote_path="/root"):
        instances = self.get_instances()
        if len(instances) > 0:
            host = self.get_instance_public_ip(instances[0])

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect(host, 22, 'root', aliyun_password)
            scp_client = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
            try:
                scp_client.put(local_path, remote_path)
            except FileNotFoundError as e:
                print(e)
                print("系统找不到指定文件" + local_path)
            else:
                print("文件上传成功")
            finally:
                ssh_client.close()
        else:
            print('无服务器！！！')

    def download_kubernetes_sealos(self):
        """登录 master1 下载 kubernetes/sealos"""
        self.login_master_1()
        self.exec_cmd(
            'wget -c https://sealyun.oss-cn-beijing.aliyuncs.com/latest/sealos && chmod +x sealos && mv sealos /usr/bin ')
        self.exec_cmd(
            'wget -c https://sealyun.oss-cn-beijing.aliyuncs.com/d551b0b9e67e0416d0f9dce870a16665-1.18.0/kube1.18.0.tar.gz ')
        self.ssh_client.close()

    def install_sealos(self):
        """登录 master1 安装 sealos"""
        self.login_master_1()
        # 创建集群的时候使用内网 IP
        ips = self.private_ip_list
        cmd = f"""sealos init --passwd {aliyun_password} \
	--master {ips[0]}  --master {ips[1]}  --master {ips[2]}  \
	--node {ips[4]} \
	--pkg-url /root/kube1.18.0.tar.gz \
	--version v1.18.0"""
        self.exec_cmd(cmd)
        self.ssh_client.close()

    def check_sealos(self):
        self.login_master_1()
        # 检测是否安装成功
        self.exec_cmd('kubectl get node')
        self.exec_cmd('kubectl get pod --all-namespaces')
        self.ssh_client.close()


if __name__ == '__main__':
    start = datetime.datetime.now()
    seal = Sealos(region_id='cn-zhangjiakou')
    seal.install_docker()
    seal.download_kubernetes_sealos()
    seal.install_sealos()
    seal.check_sealos()
    end = datetime.datetime.now()
    print((end - start).seconds)
