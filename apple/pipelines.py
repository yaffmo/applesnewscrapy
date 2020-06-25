# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from .models import AppleDB, db_connect, create_table
import psycopg2
# from scrapy.exceptions import DropItem
class ApplePipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        !!!每一次都會呼叫!!!所以要視為單獨item要通過的pipeline
        """

        session = self.Session()
        # titles = session.query(AppleDB.title).all()
        # for title in titles:
        #     if title == item["title"]:
        #         raise DropItem('found null title %s', item)
        #     else:
        appledb = AppleDB()
        appledb.title = item["title"]
        appledb.content = item["content"]
        # !終於成功拉!資料庫去重>>當資料庫沒有一樣的標題時>>存入資料庫
        if session.query(AppleDB).filter_by(title=item['title']).first() == None:
            try:
                session.add(appledb)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    
    # def open_spider(self, spider):
    #     hostname = 'localhost'
    #     username = 'postgres'
    #     password = 'admin' # your password
    #     database = 'postgres'
    #     self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    #     self.cur = self.connection.cursor()

    # def close_spider(self, spider):
    #     self.cur.close()
    #     self.connection.close()

    # def process_item(self, item, spider):
    #     self.cur.execute("insert into apple_news(title,content) values(%s,%s)",(item['title'],item['content']))
    #     self.connection.commit()
    #     return item


from scrapy.exceptions import DropItem
# !搞了半天，原來這只是單次爬取的去重
class DuplicatesPipeline():
    def __init__(self):
        self.article = set()
    
    def process_item(self, item, spider):
        title = item['title'] 
        if title in self.article:
            raise DropItem('duplicates title found %s', item)
        self.article.add(title)
        return item
