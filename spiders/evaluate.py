# -*- ecoding : utf-8 -*- #

import re
import requests
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from medicine_info.items import *


class Evaluate(Spider):
    name = "Evaluate"
    custom_settings = {
        'ITEM_PIPELINES' : {
            'medicine_info.pipelines.EvaluatePipeline': 300,
        }
    }

    start_urls = ['http://yao.xywy.com/class.htm']
    allowed_domains = ["yao.xywy.com"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",

    }

    def make_requests_from_url(self, url):
        return Request(url=url, headers=self.headers)

    def parse(self, response):  ## Get the illness urls
        sel = Selector(response)
        illness_urls = sel.xpath('//div[@class="re-sub-con mt5"]/a[@target="_blank"]/@href').extract()
        for url in illness_urls:
            url = "http://yao.xywy.com" + url
            # print url
            yield Request(url,callback=self.get_m_urls, headers=self.headers)


    def get_m_urls(self, response):  ## Get the medicine urls from all the pages of one illness
        # print response.url
        sel = Selector(response)
        urls = sel.xpath('//div[@class="s-mlist-top"]/a/@href').extract()
        for url in urls:
            eval_url = "http://yao.xywy.com" + url
            yield Request(url=eval_url,callback=self.get_all_eval, headers=self.headers)

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


    def get_all_eval(self, response):

        # print response.url
        mode = re.compile(r'\d+')
        digit = mode.findall(response.url)
        url = "http://yao.xywy.com/index.php?m=NewProduct&a=commentpage&page=1&id="+str(digit[0])
        body = requests.get(url)
        body = body.text.decode('unicode_escape')
        content = re.findall(r'<ul class="p-pj-content-ul pb5 mt5 clearfix">(.*?)<\\/ul>', body, re.S)

        all_page = re.findall(r'<a href="#content">(.*?)<\\/a>', body, re.S)
        if all_page:
            last_page = int(all_page[-1])
            for i in range(1, last_page + 1):
                    eval_url = "http://yao.xywy.com/index.php?m=NewProduct&a=commentpage&page=" + str(i) + "&id=" + str(digit[0])
                    yield Request(url=eval_url,callback=self.get_info, headers=self.headers)

        elif content:
            yield Request(url=response.url,callback=self.get_info, headers=self.headers)

    def get_info(self,response):
        item = MEvaluate()
        m_evaluate_id = []
        medicine_id = []
        m_evaluate_level = []
        m_evaluate_content = []
        m_evaluate_illness = []
        m_evaluate_location = []
        m_evaluate_date = []

        mode = re.compile(r'\d+')
        digit = mode.findall(response.url)  ##digit[0]=page digit[1]=id
        # print response.url
        body = response.body.decode('unicode_escape')
        # print body
        content = re.findall(r'<ul class="p-pj-content-ul pb5 mt5 clearfix">(.*?)<\\/ul>', body, re.S)
        for each in content:
            # print each
            med_id= digit[1]
            star = re.findall('span-huang', each, re.S)
            evaluate_level = len(star)
            evaluate_content = re.findall(r'<div class="fl p-pj-content-text">(.*?)<\\/div>',
                                                                each, re.S)[0]
            evaluate_illness = re.findall(r'<div class="fl p-pj-content-text">(.*?)<\\/div>',
                                                                each, re.S)[1]
            evaluate_location= re.findall(r'<div class="fr p-pj-content-time">(.*?)<span>', each,
                                                                 re.S)[0]
            date = re.findall(r'<\\/span>(.*?)<li class="mt5">', each,
                                                             re.S)[0]
            date = re.findall(r'\d+',date,re.S)
            date1 = '-'.join(date[0:3])
            date2 = ':'.join(date[3:6])
            evaluate_date= date1 +' '+ date2
            eval_id = mode.findall(evaluate_date)
            eval_id = "".join(eval_id)
            evaluate_id = str(digit[1]) + eval_id

            m_evaluate_id.append(evaluate_id)
            medicine_id.append(med_id)
            m_evaluate_level.append(evaluate_level)
            m_evaluate_content.append(evaluate_content)
            m_evaluate_illness.append(evaluate_illness)
            m_evaluate_location.append(evaluate_location)
            m_evaluate_date.append(evaluate_date)

        item['m_evaluate_id'] = m_evaluate_id
        item['medicine_id'] = medicine_id
        item['m_evaluate_level'] = m_evaluate_level
        item['m_evaluate_content'] = m_evaluate_content
        item['m_evaluate_illness'] = m_evaluate_illness
        item['m_evaluate_location'] = m_evaluate_location
        item['m_evaluate_date'] = m_evaluate_date
        return item
        # print len(m_evaluate_id),len(medicine_id),len(m_evaluate_level),len(m_evaluate_content),len(m_evaluate_illness),len(m_evaluate_location),len(m_evaluate_date)







