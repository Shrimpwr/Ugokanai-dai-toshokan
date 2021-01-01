from creeper.items import zlibItem
import scrapy

class ZlibSpider(scrapy.Spider):
    name = "zlib_search"
    custom_settings ={
        'ITEM_PIPELINES':{'creeper.pipelines.Search_Pipeline':300}
    }

    def start_requests(self):
        url = "https://zh.1lib.org/s/"
        kword = getattr(self, 'keyword', None)
        page = getattr(self, 'page', None)
        flag = False
        for ch in kword:
            if u'\u4e00' <= ch <= u'\u9fff':
                flag = True   
        if flag:
            url = url + "?q=" + kword + "&page=" + page
        else:
            url = url + kword + "?page=" + page
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for book in response.css('div.resItemBoxBooks'):
            item = zlibItem({
                'title': book.css("h3 a::text").get(),
                'link' : "https://zh.1lib.org" + book.css("h3 a::attr(href)").get(),
                'coverlink_s': ('https://zh.1lib.org/img/book-no-cover.png' if (book.css("div.itemCoverWrapper img::attr(src)").get() == 'img/book-no-cover.png' or book.css("div.itemCoverWrapper img::attr(data-src)").get() == '/img/cover-not-exists.png') else  book.css("div.itemCoverWrapper img::attr(data-src)").get()),
                'coverlink_l': ('https://zh.1lib.org/img/book-no-cover.png' if (book.css("div.itemCoverWrapper img::attr(src)").get() == 'img/book-no-cover.png' or book.css("div.itemCoverWrapper img::attr(data-src)").get() == '/img/cover-not-exists.png') else ("https://covers.zlibcdn2.com/covers200/books" + book.css("div.itemCoverWrapper img::attr(data-src)").get()[43:])),
                'authors': book.css("div.authors a::text").getall(),
            })
            yield item


