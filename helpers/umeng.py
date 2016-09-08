#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests
import re
try:
    import simplejson as json
except:
    import json
from datetime import date, timedelta
from helpers.crawler import BaseCrawler
from configs import *

class Umeng(BaseCrawler):
    def __init__(self):
        self.username = umeng_config.get('username')
        self.password = umeng_config.get('password')
        self.start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        self.end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.referer_list = ['http://mobile.umeng.com']
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Host': 'mobile.umeng.com',
            'Referer':'http://mobile.umeng.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.table_stat = [
            'dashboard_general',
            'dashboard_trend',
            'installations',
            'active_users',
            'versions_table',
            'silent_users',
            'launches',
            'retentions',
            'frequency',
            'duration',
            'depth',
            'interval',
            'devices_devices_install',
            'devices_resolutions_install',
            'devices_versions_install',
            'network_access_launches',
            'network_carriers',
            'location_cities',
            'index_details'
        ]
        self.benchmark_stat = [
            'DayNewUser',
            'DayActiveUser',
            'DayLaunchCnt',
            'AvgDuration',
            'WeekActiveUser',
            'WeekActiveRate',
            'MonthActiveUser',
            'MonthActiveRate'
        ]
        self.chart_stat = [
            'error_count',
            'error_rate',
            'error_affect',
            'error_affect_rate',
            'trend_new_users',
            'trend_active_users',
            'trend_new_users_rate',
            'trend_avg_duration',
            'trend_daily_avg_duration',
            'trend_daily_avg_launches',
            'trend_avg_traffic_upload',
            'trend_avg_traffic_download',
            'index_hours_install',
            'versions_trend_active_user',
            'versions_trend_launch',
            'freshness',
            'engagement'
        ]
        self.time_unit = [
            'daily',
            'hourly',
            'weekly',
        ]
        self.stat_type = [
            'daily_per_launch',
            'daily',
            'weekly'
        ]
        self.message_type = ['alien','legit']
        self.extend_stat = ['get_active_user_summary','get_silent_user_summary']
        self.other_stat = ['get_searched_version_errors']
        self.apps = {}
        self.is_login = False
        self.login()
        self.pagesize = 300
        self.urls = self.gen_table_data_url()
        self.urls.extend(self.gen_chart_data_url())
        self.urls.extend(self.gen_extend_url())
        self.urls.extend(self.gen_benchmark_url())
        self.urls.extend(self.gen_other_url())
        super(BaseCrawler, self).__init__(self.urls,params={})

    def get_token(self):
        url = 'http://i.umeng.com/'
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'i.umeng.com',
            'Upgrade-Insecure-Requests': '1',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
        }
        r = requests.get(url=url, headers=headers)
        matchObj = re.search(r'token: \'(\w+)\',', r.text, re.M | re.I | re.S)
        return (matchObj.group(1))

    def login(self):
        if self.is_login is True:
            return True
        token = self.get_token()
        url = 'http://i.umeng.com/login/ajax_do'
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.umeng.com',
            'origin': 'http://i.umeng.com',
            'referer': 'http://i.umeng.com/',
            'user-agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        datas = {
            'token': token,
            'username': self.username,
            'password': self.password,
            'sig': '',
            'sessionid': '',
            'website': 'umengplus',
            'app_id': '',
            'url': ''
        }
        r = requests.post(url=url, data=datas, headers=headers)
        self.is_login = True
        return r.text

    def get_app_list(self):
        url = 'http://mobile.umeng.com/apps/list'
        r = requests.get(url=url, headers=self.headers)
        res = json.load(r.json())
        for app in res:
            self.get_app_channels(app)
            self.get_app_versions(app)
        return self.apps

    #获取每个应用的版本列表
    def get_app_versions(self,app):
        url = 'http://mobile.umeng.com/apps/' + app + '/load_versions'
        r = requests.get(url=url, headers=self.headers)
        res = json.loads(r.json())
        versions = res.get('datas')
        self.apps.update({ app:{'versions':versions} })
        return versions

    #获取每个应用的渠道列表
    def get_app_channels(self,app):
        url = 'http://mobile.umeng.com/apps/' + app + '/load_channels'
        r = requests.get(url=url, headers=self.headers)
        res = json.loads(r.json())
        channels = res.get('datas')
        self.apps.update({ app:{'channels':channels} })
        return channels

    #指标
    def get_predefined_indices(self,app):
        url = 'http://mobile.umeng.com/apps/' + app + '/get_predefined_indices'
        r = requests.get(url=url, headers=self.headers)
        res = json.loads(r.json())
        predefined_indices = res.get('data')
        self.apps.update({ app:{'predefined_indices':predefined_indices} })
        return predefined_indices

    #客服反馈
    def get_feedback(self,app):
        url = 'http://mobile.umeng.com/api/feedback_request_proxy/?path=fb.umeng.com%2Fapi%2Fv2%2Ffeedback%2Fshow2&appkey=' + \
              app + '&count=' + self.pagesize + '&from='+self.start_date+'&to='+self.end_date+'&page=1'
        r = requests.get(url=url, headers=self.headers)
        res = json.load(r.json())
        return res.get('data')

    #生成获取table数据的url
    def gen_table_data_url(self):
        table_data_url = []
        for app,item in self.apps:
            base_url = 'http://mobile.umeng.com/apps/' + app + '/reports/load_table_data?page=1&per_page=' + self.pagesize + \
                       '&start_date=' + self.start_date + '&end_date=' + self.end_date + '&versions%5B%5D=&channels%5B%5D=&segments%5B%5D=&time_unit=daily&stats='
            for stat in self.table_stat:
                table_data_url.append(base_url + stat)
        return table_data_url

    #生成获取chart数据的url
    def gen_chart_data_url(self):
        chart_data_url = []
        for app,item in self.apps:
            base_url = 'http://mobile.umeng.com/apps/' + app + '/reports/load_chart_data?page=1&per_page=' + self.pagesize + \
                       '&start_date=' + self.start_date + '&end_date=' + self.end_date + '&versions%5B%5D=&channels%5B%5D=&segments%5B%5D=&time_unit=daily&stats='
            for stat in self.chart_stat:
                chart_data_url.append(base_url + stat)
        return chart_data_url

    #生成同行数据比较url
    def gen_benchmark_url(self):
        benchmark_url = []
        for app,item in self.apps:
            base_url = 'http://mobile.umeng.com/apps/' + app + '/reports/load_table_data?page=1&per_page=' + self.pagesize + \
                       '&versions%5B%5D=&channels%5B%5D=&segments%5B%5D=&time_unit=weekly&stats=benchmark&cat=allCat'
            for stat in self.benchmark_stat:
                url = base_url = '&item='+stat
                benchmark_url.append(url)
            benchmark_url.extend(base_url)
        return benchmark_url

    #生成其它url
    def gen_extend_url(self):
        extend_url = []
        for app,item in self.apps:
            base_url = 'http://mobile.umeng.com/apps/reports/' + app
            for stat in self.extend_stat:
                extend_url.append(base_url + '/' + stat)
            other_url = 'http://mobile.umeng.com/apps/' + app
            for stat in self.other_stat:
                extend_url.append(other_url + '/' + stat)
        return extend_url

    def gen_other_url(self):
        other_url = []
        for app,item in self.apps:
            other_url.append('http://mobile.umeng.com/apps/'+app+'/reports/load_table_data?stats=dashboard_general')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/reports/load_table_data?stats=dashboard_trend')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/channels/load_table_data?page=1&per_page='+self.pagesize+'&stats=realtime&start_date='+self.start_date+'&end_date='+self.end_date+'&counts=1')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/channels/load_table_data?page=1&per_page='+self.pagesize+'&date=today&stats=list&group_id=')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/wau/get_index_table?stats=wau')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/wau/get_transition_raw_data.json?date='+self.start_date)
            other_url.append('http://mobile.umeng.com/apps/'+app+'/events/load_table_data?page=1&per_page='+self.pagesize+'&versions%5B%5D=&stats=count&show_all=false')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/funnels/load_table_data?page=1&per_page='+self.pagesize+'&period='+self.start_date+'+-+'+self.end_date+'&time_unit=weekly&stats=funnels')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/error_types/search?start_date='+self.start_date+'&end_date='+self.end_date+'&message_type=legit&per_page='+self.pagesize+'&page=0&order_by=desc_error_count')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/error_types/search?start_date='+self.start_date+'&end_date='+self.end_date+'&message_type=alien&per_page='+self.pagesize+'&page=0&order_by=desc_error_count')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/reports/load_chart_data?metric=install&stats=index_versions')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/reports/load_chart_data?metric=install&stats=index_channels')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/wau/get_ratio_trend_chart?start_date='+self.start_date+'&end_date='+self.end_date+'&stats=active')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/channels/load_chart_data?start_date='+self.start_date+'&end_date='+self.end_date+'&versions%5B%5D=&channels%5B%5D=&segments%5B%5D=&time_unit=daily&stats=active_user')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/channels/load_chart_data?start_date='+self.start_date+'&end_date='+self.end_date+'&versions%5B%5D=&channels%5B%5D=&segments%5B%5D=&time_unit=daily&stats=launch')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/channels/load_chart_data?start_date='+self.start_date+'&end_date='+self.end_date+'&versions%5B%5D=&channels%5B%5D=&segments%5B%5D=&time_unit=daily&stats=duration')
            other_url.append('http://mobile.umeng.com/apps/'+app+'/channels/load_chart_data?start_date='+self.start_date+'&end_date='+self.end_date+'&versions%5B%5D=&channels%5B%5D=&segments%5B%5D=&time_unit=daily&stats=day_retention')
        return other_url

    #请求出错处理
    def process_exception(self, request, exception):
        print request.url
        print exception

    #返回结果处理
    def process_response(self, response, verify, cert, proxies, timeout,
                         stream):
        print json.loads(response.content)
        print response.url
