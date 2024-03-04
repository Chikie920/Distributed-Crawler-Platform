import json
import scrapy

from spider.items import SpiderItem


class PengpaiSpider(scrapy.Spider):
    name = "pengpai"
    allowed_domains = ["www.thepaper.cn"]
    # start_urls = ["https://www.thepaper.cn"]

    custom_settings = {
        'DOWNLOAD_DELAY' : 2
    }

    def start_requests(self):
        data = {"channelId":"","excludeContIds":[26548629,26548438,26548304,26548499,26548371,26548370,26548188,26547870,26546713,26548505,26548185,26547783,26547846,26548486,26547393,26547456,26547138,26547842,26547789,26545935,26545930,26546806,26545649,26546800,26545267,26546802,26547133,26547132,26547134,26548345,26547131,26548389,26546854,26548387,26548322,26547053,26546799,26548399,26546920],"listRecommendIds":[26547842,26546854,26547846,26546713],"pageSize":20,"startTime":1709541511586,"pageNum":1}
        for i in range(1, 2):
            data['pageNum'] = i
            yield scrapy.FormRequest(url="https://api.thepaper.cn/contentapi/nodeCont/getByChannelId", formdata=data, callback=self.parse_url)

    def parse_url(self, response):
        response_json_data_dict = json.loads(response.text)['data']['list']
        for data in response_json_data_dict:
            yield scrapy.Request(url='www.thepaper.cn/newsDetail_forward_'+data['contId'], callback=self.parse_content)


    def parse_content(self, response):
        item = SpiderItem()
        item['title'] = response.xpath("//h1/text()").extract()
        item['url'] = response.url
        item['date'] = response.xpath("//div[@class='ant-space-item']/span/text()").extract_first().replace(" ","")
        content = "\n".join(response.xpath("//div[@class='index_cententWrap__Jv8jK']//p/text()").extract())
        item['content'] = content
        yield item
