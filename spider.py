import json
import time
import requests
import re
import datetime
import pymysql


class Run:
    def __init__(self):
        self.connect = pymysql.connect(
            host='',        # mysql地址
            port=3306,      # 端口
            user='',    # 用户名
            passwd='',      # 密码
            db='',    # 数据库名称
            charset='utf8')
        self.cursor = self.connect.cursor()  # 这里我是先将数据存到mysql数据库，建立游标
        self.cookies = {
            'Registered': '1',
        }

        self.headers = {
            'authority': 'livestatic.titan007.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'pragma': 'no-cache',
            'referer': 'https://live.titan007.com/index2in1.aspx?id=3',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
        }
        self.last_match_flag = True
        self.last_index_flag = True
        self.last_match_dict = dict()
        self.last_index_dict = dict()
        self.ip = self.get_ip()
        self.date_now = ''
        self.match_data = {}
        self.odds_data = {}

    def get_ip(self):
        self.appKey = ''  # 产品ID
        self.appPwd = ''  # 产品密码
        url = f''  # 获取取IP代理API接口
        res = requests.get(url)
        if res.json()['code'] == 200:
            data = res.json()['data']
            ip = data[0]['ip'] + ':' + str(data[0]['port'])
            return ip
        else:
            return self.get_locked_list()

    def get_locked_list(self):
        self.appKey=''  # 产品ID
        self.appPwd=''  # 产品密码
        url = f''  # 获取取IP代理API接口
        res = requests.get(url)
        if res.json()['code'] == 200:
            data = res.json()['data']
            ip = data[0]['proxy'].split(':')[0] + ':' + str(data[0]['proxy'].split(':')[1])
            self.ip = ip
            print(ip)
            return ip
        else:
            return ''

    def remove_ip(self):
        url = f''  # 释放长效IP API接口
        headers = {
            'Host': ''
        }
        res = requests.post(url, headers=headers)
        if res.json()['code'] == 200:
            return True
        else:
            self.get_locked_list();
            print('remove_ip:', res.json()['msg'])
            return False

    def odds_data_check(self, data_list):
        # 指数list校验
        key = f"{data_list[0]}_{data_list[1]}"
        value = data_list[:-1]
        if self.last_index_flag is True:  # 第一次运行程序只做存储不进行对比，并返回True
            self.last_index_dict[key] = value
            return True
        if key not in self.last_index_dict:  # 本次数据的比赛id和指数类型则不存在上一次数据中，则进行存储并返回True
            self.last_index_dict[key] = value
            return True
        elif value == self.last_index_dict[key]:  # 如果上一次数据与本次数据不相同则返回False, 上一次的数据不变
            return False
        elif value != self.last_index_dict[key]:  # 如果上一次数据与本次数据不同则返回True, 并更新上一次的值
            self.last_index_dict[key] = value
            return True

        return False

    def match_data_check(self, data_list):
        # 比赛list校验
        key = f"{data_list[1]}"
        value = data_list[:-1]
        if self.last_match_flag is True:  # 第一次运行程序只做存储不进行对比，并返回True
            self.last_match_dict[key] = value
            return True
        if key not in self.last_match_dict:  # 本次数据的比赛id不存在上一次数据中，则进行存储并返回True
            self.last_match_dict[key] = value
            return True
        elif value == self.last_match_dict[key]:  # 如果上一次数据与本次数据相同则返回False, 上一次的数据不做更新
            return False
        elif value != self.last_match_dict[key]:  # 如果上一次数据与本次数据不同则返回True, 并更新上一次的值
            self.last_match_dict[key] = value
            return True

        return False

    def get_odds_data(self,flag):
        current_datetime = datetime.datetime.now()
        timestamp = int(current_datetime.timestamp())
        params = {
            'r': f'007{timestamp * 1000}',
        }
        proxies = {
            'http': f"socks5://{self.ip}",
            'https': f"socks5://{self.ip}"
        }
        try:
            if flag:
                response = requests.get('https://livestatic.titan007.com/vbsxml/sbOddsData.js', params=params, cookies=self.cookies, headers=self.headers, proxies=proxies, timeout=3)
            else:
                response = requests.get('https://livestatic.titan007.com/vbsxml/sbOddsData.js', params=params, cookies=self.cookies, headers=self.headers)
        except:
            return -1

        file_flag=False
        ids = re.findall(r"sData\[(\d+)\]=\[\[.*?\]\];",response.text)
        # print(ids)
        for id in ids:
            pattern = f"sData\[{id}\]=\[\[.*?\]\];"
            match = re.search(pattern, response.text)
            if match:
                extracted_data = match.group(0)[15:-1].replace(',,,',',"","",""').replace(',,',',"",""').replace('[,','["",')
                try:
                    array = json.loads(extracted_data)
                except:
                    continue
                data = [
                    [id, 'a1',json.dumps(array[0]), timestamp],  # 让球全场（初赔,即赔,滚球）
                    [id, 'o1',json.dumps(array[1]), timestamp],  # 独赢全场（初赔,即赔,滚球）
                    [id, 'd1',json.dumps(array[2]), timestamp],  # 大小球全场（初赔,即赔,滚球）
                    [id, 'a2',json.dumps(array[3]), timestamp],  # 让球半场（初赔,即赔,滚球）
                    [id, 'o2',json.dumps(array[5]), timestamp],  # 独赢全场（初赔,即赔,滚球）
                    [id, 'd2',json.dumps(array[4]), timestamp],  # 大小球全场（初赔,即赔,滚球）
                ]
                for row in data:
                    if '-' in row:
                        continue
                    elif self.odds_data_check(row) is False:  # 此处调用 数据校验函数
                        continue
                    row.remove(timestamp)
                    match_score = self.last_match_dict[row[0]][-3] + '-'+ self.last_match_dict[row[0]][-2]
                    odds_time = self.last_match_dict[row[0]][-1]
                    now_time = datetime.datetime.now()

                    match_time2 = time.localtime(self.last_match_dict[row[0]][5])
                    match_time2 = time.strftime("%Y-%m-%d %H:%M:%S", match_time2)
                    match_time2 = datetime.datetime.strptime(match_time2, "%Y-%m-%d %H:%M:%S")

                    if odds_time == '1':
                        total = ((now_time - match_time2).total_seconds())
                        mins = total / 60
                        odds_time = int(mins)

                    elif odds_time == '2':
                        odds_time = '中'

                    elif odds_time == '3':
                        total = ((now_time - match_time2).total_seconds())
                        mins = total / 60
                        odds_time = int(mins)+45
                    else:
                        match_score = '0-0'
                        odds_time = ''

                    row += [match_score, odds_time]  # 本次数据与上一次请求的数据不同，则给row添加三个元素

                    row.append(timestamp)

                    self.odds_data[id][row[1]] = row[2::]

                    self.sava('odds', row)
                    file_flag = True


            else:
                print("Pattern not found.")
        self.last_index_flag = False  # 仅记录第一次
        if file_flag:
            with open(f'resource/odds_datas_{self.match_date}.json','w') as f:
                f.write(json.dumps(self.odds_data, indent=6))

    def get_match_data(self,flag):
        current_datetime = datetime.datetime.now()
        timestamp = int(current_datetime.timestamp())
        params = {
            'r': f'007{timestamp * 1000}',
        }

        proxies = {
            'http': f"socks5://{self.ip}",
            'https': f"socks5://{self.ip}"
        }
        try:
            if flag:
                response = requests.get('https://livestatic.titan007.com/vbsxml/bfdata_ut.js', params=params, cookies=self.cookies, headers=self.headers, proxies=proxies, timeout=3)
            else:
                response = requests.get('https://livestatic.titan007.com/vbsxml/bfdata_ut.js', params=params, cookies=self.cookies, headers=self.headers)
        except:
            return -1

        file_flag=False
        with open("./1.js", "wb") as fp:
            fp.write(response.content)

        with open("./1.js", "r", encoding='utf-8') as fp:
            data = fp.read()

        match_date = re.findall(r'matchdate=\"(.*)\";', data)[0]
        year = re.findall(r'firstschematchtime=\"(.*)\";', data)[0].split(',')[0]
        self.match_date = year + '-' + match_date.replace('月','-').replace('日','')
        # self.match_date = datetime.datetime.now().date()
        if self.date_now != self.match_date:
            self.date_now = self.match_date
            self.match_data={}
            self.odds_data={}

        data = re.findall(r'A\[\d+\]=\"(.*)\"\.split.*;', data)
        item = {}
        for da in data:
            data_1 = (da.split('^^'))
            id = data_1[0].split('^')[0]
            league_color = data_1[0].split('^')[1]
            league_name = data_1[0].split('^')[2]
            home_name = data_1[1].split('^')[0].replace('<font color=#880000>', '').replace('</font>', '')
            away_name = data_1[2].split('^')[0].replace('<font color=#880000>', '').replace('</font>', '')
            match_time =data_1[3].split('^')[0]
            # print((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

            match_time2 = data_1[3].split('^')[1].split(',')
            month=str(int(match_time2[1])+1)
            if (int(match_time2[1])+1)<10:
                month='0'+str(int(match_time2[1])+1)
            day = int(match_time2[2])
            if int(match_time2[2]) < 10:
                day = '0' + str(match_time2[2])
            match_time2 = f'{match_time2[0]}-{month}-{day} {match_time2[3]}:{match_time2[4]}:{match_time2[5]}'
            # try:
            #     match_time2 = str(datetime.datetime.strptime(match_time, "%Y-%m-%d %H:%M:%S"))
            # except:
            #     match_time2 = f'{match_time2[0]}-{month}-{day} {match_time2[3]}:{match_time2[4]}:{match_time2[5]}'
            #     match_time2 = str(datetime.datetime.strptime(match_time2, "%Y-%m-%d %H:%M:%S"))
            match_time = match_time2.split(" ")[0] + ' ' + match_time+':00'

            match_time2 = time.strptime(match_time2, '%Y-%m-%d %H:%M:%S')
            match_time2 = time.mktime(match_time2)
            match_time2 = int(round(match_time2))

            home_score = data_1[3].split('^')[3]  # 比分元素1
            away_score = data_1[3].split('^')[4]  # 比分元素2
            match_state = data_1[3].split('^')[2]  # 状态

            item[id] = [league_name, match_time, home_name, away_name, home_score, away_score, match_state, timestamp]
            if id not in self.odds_data:
                self.odds_data[id] = {}
            data_list = [self.match_date, id, league_name,league_color, match_time,match_time2, home_name, away_name, home_score, away_score, match_state, timestamp]
            # matchList.append(data_list)
            if self.match_data_check(data_list) is True:
                self.match_data[id]=[id,self.match_date,league_name,league_color, match_time,match_time2, home_name, away_name, home_score, away_score, match_state, timestamp]
                self.sava('match', data_list)
                file_flag = True
                # print(self.match_date, id, league_name, home_name, away_name, match_time, home_score, away_score, match_state)
        self.last_match_flag = False  # 仅记录第一次
        if file_flag:
            # /opt/footballData/
            with open(f'resource/match_datas_{self.match_date}.json', 'w') as f:
                f.write(json.dumps(self.match_data, indent=6))

    def sava(self, t_name, data):
        if t_name == 'odds':
            sql = '''
                insert into m_odds(match_id,odds_type,odds_data,match_score,match_time,create_time) value(%s,%s,%s,%s,%s,%s);
            '''
            self.cursor.execute(sql, data)
            self.connect.commit()

        elif t_name == 'match':
            sql = '''
                    insert into m_match(match_date,old_id,league_name,league_color,match_time,match_time2,
                                               home_name,away_name,home_score,away_score,
                                               match_state,create_time) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            '''
            self.cursor.execute(sql, data)
            self.connect.commit()

    def main(self):
        self.o_time = int(time.time())
        self.count = 0
        flag = False
        if self.ip:
            flag = True
        while True:
            if int(time.time()) - self.o_time > (60*65):
                flag = False
                # if not self.remove_ip():
                #     time.sleep(0.5)
                self.remove_ip()
                time.sleep(0.3)
                self.ip = self.get_ip()
                if self.ip:
                    flag = True
                self.o_time = int(time.time())
                self.count=0

            if self.count > 5:
                flag = False
                if not self.remove_ip():
                    time.sleep(0.5)
                    self.remove_ip()
                time.sleep(0.3)
                self.ip = self.get_ip()
                if self.ip:
                    flag = True
                self.o_time = int(time.time())
                self.count=0

            now = datetime.datetime.now()
            time_content = now.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒')
            try:
                self.get_match_data(flag)  # 先获取比赛数据，以便指数方法提取last_match_dict的数据
                rel = self.get_odds_data(flag)
                print(f"Success {time_content}")
            except Exception as e:
                print(f'ERR {time_content} {e}')
                continue
            if rel == -1:
                self.count+=1
            time.sleep(1)


if __name__ == '__main__':
    run = Run()
    run.main()
    run.connect.close()
