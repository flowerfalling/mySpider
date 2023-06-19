import scrapy

from ..items import NoveletteItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request
import re


class NoveletteSpiderSpider(scrapy.Spider):
    name = 'novelette_spider'
    allowed_domains = ['www.txtnovels.com']

    def start_requests(self):
        for i in range(9):
            print(f'page: {i + 1}')
            yield Request(url=f'https://www.txtnovels.com/42_42199_{i + 1}/', callback=self.parse,
                          cb_kwargs={'page': i})

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('body > div:nth-child(2) > div:nth-child(5) > dl > dd > a')[:20]
        for chapter_id, li in enumerate(li_list):
            item = NoveletteItem()
            item['chapter_id'] = chapter_id + 20 * kwargs['page']
            item['title'] = li.css('::text').extract_first()
            item['text'] = ''
            href = li.css('::attr(href)').extract_first()
            yield Request(
                response.urljoin(href),
                callback=self.parse_text,
                cb_kwargs={'item': item},
            )

    def parse_text(self, response: HtmlResponse, **kwargs):
        item = kwargs['item']
        sel = Selector(response)
        for p in sel.css('#htmlContent::text')[:-1]:
            text = p.extract()
            if '（本章未完，请翻页）' in text:
                break
            if '\t\t\t' in text:
                text = text[8:]
            item['text'] += text.replace('\t', '').replace(' ', ' ')
        next_page = sel.css('#content > p.text-center.pt10 > a:nth-child(3)')
        if '下一页' in next_page.extract_first():
            yield Request(response.urljoin(next_page[0].css('::attr(href)').extract_first()),
                          callback=self.parse_text,
                          cb_kwargs={'item': item})
        print(item['chapter_id'], item['title'])
        yield item
