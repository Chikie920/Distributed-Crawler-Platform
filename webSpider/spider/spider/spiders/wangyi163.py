import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from spider.items import SpiderItem
import re


class A163Spider(CrawlSpider):
    name = "163"
    # allowed_domains = ["www.163.com"]
    start_urls = ["https://www.163.com"]

    rules = (Rule(LinkExtractor(allow=r"/article/"), callback="parse_item", follow=True),)

    custom_settings = {
        'DOWNLOAD_DELAY' : 2
    }

    def parse_item(self, response):
        item = SpiderItem()
        item['title'] = response.xpath("//h1/text()").extract_first()
        item['url'] = response.url
        item['date'] = re.search('\d+-\d+-\d+ \d+:\d+:\d+',response.xpath("//div[@class='post_info']/text()").extract_first()).group()
        item['content'] = "".join(response.xpath("//div[@class='post_body']//p/text()").extract())
        print(item)
        yield item
