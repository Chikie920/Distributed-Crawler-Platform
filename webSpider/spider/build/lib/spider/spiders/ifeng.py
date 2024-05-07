import datetime
import os
import time
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from gne import GeneralNewsExtractor
from spider.items import SpiderItem


class IfengSpider(RedisCrawlSpider):
    name = "ifeng"
    redis_key = 'ifeng:urls'

    rules = (
                Rule(LinkExtractor(allow=r"news.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"finance.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"tech.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"travel.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"auto.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"sports.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"ent.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(deny=r"gentie.ifeng.com")),
                Rule(LinkExtractor(deny=r"ncar.auto.ifeng.com")),
                Rule(LinkExtractor(deny=r"news.ifeng.com/ask")),
            )

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
        date = response.xpath("//div[@class='index_timeBref_20hzr']/a/text()").extract_first()
        if date != None:
            item['date'] = date.strip()
        else:
            extractor = GeneralNewsExtractor()
            result = extractor.extract(response.text)
            item['date'] = result['publish_time']
        item['content'] = "".join(response.xpath("//div[@class='index_text_D0U1y']//p/text()").extract())
        # print(item)
        time.sleep(1)
        yield item
