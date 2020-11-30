import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from BokeScraping.items import BokescrapingItem


class BoketeSpider(scrapy.Spider):
    name = 'bokete'
    allowed_domains = ['bokete.jp']
    start_urls = ['https://bokete.jp/']

    def parse(self, response):
        """
        レスポンスに対するパース処理
        """
        # item = BokescrapingItem()
        for post in response.css('.content-boke .boke'):
            
            yield BokescrapingItem(
                text = post.css('a.boke-text  div::text').extract_first().strip(),
                image_url = 'http:' + post.css('div.boke-photo  .photo-content  a  img::attr(src)').extract_first().strip()
            )

      