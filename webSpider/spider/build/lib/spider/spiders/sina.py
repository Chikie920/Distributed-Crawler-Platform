import datetime
import json
import os
import time
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from spider.items import SpiderItem


class SinaSpider(RedisSpider):
    name = "sina"
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

    redis_key = 'sina:urls'

    def start_requests(self):
        
        for lid in self.lid_list:
            for i in range(1, 2):
                yield Request(url=f"https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={lid}&k=&num=50&page={i}", callback=self.parse_url)
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 2,
        'ITEM_PIPELINES' : {
            'scrapy_redis.pipelines.RedisPipeline': 400,
        }
    }

    

    def parse_url(self, response):
        response_json_data_dict = json.loads(response.text)['result']['data']
        for data in response_json_data_dict:
            yield Request(url=data['url'], callback=self.parse_content)

    def parse_content(self, response):
        item = SpiderItem()
        item['id'] = os.path.basename(__file__).split(".")[0]+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        item['title'] = response.xpath("//h1/text()").extract_first()
        item['url'] = response.url
        item['date'] = response.xpath("//span[@class='date']//text()").extract_first().strip()
        content = "\n".join(response.xpath("//div[@class='article-content-left']//div[@class='article']/p/text()").extract())
        item['content'] = content
        time.sleep(1)
        yield item
