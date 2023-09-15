from flask import Blueprint
from system.db.controller import HelloWord
from system.db.controller import GetListData
from system.db.controller import GetIndexData

GET_DATA = Blueprint('api', __name__, static_folder='', static_url_path='')

# 蓝图注册类视图
GET_DATA.add_url_rule('/matchList', view_func=GetListData.as_view('GetListData'))
GET_DATA.add_url_rule('/oddsById', view_func=GetIndexData.as_view('GetIndexData'))
GET_DATA.add_url_rule('/helloWord', view_func=HelloWord.as_view('HelloWord'))
