#!/usr/bin/env python
# -*- coding: utf-8 -*- 

class Room:

    source = 'default source'

    def __init__(self, item):
        self.item = item
        self.get_room_img()
        self.get_room_url()
        self.get_room_name()
        self.get_room_owner()
        self.get_room_viewers_count()

    def format_count(self, origin_count):
        origin_count = origin_count.decode('utf-8')
        if( '万' in origin_count):
            count = origin_count.split('万')[0]
            count = int( float(count) * 10000 )
            return count
        return origin_count



class ZhanqiRoom(Room):

    root = 'http://www.zhanqi.tv'
    source = u'战旗'

    def get_room_img(self):
        self.img = self.item.find('img').get('src')
        # print self.img

    def get_room_url(self):
        self.url = self.root + self.item.a['href']
        # print self.url

    def get_room_name(self):
        self.name = self.item.select('.info-area')[0].a.string
        # print self.name

    def get_room_viewers_count(self):
        self.viewers_count = self.item.span.span.string
        # print self.viewers_count

    def get_room_owner(self):
        self.owner = self.item.select('.anchor')[0].string
        # print self.owner

class DouyuRoom(Room):

    root = 'http://www.douyutv.com'
    source = u'斗鱼'

    def get_room_img(self):
        self.img = self.item.img['data-original']

    def get_room_url(self):
        self.url = self.root + self.item.a['href']

    def get_room_name(self):
        self.name = self.item.h1.string

    def get_room_viewers_count(self):
        self.viewers_count = self.item.select('span.view')[0].string

    def get_room_owner(self):
        self.owner = self.item.select('span.nnt')[0].string

class HuyaRoom(Room):

    root = 'http://www.huya.com/'
    source = u'虎牙'

    def get_room_img(self):
        self.img = self.item.img['src']

    def get_room_url(self):
        self.url = self.item.a['href']

    def get_room_name(self):
        self.name = self.item.h6.string.strip()

    def get_room_viewers_count(self):
        self.viewers_count = self.item.select('span.num')[0].contents[1][:-3]

    def get_room_owner(self):
        self.owner = self.item.p.string.strip()