# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BokescrapingItem(scrapy.Item):
	text = scrapy.Field()
	image_url = scrapy.Field()
	# image = scrapy.Field()   
	# pass

