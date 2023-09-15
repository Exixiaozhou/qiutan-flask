# qiutan-flask
小程序、浏览器网页、爬虫、后端、mysql

# 环境搭建
python --version
pip requests
pip3 requests
pip3 install requests
pip3 list
pip3 install pymysql

# 安装相关依赖，项目根目录运行
pip list
pip3 list
python -m pip install --upgrade pip
pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt  --trusted-host mirrors.aliyun.com


pip install flask -i https://pypi.doubanio.com/simple/
pip install Flask_Cors -i https://pypi.doubanio.com/simple/
pip install PyMySQL==1.1.0 -i https://pypi.doubanio.com/simple/
pip install PyMySQ -i https://pypi.doubanio.com/simple/

# 运行
python app.py
python3 spider.py 

# 不加gunicorn Linux 后台运行命令
nohup python3 -u /opt/footballData/app.py > /opt/footballData/app_log.log 2>&1 &
nohup python3 -u /opt/footballData/spider.py > /opt/footballData/spider_log.log 2>&1 &

# gunicorn linux 后台运行命令
gunicorn app_test:app -w 8 -b 0.0.0.0:8082 --log-level debug --access-logfile /opt/footballData/app_test_log.log  -D
nohup python3 -u /opt/footballData/spider.py > /opt/footballData/spider_log.log 2>&1 &

# 查看信息
ps -ef | grep python | grep -v grep
# 杀死进程
kill -9 144376

# mysql自行安装，表结构参照football.sql

# 修改配置
## 4.1 修改Flask启动端口
修改启动的端口，在footballData/system/conf/settings.py 修改属性`API_DEFAULT_PORT`

### 4.2.1 接口部分mysql配置信息
在footballData/system/db/mysql_connect.py 修改连接信息
```python
class MYSQL_CONNECT(object):

    def __init__(self):
        self.username = '用户名'  # root
        self.password = '密码' # xxxxxx
        self.host = 'IP地址'  # xx.xx.xx.xx
        self.port = 3306  # mysql 默认端口
        self.db_name = 'football'  # 数据库名称
```
### 4.2.2 爬虫部分mysql配置信息
在footballData/spider.py 修改连接信息
```python
class Run:
    def __init__(self):
        self.connect = pymysql.connect(
            host='',        # mysql地址
            port=3306,      # 端口
            user='root',    # 用户名
            passwd='',      # 密码
            db='qiutan',    # 数据库名称
            charset='utf8')

