# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class BreaklunchPipeline:
    collection = ['crossmind', 'crossmind_comment', 'crossmind_reaction', 'acl_anthology']

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 从settings文件读取数据库URI和DB
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB')
        )

    # 爬虫开启 连接数据库
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # 创建索引 防止插入重复数据
        self.db[self.collection[0]].create_index('foreign_id', unique=True)
        self.db[self.collection[3]].create_index('Anthology ID', unique=True)
        spider.logger.debug('连接MongoDB数据库:' + self.mongo_db)


    # 爬虫停止 关闭数据库
    def close_spider(self, spider):
        self.client.close()
        spider.logger.debug('关闭MongoDB数据库:' + self.mongo_db)

    def process_item(self, item, spider):
        # 视频基本信息
        print("item is: "+item)
        if 'foreign_id' in item:
            try:
                self.db[self.collection[0]].insert_one(item)
                return item
            except Exception:
                spider.logger.debug('视频基本信息出现重复')
                return item
        # 视频本地路径
        elif 'video_path' in item:  # 注意 在acl中的视频路径是Video_path
            self.db[self.collection[0]].update({'foreign_id': item['target_id']},
                                               {'$set': {'video_path': item['video_path']}})
        # pdf本地路径
        elif 'pdf_path' in item:  # 注意 在acl中的视频路径是Video_path
            self.db[self.collection[0]].update({'foreign_id': item['target_id']},
                                               {'$set': {'pdf_path': item['pdf_path']}})
        # 评论信息
        elif 'content' in item:
            try:
                self.db[self.collection[1]].insert_one(item)
                return item
            except Exception:
                spider.logger.debug('评论出现重复')
                return item
        # reaction信息
        elif 'reaction' in item:
            try:
                self.db[self.collection[2]].insert_one(item)
                return item
            except Exception:
                spider.logger.debug('reaction出现重复')
                return item
        # acl
        elif 'Anthology ID' in item and 'mark_acl_path' not in item:
            try:
                self.db[self.collection[3]].insert_one(item)
                return item
            except Exception:
                spider.logger.debug('acl出现重复')
                return item
        elif 'mark_acl_path' in item:
            del item['mark_acl_path']
            for k, v in item.items():
                if k != 'Anthology ID':
                    if k == 'PDF_path':
                        self.db[self.collection[3]].update_one({'Anthology ID': item['Anthology ID']}, {'$set': {k: v}})
                    else:  # 除了PDF, 其他附件可能一类多个
                        self.db[self.collection[3]].update_one({'Anthology ID': item['Anthology ID']},
                                                               {'$addToSet': {k: v}})
        return item
