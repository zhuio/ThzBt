# -*- coding: utf-8 -*-
import scrapy
import re

from ..items import ThzbtItem
from scrapy import Request

class ThzspiSpider(scrapy.Spider):
    name = 'thzspi'
    allowed_domains = ['thzibt.com']
    start_urls = ['http://thzibt.com/forum.php?mod=viewthread&tid=1136271&extra=page%3D1%26filter%3Dtypeid%26typeid%3D322']

    def parse(self, response):
        item = ThzbtItem()
        s = response.xpath('//div[@class="t_fsz"]').extract()[0]
        item['image_urls'] = re.findall(r'file="(.*?)"',s)
        item['name'] = re.findall(r'【影片名稱】：(.*?)<br>',s)
        item['fan'] = re.findall(r'番】 :(.*?)<br>',s)
        id1 = re.findall(r'<a href="(.*?)" onmouseover',s)[0]
        id2 = re.findall(r'imc_attachad-ad\.html\?(.*)',id1)[0]
        item['bt_url'] = ['http://thzibt.com/forum.php?mod=attachment&' + id2]
        yield item

        x = response.xpath('//div[@class="pcb"]').extract()[0]
        next_page = re.findall(r'上一篇：<a href="(.*?)"',x)[0]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse, dont_filter=True)
