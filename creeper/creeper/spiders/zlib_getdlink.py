from creeper.items import dlinkItem
import scrapy


class ZlibGetdlinkSpider(scrapy.Spider):
    name = 'zlib_getdlink'
    allowed_domains = ['zh.1lib.us']
    custom_settings ={
        'ITEM_PIPELINES':{'creeper.pipelines.Getdlink_Pipeline':350}
    }
    
    def start_requests(self):
        url = getattr(self, 'link', None)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = dlinkItem({
            "dlink": "https://zh.1lib.us" + response.css("a.dlButton::attr(href)").get(),
            "file_type": response.css("a.dlButton::text").getall()[1].split("(")[1].split(',')[0]
        })
        yield item
        