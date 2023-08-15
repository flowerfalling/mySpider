import scrapy

from ..items import NoveletteItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request


class NoveletteSpiderSpider(scrapy.Spider):
    name = 'novelette_spider'
    allowed_domains = ['www.sdjnjobs.com']

    def start_requests(self):
        for i in range(4):
            # print(f'page: {i + 1}')
            yield Request(url=f'https://www.sdjnjobs.com/wapbook/k/164456/{i + 1}', callback=self.parse, cb_kwargs={'page': i})

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('body > div.container > div.row.row-section > div > div:nth-child(4) > ul > li > a')
        for chapter_id, li in enumerate(li_list):
            item = NoveletteItem()
            item['chapter_id'] = chapter_id + 40 * kwargs['page']
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
        text = sel.css('#content > p::text')
        # for p in sel.css('body > div.container > section.RBGsectionThree > script')[1:]:
        for p in text:
            item['text'] += p.extract().replace('\r', '') + '\n'
        next_page = sel.css('#container > div > div > div.reader-main > div:nth-child(1) > a:nth-child(5)')
        if '下一页' in next_page.extract_first():
            yield Request(response.urljoin(next_page[0].css('::attr(href)').extract_first()),
                          callback=self.parse_text,
                          cb_kwargs={'item': item})
        print(item['chapter_id'], item['title'])
        yield item
