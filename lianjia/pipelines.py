# -*- coding: utf-8 -*-
import os
import traceback
import urllib

import pymysql
from scrapy import log
from twisted.enterprise import adbapi

from lianjia import settings


class LianjiaPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        imagePath = self.savePic(item, spider)
        item['imagePath'] = imagePath
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def savePic(self, item, spider):
        dir_path = '%s/%s' % (settings.imageStoredPath, spider.name)  # 存储路径
        print '-----------------------' + dir_path
        file_path =''
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for image_url in item['imageUrl']:
            print '+++++++++++++++++++++++' + image_url
            list_name = image_url.split('/')
            file_name = list_name[len(list_name) - 1]
            file_path = '%s/%s' % (dir_path, file_name)
            if os.path.exists(file_name):
                continue
            with open(file_path, 'wb') as file_writer:
                conn = urllib.urlopen(image_url)
                file_writer.write(conn.read())
            file_writer.close()
        return file_path

    def _conditional_insert(self, tx, item):

        try:
            #print title, houseType, acreage, residentialName
            print '---------------------------------------'
            print 'title -----------------' + item['title']
            print 'age -----------------' + item['age']
            tx.execute("SELECT title FROM sencondhandhouse where title='" + item['title'] + "'")
            result = tx.fetchone()
            if result:
                tx.execute(
                    "update sencondhandhouse set houseType='" + item['houseType'] + "',acreage='" + item['acreage'] + "',residentialName='" + item['residentialName'] + "' where title='" + item['title'] + "'")
            else:
                tx.execute(
                    "insert into sencondhandhouse(city,district,realEstateAgent,age,houseType,unitPrice,price,residentialName,publicTime,acreage,title,imagePath) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    ("", item['district'], "", item['age'], item['houseType'], item['unitPrice'], item['price'], item['residentialName'], item['publicTime'], item['acreage'], item['title'], item['imagePath']))
        except:
            print 545445455545445455545445455545445455545445455545445455545445455545445455
            traceback.print_exc()

    def handle_error(self, e):
        log.err(e)
