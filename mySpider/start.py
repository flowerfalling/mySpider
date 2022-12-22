# -*- coding: utf-8 -*-
# @Time    : 2022/11/22 20:38
# @Author  : 之落花--falling_flowers
# @File    : start.py
# @Software: PyCharm
from scrapy import cmdline


def main():
    cmdline.execute('scrapy crawl demo'.split())
    pass


if __name__ == '__main__':
    main()
