# -*- coding: UTF-8 -*-
import scrapy
from ..items import CveScrapyItem
import re

class CveSpider(scrapy.Spider):
    name = 'cve'
    #allowed_domains = ['cve.mitre.org']

    def __init__(self, keyword='java', year='2021'):
        self.keyword = keyword
        self.year = year
        super(CveSpider, self).__init__()
        self.start_urls = ['https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=%s' % self.keyword]

    def parse(self, response):
        #print(response.request.headers)
        name_lists = response.selector.xpath('//td[@nowrap="nowrap"]/a')
        for l in name_lists:
            cve_name = l.xpath('text()').get()
            cve_uri = l.xpath('@href').get()

            # 过滤年份
            pattern = re.compile('CVE-(\d{4})-\d+')
            parse_year = re.findall(pattern, cve_name)[0]
            if self.year == parse_year:
                yield scrapy.Request(url='https://cve.mitre.org' + cve_uri, callback=self.parse_cve_details, meta={'cve_name': cve_name})
            else:
                yield

    # 解析是否存在github的commit
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
                repository = url[:url.index('/commit')]
                yield scrapy.Request(url=url, callback=self.parse_github_commit, meta={'cve_name': response.meta['cve_name'],
                                                                                       'repository': repository})
            else:
                yield

    def parse_github_commit(self, response):
        commit_url = response.url
        commit_id_new = response.selector.xpath("//span[@class='sha user-select-contain']//text()").extract()[0]
        changed_files = response.selector.xpath("//a[@class='Link--primary']//@title").extract()
        for file in changed_files:
            pattern = re.compile('(.+/commit).+')
            url_t = re.findall(pattern, commit_url)[0]
            url_prefix = url_t + 's/'
            url = url_prefix + commit_id_new + '/' + file
            yield scrapy.Request(url=url, callback=self.parse_old_id, meta={'cve_name': response.meta['cve_name'],
                                                                            'file': file,
                                                                            'url_prefix': url_prefix,
                                                                            'commit_id_new': commit_id_new,
                                                                            'repository': response.meta['repository']})

    def parse_old_id(self, response):
        commit_id_new = response.meta['commit_id_new']
        urls_t = response.selector.xpath('//a[@class="text-mono f6 btn btn-outline BtnGroup-item"]//@href').extract()
        # print(urls_t)
        pattern = re.compile('.+/commit/([0-9a-f]+).+')

        '''
        查找new_commit_id在urls中的位置，此位置的后一位就是old_commit_id
        '''
        new_id_index = 0
        for url in urls_t:
            commit_id = re.findall(pattern, url)[0]
            if commit_id == commit_id_new:
                break
            new_id_index += 1
        # print(commit_id_new)
        # print(new_id_index)

        try:
            commit_id_old = re.findall(pattern, urls_t[new_id_index + 1])[0]
            # print(commit_id_old)
        except:
            return

        new_file_url = response.url.replace('github.com', 'raw.githubusercontent.com').replace('commits/', '')
        old_file_url = (response.meta['url_prefix'] + commit_id_old + '/' + response.meta['file']).replace('github.com',
                                                                                                           'raw.githubusercontent.com').replace(
            'commits/', '')

        items = CveScrapyItem()
        items['keyword'] = self.keyword
        items['year'] = self.year
        items['cve_name'] = response.meta['cve_name']
        items['file'] = response.meta['file']
        items['old_file_url'] = old_file_url
        items['new_file_url'] = new_file_url
        items['repository'] = response.meta['repository']
        yield items