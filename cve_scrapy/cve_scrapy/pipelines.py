# -*- coding: UTF-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import requests

class CveScrapyPipeline:
    def process_item(self, item, spider):
        home_path = os.environ['HOME']
        # home_path = 'var/tmp'
        file_name = item['file'].split('/')[-1]
        old_file_path = home_path + '/' + item['keyword'] + '/' + item['year'] + '/' + item[
            'cve_name'] + '/' + file_name + '.old'
        new_file_path = home_path + '/' + item['keyword'] + '/' + item['year'] + '/' + item[
            'cve_name'] + '/' + file_name + '.new'
        README_path = home_path + '/' + item['keyword'] + '/' + item['year'] + '/' + item['cve_name'] + '/README.txt'

        if not os.path.exists(old_file_path):
            old_file_code = requests.get(item['old_file_url']).content
            os.mknod(old_file_path)
            with open(old_file_path, "w") as f:
                f.write(old_file_code)

        if not os.path.exists(new_file_path):
            new_file_code = requests.get(item['new_file_url']).content
            os.mknod(new_file_path)
            with open(new_file_path, "w") as f:
                f.write(new_file_code)

        if not os.path.exists(README_path):
            README_content = item
            os.mknod(README_path)
            with open(README_path, "w") as f:
                f.write(README_content)
