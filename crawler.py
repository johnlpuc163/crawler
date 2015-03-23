#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import logging
import threading
import time
import urllib2

from bs4 import BeautifulSoup
import redis

from room import (DouyuRoom, ZhanqiRoom, HuyaRoom)

r = redis.StrictRedis(host='pub-redis-11890.us-east-1-2.3.ec2.garantiadata.com', port=11890, db=0, password='123456')


class Crawler():
    name = 'base_crawler'

    def store_to_redis(self):
        pipe = r.pipeline()
        for i in xrange(len(self.rooms)):
            room = self.rooms[i]
            id = 'dota:{platform}:{index}'.format(platform=self.name, index=i)
            pipe.hmset(id, 
                       {
                        'img': room.img,
                        'url': room.url,
                        'name': room.name,
                        'viewers_count': room.viewers_count,
                        'owner': room.owner,
                        'source': self.name,
                        })
        pipe.execute()




class ZhanqiCrawl(Crawler):

    name = u'zhanqi'

    def crawl(self, url='http://www.zhanqi.tv/games/dota2', count=5):
        content = urllib2.urlopen(url).read()
        html = BeautifulSoup(content)
        lis = html.find(id='hotList').find_all('li')
        self.rooms = []
        for i in xrange(count):
            li = lis[i]
            self.rooms.append(ZhanqiRoom(li))
        self.store_to_redis()
        return self.rooms



class DouyuCrawl(Crawler):

    name = u'douyu'

    def crawl(self, url='http://www.douyutv.com/directory/game/DOTA2', count=5):
        content = urllib2.urlopen(url).read()
        html = BeautifulSoup(content)
        lis = html.find(id='item_data').find_all('li')
        self.rooms = []
        for i in xrange(count):
            li = lis[i]
            self.rooms.append(DouyuRoom(li))
        self.store_to_redis()
        return self.rooms

class HuyaCrawl(Crawler):

    name = u'huya'

    def crawl(self, url='http://www.huya.com/g/dota2', count=5):
        content = urllib2.urlopen(url).read()
        html = BeautifulSoup(content)
        lis = html.find(id='video-item-live').find_all('li')
        self.rooms = []
        for i in xrange(count):
            li = lis[i]
            self.rooms.append(HuyaRoom(li))
        self.store_to_redis()
        return self.rooms  







def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='(%(threadName)-10s) %(message)s',
                        )

    def worker(crawler):
        """thread worker function"""
        logging.debug('make request from' + crawler.name)
        rooms.extend(crawler.crawl())
        logging.debug('done')
        return

    crawlers = [ZhanqiCrawl(), DouyuCrawl(), HuyaCrawl()]
    while(True):
        logging.debug('awake!')
        rooms = []

        for crawler in crawlers:
            t = threading.Thread(target=worker, args=(crawler,))
            t.start()

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            logging.debug('joining %s', t.getName())
            t.join()
        logging.debug('sleeping!')
        time.sleep(5)


if __name__ == "__main__":
    main()

