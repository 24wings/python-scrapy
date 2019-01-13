import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = '111lu'
    allowed_domains = ['www.zbj.com']
    start_urls = ['https://www.zbj.com/']
    def parse_start_url(self,response):
        return {
            'url':response.url,
            'title':response.css('title::text').extract_first(),
            'html':response.css('html').extract_first()
        }

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('doc.airuanjian.vip', )),follow=True, callback='parse_item'),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow=('*', )), callback='parse_item'),
        Rule(LinkExtractor(allow=('.',)),follow=True , callback='parse_item'),
        # Rule(LinkExtractor(allow=('.html$',)), callback='parse_item'),
   
    )

    def parse_item(self, response):
        # print(response.url)
        # self.logger.info('Hi, this is an item page! %s', response.url)
        # item = scrapy.Item()
        # item['name'] = response.xpath('//html/text()').extract()
        yield {
            'url':response.url,
            'title':response.css('title::text').extract_first(),
            'html':response.css('html').extract_first()
        }
        # item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        # item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
      