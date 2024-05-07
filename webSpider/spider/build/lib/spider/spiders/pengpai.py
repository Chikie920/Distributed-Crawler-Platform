import time
import scrapy
from scrapy.http import JsonRequest
import json
from spider.items import SpiderItem
from scrapy_redis.spiders import RedisSpider
import os
import datetime


class PengpaiSpider(RedisSpider):
    name = "pengpai"

    redis_key = 'pengpai:urls'

    custom_settings = {
        'DOWNLOAD_DELAY' : 2,
        'ITEM_PIPELINES' : {
            'scrapy_redis.pipelines.RedisPipeline': 400,
        }
    }

    def start_requests(self):
        data = {"channelId":"","excludeContIds":[26548629,26548438,26548304,26548499,26548371,26548370,26548188,26547870,26546713,26548505,26548185,26547783,26547846,26548486,26547393,26547456,26547138,26547842,26547789,26545935,26545930,26546806,26545649,26546800,26545267,26546802,26547133,26547132,26547134,26548345,26547131,26548389,26546854,26548387,26548322,26547053,26546799,26548399,26546920], "listRecommendIds":[26547842,26546854,26547846,26546713],"pageSize":20,"startTime":1709541511586,"pageNum":1}
        for i in range(1, 2):
            data['pageNum'] = i
            yield JsonRequest(url="https://api.thepaper.cn/contentapi/nodeCont/getByChannelId", data=data, callback=self.parse_url, dont_filter = True)

    def parse_url(self, response):
        response_json_data_dict = json.loads(response.text)['data']['list']
        for data in response_json_data_dict:
            yield scrapy.Request(url='https://www.thepaper.cn/newsDetail_forward_'+data['contId'], callback=self.parse_content)


    def parse_content(self, response):
        item = SpiderItem()
        item['id'] = os.path.basename(__file__).split(".")[0]+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        item['title'] = response.xpath("//h1/text()").extract_first()
        item['url'] = response.url
        item['date'] = response.xpath("//div[@class='ant-space-item']/span/text()").extract_first().strip()
        content = "\n".join(response.xpath("//div[@class='index_cententWrap__Jv8jK']//p/text()").extract())
        item['content'] = content
        time.sleep(1)
        yield item
