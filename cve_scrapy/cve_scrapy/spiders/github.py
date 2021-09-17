# -*- coding: UTF-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/google/tink/commit/93d839a5865b9d950dffdc9d0bc99b71280a8899#diff-760adc57330a03f3356dcae0935914a527872860419077742e2a2b859929b0d7R481']

    def parse(self, response):

        data_hunk = 'cca68ce10d9191a321823550228e6263a4fc1c1e4b8d579ad0c7fdcfe75ef4a5'

        '''
        +--------+
        |旧代码处理|
        +--------+
        '''
        '''
        更改前的代码
        '''
        raw_line_num = response.selector.xpath('//tr[@data-hunk="' + data_hunk + '"]//td[contains(@class,"blob-code blob-code-context")]/..//td[1]/@data-line-number').extract()
        #print(raw_line_num)
        raw_code = response.selector.xpath('//tr[@data-hunk="' + data_hunk + '"]//td[@class="blob-code blob-code-context"]//text()').extract()[1:]  # 不知道为什么，爬出来开头有一个换行
        raw_code = ''.join(raw_code).split('\n')
        #print(raw_code)
        # 行号和代码合并为一个dict
        raw_code_dict = dict(zip(raw_line_num, raw_code))
        # for key in raw_code_dict:
        #     print(key+raw_code_dict[key])

        '''
        删除的代码
        '''
        old_code = response.selector.xpath('//tr[@data-hunk="' + data_hunk + '"]//td[contains(@class,"blob-code blob-code-deletion")]//text()').extract()[1:]
        old_code = ''.join(old_code).split('\n')
        # 让这几行代码对齐
        if not old_code[0] == '    ':
            old_code[0] = '    ' + old_code[0]
        #print(old_code)
        old_code_line_num = response.selector.xpath('//tr[@data-hunk="' + data_hunk + '"]//td[contains(@class,"blob-code blob-code-deletion")]/..//td[1]/@data-line-number').extract()
        # 行号和代码合并为一个dict
        old_code_dict = dict(zip(old_code_line_num, old_code))
        # 合并两个dict
        old_code_final = {**raw_code_dict, **old_code_dict}
        print('旧代码为：')
        # 按照行号排序输出
        for key in sorted(old_code_final):
            print(key + old_code_final[key])




        '''
        +--------+
        |新代码处理|
        +--------+
        '''

        '''
        更改前的代码
        '''
        raw_line_num = response.selector.xpath('//tr[@data-hunk="' + data_hunk + '"]//td[contains(@class,"blob-code blob-code-context")]/..//td[2]/@data-line-number').extract()
        #print(raw_line_num)
        raw_code = response.selector.xpath('//tr[@data-hunk="' + data_hunk + '"]//td[@class="blob-code blob-code-context"]//text()').extract()[1:]  # 不知道为什么，爬出来开头有一个换行
        raw_code = ''.join(raw_code).split('\n')
        #print(raw_code)
        # 行号和代码合并为一个dict
        raw_code_dict = dict(zip(raw_line_num, raw_code))

        # for key in raw_code_dict:
        #     print(key+raw_code_dict[key])

        '''
        新增的代码
        '''

        new_code = response.selector.xpath('//tr[@data-hunk="' + data_hunk + '"]//td[contains(@class,"blob-code blob-code-addition")]//text()').extract()[1:]
        new_code = ''.join(new_code).split('\n')
        # 让这几行代码对齐
        if not new_code[0] == '    ':
            new_code[0] = '    ' + new_code[0]
        #print(new_code)
        new_code_line_num = response.selector.xpath('//tr[@data-hunk="' + data_hunk + '"]//td[contains(@class,"blob-code blob-code-addition")]/..//td[2]/@data-line-number').extract()
        # 行号和代码合并为一个dict
        new_code_dict = dict(zip(new_code_line_num, new_code))
        # 合并两个dict
        new_code_final = {**raw_code_dict, **new_code_dict}
        print('新代码为：')
        # 按照行号排序输出
        for key in sorted(new_code_final):
            print(key + new_code_final[key])

