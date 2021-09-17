# -*- coding: UTF-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CveScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # CVE编号链接
    cve_name = scrapy.Field()
    cve_uri = scrapy.Field()


class CodeScrapyItem(scrapy.Item):
    # commit代码
    code_old = scrapy.Field()
    code_new = scrapy.Field()
