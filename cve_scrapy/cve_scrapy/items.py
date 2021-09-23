# -*- coding: UTF-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import os
import requests


class CveScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # CVE编号链接
    keyword = scrapy.Field()
    year = scrapy.Field()
    cve_name = scrapy.Field()
    file = scrapy.Field()
    old_file_url = scrapy.Field()
    new_file_url = scrapy.Field()
    repository = scrapy.Field()

