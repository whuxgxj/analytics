#!/usr/bin/env python
# -*- coding:utf8 -*-
import grequests
import random


class BaseCrawler:
    urls = []
    params = {}
    proxy_ip = []
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Chrome 20.0.1092.0 (Win 7)" useragent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
        'Firefox 12.0 (Win 7 32)" useragent="Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0',
        'Safari 531.21.10 (Win XP)" useragent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10',
        'Firefox 36.0 (Win 8.1 32 bit)" useragent="Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Chrome 22.0.1229.79 (OS X 10_8_2 Intel)" useragent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.79 Safari/537.4',
        'Safari 419.3 (OS X PPC)" useragent="Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3',
        'Chrome 35.0.1916.141 (Samsung SM-T537A) - Android 4.4.2 - " useragent="Mozilla/5.0 (Linux; Android 4.4.2; SAMSUNG-SM-T537A Build/KOT49H) AppleWebKit/537.36 (KHTML like Gecko) Chrome/35.0.1916.141 Safari/537.36',
        'Safari 5.0.2 - iPad - iOS 4_2_1)" useragent="Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
        'UCBrowser 8.6.1 - Webkit 533 - Android 2.3.3" useragent="Mozilla/5.0 (Linux; U; Android 2.3.3; en-us ; LS670 Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1/UCBrowser/8.6.1.262/145/355',
        'Apple iPad - iOS 8_0_2 - Safari 7 (9537.53)" useragent="Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML like Gecko) Mobile/12A405 Version/7.0 Safari/9537.53',
        'Samsung GT-P7100 - Android 3.0.1 - AppleWebKit 534.13" useragent="Mozilla/5.0 (Linux; U; Android 3.0.1; en-us; GT-P7100 Build/HRI83) AppleWebkit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
        'iPhone - iOS 7_1_2 - Safari 7" useragent="Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
        'Android 4.4.2 - Chrome 35.0.1916.141" useragent="Mozilla/5.0 (Linux; Android 4.4.2; SAMSUNG-SM-T537A Build/KOT49H) AppleWebKit/537.36 (KHTML like Gecko) Chrome/35.0.1916.141 Safari/537.36',
    ]
    referer_list = [
        'https://www.taobao.com',
        'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=taobao',
        'http://news.qq.com/photo.shtml', 'https://www.zhihu.com/wujun',
        'http://weibo.com/2478838621', 'http://blog.sina.com.cn/lm/sports/',
        'https://www.so.com/s?q=taobao',
        'https://www.sogou.com/web?query=taobao'
    ]
    random.shuffle(user_agent_list)
    random.shuffle(referer_list)
    header = {
        'User-Agent': user_agent_list[-1],
        'Referer': referer_list[-1],
    }
    current_num = 32
    timeout = 30

    def __init__(self, urls, params):
        self.urls = urls
        self.params = params
        self.rs = (grequests.post(u,
                                  headers=self.header,
                                  params=self.params,
                                  hooks={'response': self.process_response},
                                  verify=False,
                                  timeout=self.timeout) for u in self.urls)
        self.response_list = [response
                              for response in grequests.map(
                                  self.rs,
                                  stream=False,
                                  size=self.current_num,
                                  exception_handler=self.process_exception)]

    def process_exception(self, request, exception):
        print exception, request.url

    def process_response(self, response, verify, cert, proxies, timeout,
                         stream):
        print response.status_code, response.encoding, response.url, response.cookies, \
            response.headers, response.history, response.raise_for_status(), \
            response.content,verify,cert,proxies,timeout,stream
