import scrapy

from ..items import NoveletteItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request


class NoveletteSpiderSpider(scrapy.Spider):
    name = 'novelette_spider'
    allowed_domains = ['www.51xs.cc']

    def start_requests(self):
        for i in range(1):
            # print(f'page: {i + 1}')
            yield Request(url=f'https://www.51xs.cc/10_38631/', callback=self.parse,
                          cb_kwargs={'page': i})

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('#list > dl > dd > a')[9:]
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
        for p in sel.css('#content::text'):
            text = p.extract().replace('\n', '').replace('\r', '').replace(' ', ' ')
            if not text:
                continue
            item['text'] += text + '\n'
        # next_page = sel.css('#list > dl > dd:nth-child(12) > a')
        # if '下一页' in next_page.extract_first():
        #     yield Request(response.urljoin(next_page[0].css('::attr(href)').extract_first()),
        #                   callback=self.parse_text,
        #                   cb_kwargs={'item': item})
        print(item['chapter_id'], item['title'])
        yield item
