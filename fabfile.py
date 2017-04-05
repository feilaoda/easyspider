# -*- coding: utf-8 -*-
#!/usr/bin/env python

from fabric.api import *

# 远程服务器登陆使用的用户名
env.user = 'root'
# 需要进行操作的服务器地址
env.hosts = ['192.168.1.206']

def pack():
    # 以 tar 归档的方式创建一个新的代码分发
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    # 之处发布产品的名称和版本
    dist = local('python setup.py --fullname', capture=True).strip()
    # 将代码归档上传到服务器当中的临时文件夹内
    put('dist/%s.tar.gz' % dist, '/tmp/coderspider.tar.gz')
    # 创建一个文件夹，进入这个文件夹，然后将我们的归档解压到那里
    # run('mkdir /opt/cs')
    with cd('/opt/cs'):
        run('tar xzf /tmp/coderspider.tar.gz')
        # 使用我们虚拟环境下的 Python 解释器安装我们的包
        # run('python setup.py install')
    # 现在我们的代码已经部署成功了，可以删除这个文件夹了
    run('rm -rf /tmp/yourapplication /tmp/yourapplication.tar.gz')
    # 最终生成 .wsgi 文件，以便于 mod_wsgi 重新加载应用程序
    run('touch /var/www/yourapplication.wsgi')
