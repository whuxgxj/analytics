#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grequests
from bs4 import BeautifulSoup
import logging
log = logging.getLogger(__name__)
import requests

header = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Referer': 'https://www.taobao.com',
}

current_num = 16

result = {}


def get_urls(base_target_url):
    return [base_target_url + str(page) for page in range(1, 3000)]


def _handle_grequest_exception(request, exception):
    log.error("{e} with {url}".format(e=exception, url=request.url))
    return None


def handle_end_request(response, verify, cert, proxies, timeout, stream):
    soup = BeautifulSoup(response, "html.parser")
    trs = soup.find('table', id='ip_list').find_all('tr')
    for tr in trs[1:]:
        res = {}
        tds = tr.find_all('td')
        if tds[1].find('img') is None:
            res.update({'nation': '未知'})
            res.update({'locate': '未知'})
        else:
            res.update({'nation': tds[1].find('img')['alt'].strip()})
            res.update({'locate': tds[4].text.strip()})
        res.update({'ip': tds[2].text.strip()})
        res.update({'port': tds[3].text.strip()})
        res.update({'anony': tds[5].text.strip()})
        res.update({'protocol': tds[6].text.strip()})
        res.update({'speed': tds[7].find('div')['title'].strip()})
        res.update({'time': tds[9].text.strip()})
        ip = tds[2].text.strip()
        port = tds[3].text.strip()
        print {ip + ':' + port: res}
        #
        check_url = 'https://www.baidu.com/'
        proxies = {
            "http": "http://%s:%s" % (str(ip), str(port)),
            "https": "http://%s:%s" % (str(ip), str(port)),
        }
        r = requests.get(check_url, proxies=proxies)
        if r.raise_for_status() is None:
            result.update({ip + ':' + port: res})


nn = (grequests.get(u,
                    headers=header,
                    params={},
                    hooks={'response': handle_end_request},
                    verify=False)
      for u in get_urls('http://www.xicidaili.com/nn/'))

nt = (grequests.get(u,
                    headers=header,
                    params={},
                    hooks={'response': handle_end_request},
                    verify=False)
      for u in get_urls('http://www.xicidaili.com/nt/'))
wn = (grequests.get(u,
                    headers=header,
                    params={},
                    hooks={'response': handle_end_request},
                    verify=False)
      for u in get_urls('http://www.xicidaili.com/wn/'))

wt = (grequests.get(u,
                    headers=header,
                    params={},
                    hooks={'response': handle_end_request},
                    verify=False)
      for u in get_urls('http://www.xicidaili.com/wt/'))

grequests.map(nn,
              stream=False,
              size=current_num,
              exception_handler=_handle_grequest_exception)
grequests.map(nt,
              stream=False,
              size=current_num,
              exception_handler=_handle_grequest_exception)
grequests.map(wn,
              stream=False,
              size=current_num,
              exception_handler=_handle_grequest_exception)
grequests.map(wt,
              stream=False,
              size=current_num,
              exception_handler=_handle_grequest_exception)

print result
