import datetime
import os
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from spider.items import SpiderItem
import re
from gne import GeneralNewsExtractor


class A163Spider(RedisCrawlSpider):
    name = "163"

    redis_key = '163:urls'

    rules = (Rule(LinkExtractor(allow=r"/article/"), callback="parse_item", follow=True),)

    custom_settings = {
        'DOWNLOAD_DELAY' : 2,
        'ITEM_PIPELINES' : {
            'scrapy_redis.pipelines.RedisPipeline': 400,
        }
    }

    def parse_item(self, response):
        item = SpiderItem()
        item['id'] = os.path.basename(__file__).split(".")[0]+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        item['title'] = response.xpath("//h1/text()").extract_first()
        item['url'] = response.url
        
        date = response.xpath("//div[@class='post_info']/text()").extract_first()
        if date != None:
            item['date'] = item['date'] = re.search('\d+-\d+-\d+ \d+:\d+:\d+',date).group()
        else:
            extractor = GeneralNewsExtractor()
            result = extractor.extract(response.text)
            item['date'] = result['publish_time']
        item['content'] = "".join(response.xpath("//div[@class='post_body']//p/text()").extract())
        time.sleep(1)
        yield item
