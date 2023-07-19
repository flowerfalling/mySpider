import scrapy

from ..items import NoveletteItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request

import execjs
from lxml import etree


class NoveletteSpiderSpider(scrapy.Spider):
    name = 'novelette_spider'
    allowed_domains = ['www.newhaitang.com']
    decode = d = execjs.compile('''
function d(a, b) {
    const CryptoJS = require('crypto-js');
    b = CryptoJS.MD5(b).toString();
    var d = CryptoJS.enc.Utf8.parse(b.substring(0, 16));
    var e = CryptoJS.enc.Utf8.parse(b.substring(16));
    return CryptoJS.AES.decrypt(a, e, {
        iv: d,
        padding: CryptoJS.pad.Pkcs7
    }).toString(CryptoJS.enc.Utf8)
}
''')

    def start_requests(self):
        for i in range(1):
            # print(f'page: {i + 1}')
            yield Request(url=f'https://www.newhaitang.com/book/199626613387333/catalog/', callback=self.parse,
                          cb_kwargs={'page': i})

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('body > div.container > section.BCsectionTwo > ol > li > a')
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
        sel = sel.css('body > div.container > section.RBGsectionThree > script')[1]
        text = etree.HTML(self.decode.call('d', sel.re(r'd\("(.*?)", "')[0].replace('\\', ''), sel.re(r'", "(.*?)"\)\)')[0])).xpath('//p/text()')
        # for p in sel.css('body > div.container > section.RBGsectionThree > script')[1:]:
        for p in text:
            # text = p.extract().replace('\n', '').replace('\r', '').replace(' ', ' ')
            # if not text:
            #     continue
            # item['text'] += text + '\n'
            item['text'] += f"    {p}\n"
        # next_page = sel.css('#next_url')
        # if '下一页' in next_page.extract_first():
        #     yield Request(response.urljoin(next_page[0].css('::attr(href)').extract_first()),
        #                   callback=self.parse_text,
        #                   cb_kwargs={'item': item})
        print(item['chapter_id'], item['title'])
        yield item
