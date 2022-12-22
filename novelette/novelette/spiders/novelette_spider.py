import scrapy
from mySpider.items import MyspiderItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request


class NoveletteSpiderSpider(scrapy.Spider):
    name = 'novelette_spider'
    allowed_domains = ['www.9kmy.com']
    start_urls = ['http://www.9kmy.com/shu/108946/']

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('#ul_all_chapters > li')
        for chapter_id, li in enumerate(li_list):
            item = MyspiderItem()
            item['chapter_id'] = chapter_id
            item['title'] = li.css('a::text').extract_first()
            item['text'] = ''
            href = li.css('a::attr(href)').extract_first()
            yield Request(href, callback=self.parse_text, cb_kwargs={'item': item})

    def parse_text(self, response: HtmlResponse, **kwargs):
        item = kwargs['item']
        sel = Selector(response)
        for p in sel.css('#article > p::text'):
            item['text'] += p.extract().replace('\r', '\n')
        next_page = sel.css('#next_url')
        if '下一页' in next_page[0].css('::text').extract_first():
            yield Request(response.urljoin(next_page[0].css('::attr(href)').extract_first()),
                          callback=self.parse_text,
                          cb_kwargs={'item': item})
        else:
            print(item['chapter_id'], item['title'])
            yield item
