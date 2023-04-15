import scrapy
from ..items import NoveletteItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request


class NoveletteSpiderSpider(scrapy.Spider):
    name = 'novelette_spider'
    allowed_domains = ['www.sbooktxt.com']

    def start_requests(self):
        yield Request(url='https://www.sbooktxt.com/60_60380/')

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('#list > dl > dd > a')
        for chapter_id, li in enumerate(li_list):
            item = NoveletteItem()
            item['chapter_id'] = chapter_id
            item['title'] = li.css('::text').extract_first()
            item['text'] = ''
            href = li.css('::attr(href)').extract_first()
            print(item['chapter_id'], item['title'])
            yield Request(response.urljoin(href), callback=self.parse_text, cb_kwargs={'item': item})

    def parse_text(self, response: HtmlResponse, **kwargs):
        item = kwargs['item']
        sel = Selector(response)
        for p in sel.css('#content::text'):
            item['text'] += p.extract().replace('\r', '\n') + '\n'
        # next_page = sel.css('#next_url')
        # if '下一页' in next_page[0].css('#next_url').extract_first():
        #     item['text'] = item['text'][:-1]
        #     yield Request(response.urljoin(next_page[0].css('::attr(href)').extract_first()),
        #                   callback=self.parse_text,
        #                   cb_kwargs={'item': item})
        print(item['chapter_id'], item['title'])
        yield item
