from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from spider.items import SpiderItem
import re


class A163Spider(RedisCrawlSpider):
    name = "163"
    # allowed_domains = ["www.163.com"]
    # start_urls = ["https://www.163.com"]

    redis_key = 'wangyi:urls'

    rules = (Rule(LinkExtractor(allow=r"/article/"), callback="parse_item", follow=True),)

    custom_settings = {
        'DOWNLOAD_DELAY' : 2,
        'ITEM_PIPELINES' : {
            'scrapy_redis.pipelines.RedisPipeline': 400,
        }
    }

    def parse_item(self, response):
        item = SpiderItem()
        item['title'] = response.xpath("//h1/text()").extract_first()
        item['url'] = response.url
        item['date'] = re.search('\d+-\d+-\d+ \d+:\d+:\d+',response.xpath("//div[@class='post_info']/text()").extract_first()).group()
        item['content'] = "".join(response.xpath("//div[@class='post_body']//p/text()").extract())
        yield item
