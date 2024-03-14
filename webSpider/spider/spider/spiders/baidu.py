import datetime
import os
import time
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from spider.items import SpiderItem


class BaiduSpider(RedisCrawlSpider):
    name = "baidu"

    redis_key = 'baidu:urls'

    rules = (
             Rule(LinkExtractor(allow=r"mbd.baidu.com"), callback="parse_item", follow=True),
             Rule(LinkExtractor(allow=r"baijiahao.baidu.com"), callback="parse_item", follow=True),
             )
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 3,
        'DOWNLOADER_MIDDLEWARES' : {
            "spider.middlewares.SpiderDownloaderMiddleware": 300,
        },
        'LOG_LEVEL' : 'WARNING',
        'ITEM_PIPELINES' : {
            'scrapy_redis.pipelines.RedisPipeline': 400,
        }
    }

    cookie_str = 'BIDUPSID=752797DB3967220CBCA1926824252DF7; PSTM=1708769763; H_PS_PSSID=40125_40170_40202_39661_40206_40212_40216_40224_40265_40278_40295_40291_40289_40284; ZFY=TY3tSySVApxDf1ON7jDcwiqFfNjH8pQuhUfBMu9X8IQ:C; BAIDUID_BFESS=752797DB3967220CBCA1926824252DF7:FG=1; BDUSS=ExWd0FqYzA5c2xrWXNHVjFSRDhIZ21zRnhVZ2JxczdMTGVnYnRpSlM4aEdTUUptRVFBQUFBJCQAAAAAAAAAAAEAAADBrfqBam9obrDrt93QptHVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEa82mVGvNplO; BDUSS_BFESS=ExWd0FqYzA5c2xrWXNHVjFSRDhIZ21zRnhVZ2JxczdMTGVnYnRpSlM4aEdTUUptRVFBQUFBJCQAAAAAAAAAAAEAAADBrfqBam9obrDrt93QptHVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEa82mVGvNplO; BAIDU_WISE_UID=wapp_1709465600596_602; H_WISE_SIDS=110085_287977_288664_294244_287174_269893_294392_295129_295155_292242_295504_295728_277936_295724_296175_291026_281879_296147_283867_294386_294565_297003_296981_297116_297148_296744_296745_296747_296750_297240_283782_294860_297468_297497_297535_292709_295508_297577_294361_295499_297691_297749_284553_297983_297978_297126_297713_297484_298105_292169_294755_290401_298305_298350_298395_298364_298296_298527_298625_298624_294133_298840_298111_298949_298192_299016_299064_293583_299157_107320_299348; H_WISE_SIDS_BFESS=110085_287977_288664_294244_287174_269893_294392_295129_295155_292242_295504_295728_277936_295724_296175_291026_281879_296147_283867_294386_294565_297003_296981_297116_297148_296744_296745_296747_296750_297240_283782_294860_297468_297497_297535_292709_295508_297577_294361_295499_297691_297749_284553_297983_297978_297126_297713_297484_298105_292169_294755_290401_298305_298350_298395_298364_298296_298527_298625_298624_294133_298840_298111_298949_298192_299016_299064_293583_299157_107320_299348; LOCALGX=%u957F%u6C99%7C%35%31%36%32%7C%u957F%u6C99%7C%35%31%36%32; Hm_lvt_e9e114d958ea263de46e080563e254c4=1708918752,1709465415,1709525603,1710385159; ariaReadtype=1; ariaStatus=false; Hm_lpvt_e9e114d958ea263de46e080563e254c4=1710385204; ab_sr=1.0.1_MjBiNTY2N2UyYTI5MGQ3OGJmNDE4OWZmZjMyMDFlODY5YzhlYjZhYzgxNmEwOGRlOTIwZmI0MDgxMjg5NWVkMTc5OTFiMjRkNzliYzcwYTVjYzE2ZTY3YWVmOGQ2YTdlYTI0MzlmMmJkNzg1M2IwMmNkNmNhMjQzYjJhYjlhNTI3MDJkZTBkOWUwMzVmMmMwZjBmMjc1NWMyMjQ4MjJhZg==; RT="z=1&dm=baidu.com&si=e127e018-f672-4513-88a9-863e3e3a8171&ss=ltqnmso8&sl=1&tt=84b&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=8aa&ul=8pa&hd=8pf"'

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
        item['id'] = os.path.basename(__file__).split(".")[0]+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        item['title'] = response.xpath("//div[@class='sKHSJ']/text()").extract_first()
        item['url'] = response.url
        date = response.xpath("//span[@data-testid='updatetime']/text()").extract_first()
        if len(date) != 0:
            item['date'] = date.strip()
        item['content'] = "".join(response.xpath("//div[@data-testid='article']//text()").extract())
        time.sleep(1)
        yield item
        
