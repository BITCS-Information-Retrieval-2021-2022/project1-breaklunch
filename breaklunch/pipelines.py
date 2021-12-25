# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import pymongo


class BreaklunchPipeline:
    collection = ['springer_paper']

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
        self.db[self.collection[0]].create_index('doi', unique=True)
        spider.logger.debug('连接MongoDB数据库:' + self.mongo_db)

    # 爬虫停止 关闭数据库
    def close_spider(self, spider):
        self.client.close()
        spider.logger.debug('关闭MongoDB数据库:' + self.mongo_db)

    def process_item(self, item, spider):
        # 视频基本信息

        print("________________________________________________")
        print(item)
        if 'doi' in item:
            try:
                self.db[self.collection[0]].insert_one(item)
                print("插入成功")
                return item
            except Exception:
                spider.logger.debug('item出现重复,尝试更新')
                try:
                    self.db[self.collection[0]].update(
                        {'doi': item['doi']},
                        {"$set": {'abstract': item['abstract']}}
                        )
                    print("更新成功")
                    return item
                except Exception:
                    spider.logger.debug('item出现重复,尝试更新失败')
                    return item
                return item
        # 视频本地路径
        elif 'video_path' in item:  # 注意 在acl中的视频路径是Video_path
            print("vp:" + item['video_path'])
            self.db[self.collection[0]].update(
                {'foreign_id': item['target_id']},
                {'$set': {'video_path': item['video_path']}}
                )
        # pdf本地路径
        elif 'pdf_path' in item:  # 注意 在acl中的视频路径是Video_path
            self.db[self.collection[0]].update(
                {'foreign_id': item['target_id']},
                {'$set': {'pdf_path': item['pdf_path']}}
                )
        # pdf url
        elif 'pdf_url' in item:  #
            print("nannana")
            self.db[self.collection[0]].update(
                {'foreign_id': item['target_id']},
                {'$set': {'pdf_url': item['pdf_url']}}
                )  # pdf url
        elif 'authors' in item:  #
            print("!!!!!!!!!!!!!!!")
            print(item['authors'])
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
                        self.db[self.collection[3]].update_one(
                            {'Anthology ID': item['Anthology ID']},
                            {'$set': {k: v}}
                            )
                    else:  # 除了PDF, 其他附件可能一类多个
                        self.db[self.collection[3]].update_one(
                            {'Anthology ID': item['Anthology ID']},
                            {'$addToSet': {k: v}}
                            )
        else:
            print()
        return item
