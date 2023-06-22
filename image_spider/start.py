# -*- coding: utf-8 -*-
# @Time    : 2023/6/22 15:29
# @Author  : 之落花--falling_flowers
# @File    : start.py
# @Software: PyCharm
from scrapy import cmdline


def main():
    cmdline.execute('scrapy crawl comics_spider'.split())
    pass


if __name__ == '__main__':
    main()
