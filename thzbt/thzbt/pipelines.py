# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipelines to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import re
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.contrib.pipeline.files import FilesPipeline
from scrapy.exceptions import DropItem
from fake_useragent import UserAgent
ua = UserAgent()
headers = {"User-Agent": ua.chrome, "Referer":"thzibt.com"}
class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        fname = request.meta['fan'] + '_' + request.url.split('/')[-1]
        wfile = request.meta['name']
        filename = wfile + '/' + fname
        return filename

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            ls = re.findall(r'data',image_url)
            if len(ls) != 0:
                image_url = 'http://thzibt.com' + image_url
            yield scrapy.Request(image_url,headers = headers,meta={'name': item['name'][0],'fan': item['fan'][0]})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item



class MyfilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for url in item["bt_url"]:
            yield scrapy.Request(url, headers = headers, meta={'name': item['name'][0],'fan': item['fan'][0]})

    def file_path(self, request, response=None, info=None):
        fname = request.meta['fan'] + '_' + request.url.split('/')[-1]
        wfile = request.meta['name']
        filename = wfile + '/' + fname
        return filename

    def item_completed(self, results, item, info):
        file_paths = [x["path"] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        item['file_paths'] = file_paths
        return item
