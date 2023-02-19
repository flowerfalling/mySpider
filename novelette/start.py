# -*- coding: utf-8 -*-
# @Time    : 2022/12/23 14:47
# @Author  : 之落花--falling_flowers
# @File    : start.py
# @Software: PyCharm
from scrapy import cmdline


def main():
    cmdline.execute('scrapy crawl novelette_spider'.split())
    pass


if __name__ == '__main__':
    main()
