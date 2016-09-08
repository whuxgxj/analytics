#!/usr/bin/env python
# -*- coding:utf8 -*-

import urlparse
from os.path import splitext, basename
from bs4 import BeautifulSoup


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('a', href=True)
    # Remove '#' tag links
    links[:] = [l for l in links if not l['href'].startswith('#')]
    return links


def get_external_links(host_url, base_url, html):
    external_links = {}
    links = get_all_links(html)
    for l in links:
        url = get_absolute_url(base_url, l['href'])
        if not url.startswith(host_url) and url not in external_links:
            text = u' '.join(l.text.split())
            external_links[url] = (text or None)
    return external_links


def get_internal_links(host_url, base_url, html):
    internal_links = {}
    links = get_all_links(html)
    for l in links:
        url = get_absolute_url(base_url, l['href'])
        if url.startswith(host_url) and url not in internal_links:
            print 'base_url = {0} , href= {1} => {2}'.format(base_url,
                                                             l['href'], url)
            text = u' '.join(l.text.split())
            internal_links[url] = (text or None)
    return internal_links


def get_absolute_url(base_url, relative_url):
    base_url = base_url.strip()
    relative_url = relative_url.strip()
    # relative url checking and handling
    page, ext = splitext(basename(base_url))
    if ext or base_url.endswith('/'):
        base_url = base_url
    else:
        base_url = base_url + '/'
    absolute_url = urlparse.urljoin(base_url, relative_url)
    return absolute_url


def clean(str):
    return str.strip().lower()
