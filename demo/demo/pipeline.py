from scrapy.exceptions import DropItem
import pymongo

class MongoDBPipeline(object):

    collection_name = 'lu'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri =mongo_uri
        self.mongo_db =mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item



class DuplicatesPipeline(object):
    collection_name = 'lu'
    
    def __init__(self,mongo_uri, mongo_db):
        self.mongo_uri =mongo_uri
        self.mongo_db =mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def close_spider(self, spider):
        self.client.close()
#  查看是否有重复
    def process_item(self, item, spider):
        exsit =  self.db[self.collection_name].find_one(dict({'url':item['url']}))
        if exsit is not None:
            # return exsit
            raise DropItem("Duplicate item found: %s" % item)
        else:
            # self.ids_seen.add(item['id'])
            return item