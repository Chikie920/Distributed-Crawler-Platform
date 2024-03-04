import json
from scrapy import Request
from scrapy.spiders import Spider
from spider.items import SpiderItem


class SinaSpider(Spider):
    name = "sina"
    # allowed_domains = ["news.sina.com.cn", "finance.sina.com.cn"]
    # start_urls = ["https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1"]
    # lid参数
    # 国内 2510
    # 国际 2511
    # 社会 2669
    # 体育 2512
    # 娱乐 2513
    # 军事 2514
    # 科技 2515
    # 财经 2516
    # 股市 2517
    # 美股 2518
    lid_list = [2510, 2511, 2669, 2512, 2513, 2514, 2515, 2516, 2517, 2518];

    def start_requests(self):
        
        for lid in self.lid_list:
            for i in range(1, 2):
                yield Request(url=f"https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={lid}&k=&num=50&page={i}", callback=self.parse_url)
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 2,
        "ITEM_PIPELINES" : {
            "spider.pipelines.SinaSpiderPipeline": 300,
        }
    }

    

    def parse_url(self, response):
        response_json_data_dict = json.loads(response.text)['result']['data']
        for data in response_json_data_dict:
            yield Request(url=data['url'], callback=self.parse_content)

    def parse_content(self, response):
        item = SpiderItem()
        item['title'] = response.xpath("//h1/text()").extract()
        item['url'] = response.url
        item['date'] = response.xpath("//span[@class='date']//text()").extract_first().replace(" ","")
        content = "\n".join(response.xpath("//div[@class='article-content-left']//div[@class='article']//p//text()").extract())
        item['content'] = content
        yield item
