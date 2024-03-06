from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from spider.items import SpiderItem


class SohuSpider(RedisCrawlSpider):
    name = "sohu"
    # allowed_domains = ["news.sohu.com"]
    # start_urls = ["https://news.sohu.com"]

    redis_key = 'sohu:urls'

    rules = (Rule(LinkExtractor(allow=r"www.sohu.com/a/"), callback="parse_item", follow=True),)

    custom_settings = {
        'DOWNLOAD_DELAY' : 10,
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
        item['title'] = response.xpath("//h1/text()").extract_first().trim()
        item['url'] = response.url
        item['date'] = response.xpath("//span[@class='time']/text()").extract_first().replace(" ","")
        item['content'] = "".join(response.xpath("//article[@class='article']//p/text()").extract())
        # print(item)
        yield item
        

