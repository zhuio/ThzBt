# -*- coding: utf-8 -*-
import scrapy
import re

from ..items import ThzbtItem
from scrapy import Request

class ThzspiSpider(scrapy.Spider):
    name = 'thzspi'
    allowed_domains = ['thzibt.com']
    start_urls = ['http://thzibt.com/thread-731418-1-1.html']

    def parse(self, response):
        item = ThzbtItem()
        s = response.xpath('//div[@class="t_fsz"]').extract()[0]
        item['image_urls'] = re.findall(r'file="(.*?)"',s)
        item['name'] = response.xpath('//span[@id="thread_subject"]/text()').extract()
        item['fan'] = response.xpath('//title/text()').extract()
        try:
            id = re.findall(r'imc_attachad-ad\.html\?(.*?)"',s).pop()
            btls = re.findall(r'(.*?)%3D&amp;nothumb',id)
            if len(btls) != 0:
                id = btls[0]
            item['bt_url'] = ['http://thzibt.com/forum.php?mod=attachment&' + id]
        except Exception as e:
            print('这个页面没有种子')
        yield item

        x = response.xpath('//div[@class="pcb"]').extract()[0]
        next_page = re.findall(r'上一篇：<a href="(.*?)"',x)[0]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse, dont_filter=True)
