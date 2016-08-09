import os
import re
import time

import urllib3
import urllib3.util

import parser_soup


def get_top_domain(url):
    try:
        return '.'.join(urllib3.util.parse_url(url).host.split('.')[-2:])
    except:
        return None

class Crawler(object):
    def __init__(self, url, querry, dir = os.path.dirname(__file__)):
        self.start_url = url
        self.start_parsed = urllib3.util.parse_url(url)
        self.query = re.compile(querry, re.IGNORECASE)
        self.dir = dir
        self.__horizon = set()
        self.log = []

        self.__horizon.add(url)
        self.log.append(url)
        print("initializing crawler....")
        print(locals())

    def start(self, depth= 5, url = '/'):
        print(url, depth)
        self.log.append(url)
        if depth > 0:
            pool = urllib3.PoolManager()
            data = pool.request("GET", self.start_url if url == '/' else url).data.decode('utf-8')

            valid_list = []
            self.add_horizon(parser_soup.get_links(data), valid_list)

            if re.search(self.query, parser_soup.get_text(data)):
                self.output(data)

            for u in valid_list:
                self.start(depth = (depth-1), url = u)

    def output(self, data):
        with open(os.path.join(self.dir, get_top_domain(self.start_parsed.host) + '.' + str(time.time()) + '.html'), 'w+') as f:
            f.write(data)

    def add_horizon(self, url_list, valid_list = []):
        for url in url_list:
            if get_top_domain(url) == get_top_domain(self.start_parsed.host)  \
                    and (not str(url) in self.log or not str(url) in self.__horizon):
                valid_list.append(str(url))

        self.__horizon.update(valid_list)

if __name__ == "__main__":
    nytimes = Crawler('https://www.theguardian.com', 'trump')

    # nytimes.start(depth=3)
    try:
        nytimes.start(depth=3)
    except Exception as s:
        print(s.args)
    finally:
        print(nytimes.log)
        with open(os.path.join(os.path.dirname(__file__), 'log.txt'), 'w+') as f:
            f.write(',\r'.join(map(str, nytimes.log)))