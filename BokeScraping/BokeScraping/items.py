# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Odai(scrapy.Item):
    number = scrapy.Field()
    image_url = scrapy.Field()
    bokes = scrapy.Field()
    pass


class Boke(scrapy.Item):
    text = scrapy.Field()
    star = scrapy.Field()
    number = scrapy.Field()
    pass
