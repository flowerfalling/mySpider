import os.path

import scrapy

from scrapy import Request
from scrapy import Selector
from ..items import ImageItem


class ComicsSpider(scrapy.Spider):
    name = 'comics_spider'
    allowed_domains = ['e-hentai.org', 'fjpmguw.mpfqzstuapfb.hath.network']

    # start_urls = ['http://e-hentai.org/']

    def start_requests(self):
        for i in range(13):
            print(f'page: {i + 1}')
            yield Request(url=f'https://e-hentai.org/g/2384366/dd537a2bff/?p={i}', callback=self.parse, cb_kwargs={'page': i})

    def parse(self, response, **kwargs):
        resp = Selector(response)
        index_list = resp.css('#gdt > div > div > a')
        for image_id, li in enumerate(index_list):
            if os.path.exists(fr".\images\{217 + image_id + 40 * kwargs['page']}.jpg"):
                continue
            item = ImageItem()
            item['id'] = 217 + image_id + 40 * kwargs['page']
            href = li.css('::attr(href)').extract_first()
            yield Request(
                response.urljoin(href),
                callback=self.parse_image_url,
                cb_kwargs={'item': item},
            )

    def parse_image_url(self, response, **kwargs):
        resp = Selector(response)
        item = kwargs['item']
        item['image_urls'] = resp.css('#img').attrib['src']
        yield item