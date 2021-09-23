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
        # home_path = os.environ['HOME']
        home_path = '/tmp'
        file_name = item['file'].split('/')[-1]
        file_dir = home_path + '/' + item['keyword'] + '/' + item['year'] + '/' + item[
            'cve_name'] + '/'
        old_file_path = file_dir + file_name.split('.')[0] + '_old.' + file_name.split('.')[1]
        new_file_path = file_dir + file_name.split('.')[0] + '_new.' + file_name.split('.')[1]
        README_path = file_dir + 'README.txt'

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        if not os.path.exists(old_file_path):
            old_file_code = requests.get(item['old_file_url']).content
            with open(old_file_path, "w") as f:
                f.write(old_file_code.decode('utf-8'))

        if not os.path.exists(new_file_path):
            new_file_code = requests.get(item['new_file_url']).content
            with open(new_file_path, "w") as f:
                f.write(new_file_code.decode('utf-8'))

        if not os.path.exists(README_path):
            README_content = 'repository:' + item['repository'] + '\n'  +'file:' + item['file'] + '\n'
            print(README_content)
            with open(README_path, "a") as f:
                f.write(README_content)
        else:
            README_content = 'file:' + item['file'] + '\n'
            print(README_content)
            with open(README_path, "a") as f:
                f.write(README_content)
