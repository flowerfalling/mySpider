import scrapy
from mySpider.items import MyspiderItem
from scrapy.http import HtmlResponse
from scrapy import Selector
from scrapy import Request


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/top250']

    def start_requests(self):
        for page in range(10):
            yield Request(url=f'http://movie.douban.com/top250?start={page * 25}&filter=')

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        li_list = sel.css('#content > div > div.article > ol > li')
        for li in li_list:
            movie_item = MyspiderItem()
            movie_item['title'] = li.css('span.title::text').extract_first()
            movie_item['rank'] = li.css('span.rating_num::text').extract_first()
            movie_item['subject'] = li.css('span.inq::text').extract_first()
            yield movie_item
        href_list = sel.css('div.paginator > a::attr(href)')
        for href in href_list:
            url = response.urljoin(href.extract())
            yield Request(url=url)
