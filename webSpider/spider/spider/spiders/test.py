from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from gne import GeneralNewsExtractor
from spider.items import SpiderItem
import datetime
import os
import time


class TestSpider(RedisCrawlSpider):
    name = "test"

    redis_key = 'test:urls'

    custom_settings = {
        'DOWNLOAD_DELAY' : 2,
        'ITEM_PIPELINES' : {
            'scrapy_redis.pipelines.RedisPipeline': 400,
        },
        'CONCURRENT_REQUESTS' : 100 # 并发请求参数
    }

    rules = (
        Rule(LinkExtractor(allow=r""), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        item['id'] = os.path.basename(__file__).split(".")[0]+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        extractor = GeneralNewsExtractor()
        result = extractor.extract(response.text)
        item = SpiderItem()
        item['title'] = result['title']
        item['url'] = response.url
        date = result['publish_time']
        if len(date) != 0:
            item['date'] = date.strip()
        else:
            item['date'] = "采集失败"
        item['content'] = result['content']
        time.sleep(1)
        return item

    def __init__(self, *args, **kwargs):
        if 'DOWNLOADER_MIDDLEWARES' in kwargs:
            middleWare = kwargs['DOWNLOADER_MIDDLEWARES']
            kwargs.popitem()
            print(middleWare)
            self.custom_settings['DOWNLOADER_MIDDLEWARES'] = middleWare
        if 'rules' in kwargs:
            rules = kwargs['rules']
            kwargs.popitem()
            print(rules)
            rule_list = rules.split(',')
            for item in rule_list:
                self.rules+=(Rule(LinkExtractor(allow=r"%s" % item), callback="parse_item", follow=True),)
        if 'CONCURRENT_REQUESTS' in kwargs:
            self.custom_settings['CONCURRENT_REQUESTS'] = kwargs['CONCURRENT_REQUESTS']
            kwargs.popitem()
            print(self.custom_settings['CONCURRENT_REQUESTS'])
        if 'DOWNLOAD_DELAY' in kwargs:
            self.custom_settings['DOWNLOAD_DELAY'] = kwargs['DOWNLOAD_DELAY']
            kwargs.popitem()
            print(self.custom_settings['DOWNLOAD_DELAY'])
        
        super(TestSpider, self).__init__(*args, **kwargs)
            

