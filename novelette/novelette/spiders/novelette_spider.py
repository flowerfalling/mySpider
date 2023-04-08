import scrapy
from ..items import NoveletteItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request


class NoveletteSpiderSpider(scrapy.Spider):
    name = 'novelette_spider'
    allowed_domains = ['www.xylyc.com']

    def start_requests(self):
        yield Request(url='http://www.xylyc.com/directory/222843', cb_kwargs={'page': 0})
        yield Request(url='http://www.xylyc.com/directory/222843/2/', cb_kwargs={'page': 1})

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('#list > dl > a')
        for chapter_id, li in enumerate(li_list):
            item = NoveletteItem()
            item['chapter_id'] = chapter_id + kwargs['page'] * 100
            item['title'] = li.css('dd::text').extract_first()
            item['text'] = ''
            href = li.css('::attr(href)').extract_first()
            print(item['chapter_id'], item['title'])
            yield Request(response.urljoin(href), callback=self.parse_text, cb_kwargs={'item': item})

    def parse_text(self, response: HtmlResponse, **kwargs):
        item = kwargs['item']
        sel = Selector(response)
        for p in sel.css('#booktxt > p::text'):
            item['text'] += p.extract().replace('\r', '\n')
        next_page = sel.css('#next_url')
        if '下一页' in next_page[0].css('#next_url').extract_first():
            item['text'] = item['text'][:-1]
            yield Request(response.urljoin(next_page[0].css('::attr(href)').extract_first()),
                          callback=self.parse_text,
                          cb_kwargs={'item': item})
        print(item['chapter_id'], item['title'])
        yield item
