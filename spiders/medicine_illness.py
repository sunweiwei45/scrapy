# -*- ecoding : utf-8 -*- #

import re
import sys
import scrapy
import requests
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from medicine_info.items import *

class MedicineIllness(Spider):
    name = "MedicineIllness"
    custom_settings = {
        'ITEM_PIPELINES' : {
            'medicine_info.pipelines.MedIllnessPipeline': 300,
        }
    }

    start_urls = ["http://yao.xywy.com/class.htm"]
    allowed_domains = ["yao.xywy.com"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",

    }

    def make_requests_from_url(self, url):
        return Request(url = url, headers=self.headers)

    def parse(self, response):
        sel = Selector(response)
        illness_urls = sel.xpath('//div[@class="re-sub-con mt5"]/a[@target="_blank"]/@href').extract()
        for url in illness_urls:
            url = "http://yao.xywy.com" + url
            # print url
            yield Request(url,callback=self.get_m_urls, headers=self.headers)

    def get_m_urls(self,response):  ## Get the medicine urls from all the pages of one illness
        # print response.url
        item = MedAndIll()
        sel = Selector(response)
        urls = sel.xpath('//div[@class="s-mlist-top"]/a/@href').extract()
        mode = re.compile(r'\d+')

        for url in urls:
            # print url
            ill_id = mode.findall(response.url)
            # ill_id = "".join(ill_id)
            item['m_illness_id'] = ill_id[0]
            yield Request(url="http://yao.xywy.com" + url, meta={'item': item}, callback=self.get_info, headers=self.headers)


        home_url = response.url.split("-") ## Split the url to six parts by "-"

        current = len(urls)
        if current >= 20:
            ##Judge whether it has next pages
            mode = re.compile(r'\d+')
            digit = mode.findall(home_url[5])[0]
            next_digit = int(digit) + 1

            next_page = home_url[0]
            for i in range(1,5):
                ## link the first five parts
                next_page = next_page + "-" + home_url[i]

            next_url = next_page + "-" + str(next_digit) + ".htm"
            next_cont = requests.get(next_url)
            if next_cont.text == response.body:
                pass
            else:
                yield Request(url=next_url,callback=self.get_m_urls, headers=self.headers)

    def get_info(self,response):
        item = response.meta['item']
        # item = MedAndIll()
        mode = re.compile(r'\d+')
        med_id = mode.findall(response.url)
        item['medicine_id'] = med_id[0]
        # print item['m_illness_id'],item['medicine_id']
        return item
