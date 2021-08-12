# Risk Service

## 1 Quick Start

### 环境安装&配置 
* python 版本：3.8以上

* 安装virtualenv
  
  * MacOS: brew install python-virtualenv
    
  > 没有brew? 不了解brew? 请先移步[这里](https://docs.brew.sh/Installation)
  
  * Linux(ubuntu, debian): sudo aptitude install virtualenv
  
* 创建环境
  
* 在项目当前目录，执行: virtualenv --system-site-packages --python=python3.8.2 venv
  
* 启动/关闭环境
  * 在项目目录，执行: source venv/bin/activate 启动python虚拟环境
  * 执行: deactivate 退出python虚拟环境

* 安装依赖(只安装一次)
  
  * 进入python虚拟环境后，在项目目录，执行: pip install -r requirements.txt
  

* 安装mysql 5.7

### 开发环境运行
* 1、安装环境
python install -r requirements.txt
* 2、创建mysql数据库
create database test default character set utf8mb4;
* 3、创建表，在sql地下获取user.sql中的语句创建表
* 4、初始化账号
  python manage.py init_admin_user
* 5、初始化权限
 python manage.py init_permissions
* 6、本地启动
  python manage.py runserver

#### 线上运行
gunicorn -c services/gunicorn_config.py --timeout 300 -w 5 -b 0.0.0.0:5000 services.risk_serv.user:app --preload --log-file /data/logs/gunicorn.log


