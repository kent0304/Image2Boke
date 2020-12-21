import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from BokeScraping.items import Odai, Boke
from bs4 import BeautifulSoup 

class BoketeSpider(scrapy.Spider):
    name = 'bokete'
    allowed_domains = ['bokete.jp/odai']
    start_urls = [f'https://bokete.jp/odai/{odai_id}/?sort=rate' for odai_id in range(5000000, 5634368)]

    def parse(self, response):
        """
        レスポンスに対するパース処理
        """
        if response.status != 200:
            return 
        odai = self.parse_odai(response)
        odai['bokes'] = [boke for boke in self.parse_boke(response)]
        if not odai['bokes']:
            return 
        odai_star = odai['bokes'][0]['star']
        if odai_star >= self.settings['MIN_ODAI_STAR']:
            return odai

        # item = BokescrapingItem()
        # for post in response.css('.content-boke .boke'):
            
        #     yield BokescrapingItem(
        #         text = post.css('a.boke-text  div::text').extract_first().strip(),
        #         image_url = 'http:' + post.css('div.boke-photo  .photo-content  a  img::attr(src)').extract_first().strip()
        #     )

    def parse_odai(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        image_src = find_image_src(soup)
        return Odai(
            number = response.url.split('/')[-2],
            image_url = [image_src]
        )

    def parse_boke(self, response):
        for boke in response.xpath('//div[@id="content"]/div[@class="boke"]'):
            text = boke.xpath('a[@class="boke-text"]/div/text()').get().strip()
            star_str = boke.xpath(
                    './/div[@class="boke-stars"]/a/text()'
                ).getall()[1].strip().replace(',', '')
            star = int(star_str)
            number = boke.xpath(
                    'a[@class="boke-text"]/@href'
                ).get().split('/')[-1]
            return [Boke(text=text, star=star, number=number)]


def find_image_src(soup):
    image_src = 'https:' + soup.find('div', attrs={'class': 'photo-content'}).find('img').get('src')
    return image_src

      