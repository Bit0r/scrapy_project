# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface

import mysql.connector
from env import mysql_info
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class MysqlPipeline:
    user = mysql_info['user']
    password = mysql_info['password']
    autocommit = True

    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(user=self.user,
                                           password=self.password,
                                           database=self.database,
                                           autocommit=self.autocommit)
        self.cursor = self.cnx.cursor(prepared=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        try:
            self.cursor.execute(
                self.query,
                tuple(adapter[field_name] for field_name in self.field_names))
        except mysql.connector.Error as err:
            raise DropItem(str(err))

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()


class GamePipeline(MysqlPipeline):
    database = 'game'
    query = '''
    REPLACE INTO downlink (id, download, gift, cdk)
    VALUES (?, ?, ?, ?)
    '''
    field_names = ('id', 'download', 'gift', 'cdk')
