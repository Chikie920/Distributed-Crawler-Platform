import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from spider.items import SpiderItem


class BaiduSpider(CrawlSpider):
    name = "baidu"
    # allowed_domains = ["news.baidu.com"]
    start_urls = ["https://news.baidu.com/"]

    rules = (
             Rule(LinkExtractor(allow=r"mbd.baidu.com"), callback="parse_item", follow=True),
             Rule(LinkExtractor(allow=r"baijiahao.baidu.com"), callback="parse_item", follow=True),
             )
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 3,
        'DOWNLOADER_MIDDLEWARES' : {
            "spider.middlewares.SpiderDownloaderMiddleware": 300,
        },
        'LOG_LEVEL' : 'WARNING'
    }

    cookie_str = 'BIDUPSID=752797DB3967220CBCA1926824252DF7; PSTM=1708769763; H_PS_PSSID=40125_40170_40202_39661_40206_40212_40216_40224_40265_40278_40295_40291_40289_40284; ZFY=TY3tSySVApxDf1ON7jDcwiqFfNjH8pQuhUfBMu9X8IQ:C; BAIDUID_BFESS=752797DB3967220CBCA1926824252DF7:FG=1; BDUSS=ExWd0FqYzA5c2xrWXNHVjFSRDhIZ21zRnhVZ2JxczdMTGVnYnRpSlM4aEdTUUptRVFBQUFBJCQAAAAAAAAAAAEAAADBrfqBam9obrDrt93QptHVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEa82mVGvNplO; BDUSS_BFESS=ExWd0FqYzA5c2xrWXNHVjFSRDhIZ21zRnhVZ2JxczdMTGVnYnRpSlM4aEdTUUptRVFBQUFBJCQAAAAAAAAAAAEAAADBrfqBam9obrDrt93QptHVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEa82mVGvNplO; LOCALGX=%u6B66%u6C49%7C%34%38%31%32%7C%u6B66%u6C49%7C%34%38%31%32; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaStatus=false; BAIDU_WISE_UID=wapp_1709465600596_602; arialoadData=false; Hm_lvt_e9e114d958ea263de46e080563e254c4=1708832449,1708918752,1709465415,1709525603; BAIDU_SSP_lcr=https://cn.bing.com/; RT="z=1&dm=baidu.com&si=00a80eb7-35e1-4452-9d4f-11ddafd0d5e1&ss=ltcfggxk&sl=5&tt=2fz&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=49fs&nu=2gks0cx0&cl=4ask"; ab_sr=1.0.1_ODU2YzUwZTk2NGFmOTQyNzJkZDE2YzY3MWQ4ZjdhYWIyYjg2MDNiMWJlNzMwYjA1NTIyOGMxMjlhN2YwOWYwZmZjNmZiOGVjZTQ2Mjk4ZjIyNzNiNjg1YTk3NmFjY2FjMjdiZGNkNzMxY2E1YjQzZGEwZWEyNDY4M2UwNDFmNjg4NTk0NTdmNWMxNWYxODJhYzJjYTU1OTIzMjYzYjMwMA==; Hm_lpvt_e9e114d958ea263de46e080563e254c4=1709526713'

    # def start_requests(self):
    #     cookie_list = self.cookie_str.split("; ")
    #     self.cookie = {}
    #     for item in cookie_list:
    #         key = item.split("=")[0]
    #         value = item.split("=")[1]
    #         self.cookie[key] = value
    #     yield scrapy.Request(url="https://news.baidu.com/", cookies=self.cookie)

    def parse_item(self, response):
        item = SpiderItem()
        item['title'] = response.xpath("//div[@class='sKHSJ']/text()").extract_first()
        item['url'] = response.url
        date = response.xpath("//span[@data-testid='updatetime']/text()").extract_first()
        if len(date) != 0:
            item['date'] = date.replace(" ", "")
        item['content'] = "".join(response.xpath("//div[@data-testid='article']//text()").extract())
        print(item)
        yield item
