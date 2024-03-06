import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule

from spider.items import SpiderItem


class IfengSpider(RedisCrawlSpider):
    name = "ifeng"
    # allowed_domains = ["www.ifeng.com"]
    # start_urls = ["https://www.ifeng.com"]

    redis_key = 'ifeng:urls'

    rules = (
                Rule(LinkExtractor(allow=r"news.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"finance.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"tech.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"travel.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"auto.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"sports.ifeng.com"), callback="parse_item", follow=True),
                Rule(LinkExtractor(allow=r"ent.ifeng.com"), callback="parse_item", follow=True),
            )

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
        item['date'] = response.xpath("//div[@class='index_timeBref_20hzr']/a/text()").extract_first().replace(" ","")
        item['content'] = "".join(response.xpath("//div[@class='index_text_D0U1y']//p/text()").extract())
        # print(item)
        yield item
