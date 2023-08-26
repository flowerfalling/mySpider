import scrapy

from ..items import NoveletteItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request


class NoveletteSpiderSpider(scrapy.Spider):
    name = 'novelette_spider'
    allowed_domains = ['www.82zg.com']

    def start_requests(self):
        for i in range(1):
            # print(f'page: {i + 1}')
            yield Request(url=f'https://www.82zg.com/book/25429/', callback=self.parse, cb_kwargs={'page': i})

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('#list > dl > dd > a')
        for chapter_id, li in enumerate(li_list[12:]):
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
        text = sel.css('#content::text')
        # for p in sel.css('body > div.container > section.RBGsectionThree > script')[1:]:
        for p in text:
            item['text'] += p.extract().replace('\r', '') + '\n'
        # if '下一页' in (next_page := sel.css('#A3')).extract_first():
        #     yield Request(response.urljoin(next_page[0].css('::attr(href)').extract_first()),
        #                   callback=self.parse_text,
        #                   cb_kwargs={'item': item})
        # else:
        #     item['text'] += text[-2].extract().replace('\r', '') + '\n'
        print(item['chapter_id'], item['title'])
        yield item
