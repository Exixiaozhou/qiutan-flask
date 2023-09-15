import re
import datetime
from datetime import datetime as d1
from flask.views import MethodView
from flask import request
from flask import jsonify
from system.db.utils import find_match_data, find_odds_data, find_match_json
from system.conf.loggers import logger


class GetListData(MethodView):
    """ 获取list接口数据 """
    __methods__ = ['GET']

    def get(self):
        try:
            url = request.url
            re_object = re.search(pattern='date=(.{9,10})', string=url)
            date = None if re_object is None else re_object.group(1).strip()
            logger.info(f"date={date}")
            # result = find_match_data(s_date)
            result = find_match_json(date)
            if result['success'] is False:
                last_date = (d1.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
                result = find_match_json(last_date)
            logger.info(result['message'])
            result['code'] = 200 if result['success'] is True else 205
        except Exception as e:
            logger.info(f"Error matchList {e}")
            result = {"code": 400, "message": "服务器异常", "data": []}
        response = jsonify(result)
        return response


class GetIndexData(MethodView):
    """ 获取指数接口数据 """
    __methods__ = ['GET']

    def get(self):
        try:
            url = request.url
            re_object = re.search(pattern='matchId=([0-9]{7,8})', string=url)
            matchId = None if re_object is None else re_object.group(1)
            re_object = re.search(pattern='oddsType=([a-zA-Z0-9]{2,3})', string=url)
            oddsType = None if re_object is None else re_object.group(1)
            logger.info(f"matchId={matchId}, oddsType={oddsType}")
            result = find_odds_data(matchId, oddsType)
            logger.info(result['message'])
            result['code'] = 200 if result['success'] is True else 205
        except Exception as e:
            logger.info(f"Error oddsById {e}")
            result = {"code": 400, "message": "服务器异常", "data": []}
        response = jsonify(result)
        return response


class HelloWord(MethodView):
    __methods__ = ['GET']

    def get(self):
        return "Hello Word!"
