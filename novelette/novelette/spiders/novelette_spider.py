import scrapy

from ..items import NoveletteItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request


class NoveletteSpiderSpider(scrapy.Spider):
    name = 'novelette_spider'
    allowed_domains = ['www.xcbiquge.org']

    def start_requests(self):
        for i in range(1):
            # print(f'page: {i + 1}')
            yield Request(url=f'http://www.xcbiquge.org/72_72601', callback=self.parse,
                          cb_kwargs={'page': i})

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('body > div.container.border3-2.mt8.mb20 > div.info-chapters.flex.flex-wrap > a')
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
        for p in sel.css('#article > p::text'):
            text = p.extract().replace('\n', '').replace('\r', '').replace(' ', ' ')
            if not text:
                continue
            item['text'] += text + '\n'
        next_page = sel.css('#next_url')
        if '下一页' in next_page.extract_first():
            yield Request(response.urljoin(next_page[0].css('::attr(href)').extract_first()),
                          callback=self.parse_text,
                          cb_kwargs={'item': item})
        print(item['chapter_id'], item['title'])
        yield item
