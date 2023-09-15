# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from system.conf.settings import DEFAULT_SERVICE_NAME
from system.conf.settings import CORS_RESOURCES
from system.conf.settings import CORS_HEADERS
from system.conf.settings import CORS_MAX_AGE
from system.conf.settings import APIConfig
from system.db.routes import GET_DATA


def create_app_instance():
    """ 创建app实例对象 """
    app = Flask(DEFAULT_SERVICE_NAME)
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
    # 加入中间件
    return app


def register_blueprint(app, base_path):
    app.register_blueprint(GET_DATA, url_prefix=f"{base_path}api")


def main():
    app = create_app_instance()
    # logger.info("Start Run Epidemic_System Api")
    """ 调用创建app实例 """
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'), debug=True)


if __name__ == "__main__":
    main()


"""
安装模块  pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt  --trusted-host mirrors.aliyun.com
"""
