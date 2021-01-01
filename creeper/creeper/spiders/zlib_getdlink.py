from scrapy.http import headers
from creeper.items import dlinkItem
import scrapy


class ZlibGetdlinkSpider(scrapy.Spider):
    name = 'zlib_getdlink'
    allowed_domains = ['zh.1lib.us']
    custom_settings ={
        'ITEM_PIPELINES':{'creeper.pipelines.Getdlink_Pipeline':350}
    }
    
    def start_requests(self):
        HEADERS = {
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            #"Referer": "https://zh.1lib.us/s/python?page=1",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        }
        url = getattr(self, 'link', None)
        yield scrapy.Request(url=url, headers=HEADERS, callback=self.parse)

    def parse(self, response):
        item = dlinkItem({
            "dlink": "https://zh.1lib.us" + response.css("a.dlButton::attr(href)").get(),
            "file_type": response.css("a.dlButton::text").getall()[1].split("(")[1].split(',')[0]
        })
        yield item
        