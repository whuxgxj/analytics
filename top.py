#!/usr/bin/env python
# -*- coding:utf8 -*-
import logging
import grequests
from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()

head = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Referer': 'https://www.taobao.com',
}

urls = [
    'http://top.baidu.com/buzz?b=2', 'http://top.baidu.com/buzz?b=341',
    'http://top.baidu.com/buzz?b=26', 'http://top.baidu.com/buzz?b=4&c=2',
    'http://top.baidu.com/buzz?b=19&c=3',
    'https://c.api.weibo.com/2/friendships/followers/active_list.json',
    'https://c.api.weibo.com/2/friendships/followers/trend_count.json',
    'https://c.api.weibo.com/2/users/behavior_trend.json',
    'https://top.taobao.com/index.php?spm=a1z5i.1.2.1.hUTg2J&topId=HOME',
    'https://top.etao.com/index.php?spm=a1z5i.3.4.2.SjME2A&topId=TR_FS&leafId=50010850&rank=sale&type=hot',
    'https://mtj.baidu.com/web/demo/overview?appId=468475',
    'http://mobile.umeng.com/apps/4100008dd65107258db11ef4/reports/realtime_summary',
    'http://www.umindex.com/devices/android_models',
    'https://www.appannie.com/apps/ios/top/'
]

current_num = 100

log = logging.getLogger(__name__)


def _handle_grequest_exception(request, exception):
    print exception, request.url
    log.error("{e} with {url}".format(e=exception, url=request.url))
    return None


def handle_end_request(response, verify, cert, proxies, timeout, stream):
    pass
    # print response.status_code, response.encoding, response.url, response.cookies, \
    #     response.headers, response.history, response.raise_for_status(), \
    #     response.content

#urls = ['http://www.csdn.net/'] * 200

rs = (grequests.get(u,
                    headers=head,
                    session=session,
                    params={},
                    hooks={'response': handle_end_request},
                    verify=False) for u in urls)

# ddos
#rs = (grequests.head(u, timeout=1, allow_redirects=False) for u in urls)

res = [
    response
    for response in grequests.map(rs,
                                  stream=False,
                                  size=current_num,
                                  exception_handler=_handle_grequest_exception)
]
