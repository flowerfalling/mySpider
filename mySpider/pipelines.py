# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql


class MyspiderPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='falling',
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        title = item.get('title', '')
        rank = item.get('rank', 0)
        subject = item.get('subject', '')
        self.cursor.execute('insert into tb_top_movie (title, rating, subject) values (%s, %s, %s)',
                            (title, rank, subject))
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
