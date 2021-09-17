# -*- coding: UTF-8 -*-

from scrapy import cmdline

cmdline.execute('scrapy crawl cve -a keyword=java -a year=2020'.split())
# cmdline.execute('scrapy crawl github'.split())
