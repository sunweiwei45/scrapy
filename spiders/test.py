# -*- encoding : utf-8 -*- #
import re
import sys
import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
# from medicine_info.items import *

class Test(Spider):
    name = "test"
    start_urls = ["http://yao.xywy.com/goods/406.htm"]
    def parse(self,response):
        # print response.body
        url = "http://yao.xywy.com/index.php?m=NewProduct&a=quepage&page=3&id=406"
        # data = {'page':'3','id':'406'}
        # header = {}
        # url = "http://yao.xywy.com/goods/406.htm"
        yield Request("http://yao.xywy.com/class/196-0-0-1-0-1.htm",callback=self.get_m_urls)

    def get_m_urls(self,response):  ## Get the medicine urls from all the pages of one illness
        yield Request(url="http://yao.xywy.com/index.php?m=NewProduct&a=quepage&page=1&id=406",callback=self.get_all_con)



    def get_all_con(self,response):

        yield Request(url="http://yao.xywy.com/index.php?m=NewProduct&a=quepage&page=1&id=409",callback=self.get_info)


        # con_num = len(content)
        # print con_num
        # if con_num >=10:
        #     mode = re.compile(r'\d+')
        #     digit = mode.findall(response.url)[0]
        #     next_digit = int(digit) + 1
        #     # print response.url.replace(str(digit),str(next_digit))
        #     yield Request(url=response.url.replace(str(digit),str(next_digit),1),callback=self.get_all_con)



    def get_info(self,response):
        list = ['a','s','d','f','g','h','jj','k','kl']
        print len(list)
        for i in range(0,len(list)):
            print list[i]

