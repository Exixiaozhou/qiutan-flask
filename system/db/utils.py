import os
import time
import json
import datetime
from datetime import datetime as d1
from system.db.mysql_connect import sql_execute
from system.conf.loggers import logger
from system.conf.settings import SpiderDataFileConfig


def json_read(file_path, read_count=3):
    with open(file=file_path, mode='r', encoding='utf-8') as fis:
        content = fis.read().strip()
    if read_count < 1:
        return []
    if len(content) > 1:
        try:
            json_data = json.loads(content)
            return json_data
        except Exception as e:
            logger.info(f"Error Json Parse {e}")
    time.sleep(0.2)
    json_read(file_path=file_path, read_count=read_count - 1)


def new_dict_sort(data_dict):
    format_str = '%Y-%m-%d %H:%M:%S'
    desc_dict = {k: v for k, v in sorted(data_dict.items(), key=lambda x: d1.strptime(x[1][1], format_str), reverse=True)}
    result = {k: v for k, v in sorted(desc_dict.items(), key=lambda x: float(x[1][6]), reverse=True)}
    return list(result.values())


def match_list_add_key(value, match_id):
    matchTime = time.strptime(value[4], '%Y-%m-%d %H:%M:%S')
    matchTime = time.mktime(matchTime)
    matchTime = int(round(matchTime))
    data = {
        'matchId': match_id,'oldId': match_id,'matchDate': value[1],'leagueName': value[2],'leagueColor': value[3], 'matchTime':matchTime,'matchTime2': value[5], 'homeName': value[6], 'awayName': value[7],
        'homeScore': value[8], 'awayScore': value[9], 'matchState': value[10], 'createTime': value[11]
    }
    return data


def join_index_json(match_json_data, index_json_data):
    data_dict = dict()
    for match_id in match_json_data:
        value = match_json_data[match_id]
        data = match_list_add_key(value, match_id)
        if match_id in index_json_data:
            data['a1'] = index_json_data[match_id].get('a1', '')
            if type(data['a1']) is dict:
                data['a1'] = data['a1'].get('oddsData', '')
            data['a2'] = index_json_data[match_id].get('a2', '')
            if type(data['a2']) is dict:
                data['a2'] = data['a2'].get('oddsData', '')
            data['o1'] = index_json_data[match_id].get('o1', '')
            if type(data['o1']) is dict:
                data['o1'] = data['o1'].get('oddsData', '')
            data['o2'] = index_json_data[match_id].get('o2', '')
            if type(data['o2']) is dict:
                data['o2'] = data['o2'].get('oddsData', '')
            data['d1'] = index_json_data[match_id].get('d1', '')
            if type(data['d1']) is dict:
                data['d1'] = data['d1'].get('oddsData', '')
            data['d2'] = index_json_data[match_id].get('d2', '')
            if type(data['d2']) is dict:
                data['d2'] = data['d2'].get('oddsData', '')
        data_dict[match_id] = data
    return dict_sort(data_dict) if len(data_dict) > 0 else data_dict


def find_match_json(date):
    resource_path = SpiderDataFileConfig.ResourceDirectoryPath.value
    match_file_path = os.path.join(resource_path, f"match_datas_{date}.json")
    index_file_path = os.path.join(resource_path, f"odds_datas_{date}.json")
    if os.path.exists(match_file_path) is False:
        status_content = f"数据查询失败"
        return {'message': status_content, 'success': False, "data": []}
    match_json_data = json_read(file_path=match_file_path, read_count=3)
    index_json_data = find_index_json(index_file_path)['data']  # 获取指数的数据
    data_dict = join_index_json(match_json_data, index_json_data)
    status_content = f"数据查询成功{len(data_dict)}"
    status = True if len(data_dict) > 0 else False
    return {'message': status_content, 'success': status, "data": data_dict}


def index_list_add_key(data):
    data_dict = dict()
    for match_id in data:
        items = data[match_id]
        data_dict[match_id] = {}
        for odds_type in items:
            value = items[odds_type]
            data_dict[match_id][odds_type] = {
                'oddsData': value[0], 'matchScore': value[1],'matchTime': value[2], 'createTime': value[3],
                 'oddsType': odds_type, 'matchId': match_id
            }
    return data_dict


def find_index_json(index_file_path, match_id=None, odds_type=None):
    if os.path.exists(index_file_path) is False:
        status_content = f"数据查询失败 {index_file_path} 文件不存在"
        return {'message': status_content, 'success': False, "data": []}
    data = json_read(file_path=index_file_path, read_count=3)
    status_content = f"数据查询成功 {index_file_path}"
    # if match_id is not None and odds_type is None:
    #     recent_index_date = [recent_index_date[match_id]] if match_id in recent_index_date else []
    # elif match_id is not None and odds_type is not None:
    #     if match_id in recent_index_date and odds_type in recent_index_date[match_id]:
    #         recent_index_date = [recent_index_date[match_id][odds_type]]
    #     else:
    #         recent_index_date = []
    try:
        recent_index_date = index_list_add_key(data) if len(data) > 0 else []
        status = True if len(recent_index_date) > 0 else False
    except Exception as e:
        status = False
        recent_index_date = []
        logger.info(f"Error Find index json {e}")
    return {'message': status_content, 'success': status, "data": recent_index_date}


def recent_data_filter(data_list, id_type):
    data_dict = dict()
    for data in data_list:
        keys = str(data[id_type]) if id_type == 'match_id' else f"{data[id_type]}_{data['odds_type']}"
        time_stamp = int(data['datetime'])
        if keys in data_dict:
            data_dict[keys] = data if time_stamp > int(data_dict[keys]['datetime']) else data_dict[keys]
        else:
            data_dict[keys] = data
    return data_dict


def index_filter_controller(match_date):
    current_date = match_date
    last_date = (d1.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    next_date = (d1.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    date_list = [last_date, current_date, next_date]
    all_index_date_dict = dict()
    for date in date_list:
        odds_data = find_odds_data(match_date=date)['data']
        for key in odds_data:
            all_index_date_dict[key] = odds_data[key]
    return all_index_date_dict


def dict_sort(data_dict):

    desc_dict = {k: v for k, v in sorted(data_dict.items(), key=lambda x:x[1]['matchTime'], reverse=True)}
    result = {k: v for k, v in sorted(desc_dict.items(), key=lambda x: float(x[1]['matchState']), reverse=True)}

    modelList=[];
    for match_id in result:
        try:
            if "a1" in result[match_id]:
                if result[match_id]['a1']:
                    modelList.append(result[match_id])
        except Exception as e:
            print('ERR', e)
            logger.info(f"{match_id} {result}")
    return modelList


def list_data_build(data_list, id_type, match_date):
    # 根据比赛ID 调用指数查询方法
    recent_match_data = recent_data_filter(data_list, id_type)
    recent_odds_data = index_filter_controller(match_date)
    for key in recent_match_data:
        recent_match_data[key]['odds_data'] = []
    for key in recent_odds_data:
        match_id = str(key).split('_')[0]
        if match_id not in recent_match_data:  # 如果指数中的比赛ID不存在比赛数据表中
            continue
        elif len(recent_match_data[match_id]['odds_data']) < 1:
            recent_match_data[match_id]['odds_data'] = [recent_odds_data[key]]
        elif match_id in recent_match_data:
            recent_match_data[match_id]['odds_data'] += [recent_odds_data[key]]
    return dict_sort(recent_match_data)


def sql_find_controller(table_name, sql):
    try:
        result = sql_execute(sql)
        status_content = f"mysql {table_name} 数据查询成功 {sql}"
        logger.info(status_content)
    except Exception:
        status_content = f"mysql {table_name} 数据查询失败 {sql}"
        logger.info(status_content)
        return {'message': status_content, 'success': False, "data": []}
    return {'message': status_content, 'success': True, "data": result}


def find_match_data(match_date=None):
    # 比赛查询
    id_type = 'old_id'
    match_table_name = 'm_match'
    sql = f"SELECT * FROM {match_table_name} WHERE match_date = '{match_date}'"
    try:
        data = sql_execute(sql)
        status_content = f"mysql {match_table_name} 数据查询成功 {sql}"
        logger.info(status_content)
    except Exception:
        status_content = f"mysql {match_table_name} 数据查询失败 {sql}"
        logger.info(status_content)
        return {'message': status_content, 'success': False, "data": []}
    list_data = list_data_build(data, id_type, match_date) if len(data) > 0 else []
    status = True if len(data) > 0 else False
    return {'message': status_content, 'success': status, "data": list_data}


def find_odds_data(matchId=None, oddsType=None, mysql_cursor=None):
    # 指数查询
    id_type = 'match_id'
    index_table_name = 'm_odds'
    if matchId is None:
        status_content = f"请传入参数：match_id"
        return {'message': status_content, 'success': False, "data": []}
    elif oddsType is None:
        sql = f"SELECT * FROM {index_table_name} WHERE {id_type} = '{matchId}'"
    else:
        sql = f"SELECT * FROM {index_table_name} WHERE {id_type} = '{matchId}' and odds_type = '{oddsType}'"
    try:
        data = sql_execute(sql) if mysql_cursor is None else mysql_cursor.sql_find_execute(sql)
        status_content = f"数据查询成功"
        logger.info(status_content)
    except Exception:
        status_content = f"数据查询失败"
        logger.info(status_content)
        return {'message': status_content, 'success': False, "data": []}
    status = True if len(data) > 0 else False
    # recent_index_date = recent_data_filter(data, id_type) if len(data) > 0 else {}
    # data_list = list(recent_index_date.values()) if match_date is None else recent_index_date
    return {'message': status_content, 'success': status, "data": convert_field_names(data)}


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


# 遍历JSON数据，转换字段命名
def convert_field_names(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            new_key = snake_to_camel(key)
            new_value = convert_field_names(value)
            new_obj[new_key] = new_value
        return new_obj
    elif isinstance(obj, list):
        return [convert_field_names(element) for element in obj]
    else:
        return obj


# find_match_json("2023-08-15")

# find_match_data("2023-08-15")
# sql_cursor.close_connect()
# find_odds_data("235293512")
# find_odds_data("2352935", 'o1')
