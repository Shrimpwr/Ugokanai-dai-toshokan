# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class zlibItem(scrapy.Item):
   title = scrapy.Field()
   id = scrapy.Field()
   link  = scrapy.Field()
   property_value = scrapy.Field()
   coverlink_s = scrapy.Field()
   coverlink_l = scrapy.Field()
   authors = scrapy.Field()

class dlinkItem(scrapy.Item):
   dlink = scrapy.Field()
   file_type = scrapy.Field()

class coverItem(scrapy.Item):
   image_urls = scrapy.Field()
   images = scrapy.Field()