import datetime
import os
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from gne import GeneralNewsExtractor
from spider.items import SpiderItem


class SohuSpider(RedisCrawlSpider):
    name = "sohu"

    redis_key = 'sohu:urls'

    rules = (Rule(LinkExtractor(allow=r"www.sohu.com/a/"), callback="parse_item", follow=True),)

    custom_settings = {
        'DOWNLOAD_DELAY' : 3,
        'DOWNLOADER_MIDDLEWARES' : {
            "spider.middlewares.SpiderDownloaderMiddleware": 300,
        },
        'LOG_LEVEL' : 'WARNING',
        'ITEM_PIPELINES' : {
            'scrapy_redis.pipelines.RedisPipeline': 400,
        }
    }

    def parse_item(self, response):
        item = SpiderItem()
        item['id'] = os.path.basename(__file__).split(".")[0]+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        item['title'] = response.xpath("//h1/text()").extract_first().strip()
        item['url'] = response.url
        date = response.xpath("//span[@class='time']/text()").extract_first().strip()
        if date != None:
            item['date'] = date.strip()
        else:
            extractor = GeneralNewsExtractor()
            result = extractor.extract(response.text)
            item['date'] = result['publish_time']
        item['content'] = "".join(response.xpath("//article[@class='article']//p/text()").extract())
        # print(item)
        time.sleep(3)
        yield item
        

