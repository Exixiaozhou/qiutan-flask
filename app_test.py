
from flask import Flask
from flask_cors import CORS

from system.conf.settings import DEFAULT_SERVICE_NAME
from system.conf.settings import CORS_RESOURCES
from system.conf.settings import CORS_HEADERS
from system.conf.settings import CORS_MAX_AGE
from system.conf.settings import APIConfig
from system.db.routes import GET_DATA


def register_blueprint(app, base_path):
    app.register_blueprint(GET_DATA, url_prefix=f"{base_path}api")


""" 创建app实例对象 """
app = Flask(DEFAULT_SERVICE_NAME)
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)
# app.config.suppress_callback_exceptions = True
api = APIConfig()
# 初始化app.config信息,供后期调用
app.config.from_object(api)
# 调整超时时间
app.config['TIMEOUT'] = 60
# 蓝图Api注册
register_blueprint(app, api.BASE_PATH)
# 解决跨域
CORS(
    app, resources=CORS_RESOURCES, expose_headers=CORS_HEADERS,
    max_age=CORS_MAX_AGE, send_wildcard=True
)

app.run(host=app.config.get('HOST'), port=app.config.get('PORT'), debug=True)

"""
linux启动命令
gunicorn app_test:app -w 8 -b 0.0.0.0:8082 --log-level debug --access-logfile /opt/footballData/app_test_log.log  -D
"""