import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookToscrapeSpider(CrawlSpider):
    name = 'book_toscrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (
        Rule(LinkExtractor(allow=r'catalogue/[\w\-\d]+/index.html'), callback='parse_item', follow=False),  #爬取详情页，不follow
        Rule(LinkExtractor(allow=r'page-\d+.html')), #爬取下一页，默认follow
    )

    def parse_item(self, response):
        title = response.css('div.product_main h1::text').extract_first()
        price = response.css('div.product_main p.price_color::text').extract_first()
        #简单返回
        yield {
            'title':title,
            'price':price,
        }
