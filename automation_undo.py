import json
import random
import os 
import re

import requests

import client
from settings import *


class Undo:
    def __init__(self, req, LOG_DATA):
        self.req = req
        # self.req.proxies = {'http': '127.0.0.1:8888', 'https': '127.0.0.1:8888'}
        # self.req.verify = False
        self.LOG_DATA = LOG_DATA
        self.identity_list_url = 'https://churenkyosystem.com/member/identity_list.php'
        self.identity_name_url = 'https://churenkyosystem.com/member/identity_name_list.php?IDENTITY_ID={}'
        self.i_nup_e_url = 'https://churenkyosystem.com/member/identity_nameupload_edit.php?IDENTITY_ID={}'
        self.info = '{0}（{1}）：{2}名'.format(self.LOG_DATA[1], self.LOG_DATA[2], self.LOG_DATA[3])
        # 登录页面url
        self.login_url = 'https://churenkyosystem.com/member/login.php'

    # 1、 进入搜索信息搜索列表，并搜索指定ID
    def search_info(self):
        print('进入搜索信息搜索列表，并搜索指定ID')
        data = {
            'CODE': self.LOG_DATA[-1],
            'PAGE_VIEW_NUMBER': '0',
            'BTN_SEARCH_x': '検 索',
        }

        res = self.req.post(self.identity_list_url, data=data)
        reg = r'<a href="identity_info\.php\?IDENTITY_ID=(.*?)">{}</a>'.format(self.LOG_DATA[-1])
        self.identity_id = re.findall(reg, res.text)[0]
        print(self.identity_id)
       

    # 2、执行撤销操作
    def undo(self):
        data = {
            'IDENTITY_ID': self.identity_id,
            'CANCEL_TYPE': random.choice(['2', '3'])
        }
        res = self.req.post('https://churenkyosystem.com/member/set_cancel_identity.php', data=data)
        if res.url == self.login_url:
            print(res.url)
            c = client.ClientLogin()
            c.run
            self.req = c.req
            res = self.req.get('https://churenkyosystem.com/member/set_cancel_identity.php', data=data)
        sleep(3)

        japan_url = 'http://www.mobtop.com.cn/index.php?s=/Api/MalaysiaApi/japanVisaStatus'
        data = {'tid': self.LOG_DATA[-2], 'submit_status': '111'}
        res = requests.post(japan_url, data=data).json()
        if res['status'] == 1:
            print('==========\n撤回请求成功!\n==========')
        
        with open(os.path.join(LOG_DIR, f'{DAY()}.json'), 'a') as f:
            log = {'撤销': self.LOG_DATA, 'id': self.LOG_DATA[-1], 'time': strftime('%m/%d %H:%M:%S')}
            json.dump(log, f)
            f.write(',\n')

        res = self.req.get('https://churenkyosystem.com/member/top.php')
        if res.url == self.login_url:
            c = client.ClientLogin()
            c.run
            self.req = c.req
            res = self.req.get('https://churenkyosystem.com/member/top.php')
   
    @property
    def run(self):
        sleep(1)
        try:
            self.search_info()
            sleep(1)
            self.undo()
        except:
            pass