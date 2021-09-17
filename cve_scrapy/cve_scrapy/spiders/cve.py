# -*- coding: UTF-8 -*-
import scrapy
from ..items import CveScrapyItem
import re

class CveSpider(scrapy.Spider):
    name = 'cve'
    allowed_domains = ['cve.mitre.org']

    def __init__(self, keyword='java', year='2021'):
        self.keyword = keyword
        self.year = year
        super(CveSpider, self).__init__()
        self.start_urls = ['https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=%s' % self.keyword]

    def parse(self, response):
        #print(response.request.headers)
        self.items = CveScrapyItem()
        name_lists = response.selector.xpath('//td[@nowrap="nowrap"]/a')
        for l in name_lists:
            self.items['cve_name'] = l.xpath('text()').get()
            self.items['cve_uri'] = l.xpath('@href').get()

            # 过滤年份
            pattern = re.compile('CVE-(\d{4})-\d+')
            parse_year = re.findall(pattern, self.items['cve_name'])[0]
            if self.year == parse_year:
                yield scrapy.Request(url='https://cve.mitre.org' + self.items['cve_uri'], callback=self.parse_cve_details)
            else:
                yield

    def parse_cve_details(self, response):
        description = response.selector.xpath('//table//tr[4]//td[1]/text()').get()
        # 排除js干扰，其他语言可补充自定
        if self.keyword == 'java' and 'javascript' in description.lower():
            return
        refs = response.selector.xpath('//table//tr[7]//td[1]//a[@href]/text()').extract()
        for ref in refs:
            pattern = re.compile('http[s]?://github\.com/.+/commit/.+')
            url = re.findall(pattern, ref)
            if url != []:
                url = url[0]
                yield scrapy.Request(url=url, callback=self.parse_github_commit)

    def parse_github_commit(self, response):
        files = response.selector.xpath('//table//tr[4]//td[1]/text()').get()
        added_data = '//tr[@data-hunk="47a22db29e547845bee9ebb17cf335019ea19a51852d193afeb632e1b8e7499e"]//span[@data-code-marker='+']'
