# -*- ecoding : utf-8 -*- #
#coding:utf-8
import re
import requests
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from medicine_info.items import *


class Consult(Spider):
    name = "Consult"
    custom_settings = {
        'ITEM_PIPELINES': {
            'medicine_info.pipelines.ConsultPipeline': 300,
        }
    }
    start_urls = ['http://yao.xywy.com/class.htm']
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

    def get_m_urls(self, response):
        # print response.url
        sel = Selector(response)
        urls = sel.xpath('//div[@class="s-mlist-top"]/a/@href').extract()
        for url in urls:
            mode = re.compile(r'\d+')
            digit = mode.findall(url)[0]
            url = "http://yao.xywy.com" + url
            # print url
            yield Request(url=url,callback=self.get_all_con, headers=self.headers)

        home_url = response.url.split("-")

        current = len(urls)
        if current >= 20:

            mode = re.compile(r'\d+')
            digit = mode.findall(home_url[5])[0]
            next_digit = int(digit) + 1

            next_page = home_url[0]
            for i in range(1,5):
                next_page = next_page + "-" + home_url[i]

            next_url = next_page + "-" + str(next_digit) + ".htm"
            next_cont = requests.get(next_url)
            if next_cont.text == response.body:
                pass
            else:
                yield Request(url=next_url,callback=self.get_m_urls, headers=self.headers)


    def get_all_con(self, response):
        mode = re.compile(r'\d+')
        digit = mode.findall(response.url)
        url = "http://yao.xywy.com/index.php?m=NewProduct&a=quepage&page=1&id="+str(digit[0])   ##通过拼接网址解决异步加载问题 所传参数是药品id和页数
        body = requests.get(url)
        body = body.text.decode('unicode_escape')  #将unicode码翻译成文字
        # print body
        content = re.findall(r'<ul class="p-zx-content-ul pb10 mt5 clearfix">(.*?)<\\/ul>', body, re.S)

        all_page = re.findall(r'<a href="#content">(.*?)<\\/a>', body, re.S)
        if all_page:
            last_page = all_page[-1]
            for i in range(1, int(last_page) + 1):
                con_url = "http://yao.xywy.com/index.php?m=NewProduct&a=quepage&page=" + str(i) + '&id=' + str(digit[0])
                # print con_url
                yield Request(url=con_url,callback=self.get_info, headers=self.headers)
        elif content:
            # print response.url
            yield Request(url=url,callback=self.get_info, headers=self.headers)

    def get_info(self,response):
        item = MConsult()
        m_consult_name = []
        m_consult_id = []
        medicine_id = []
        m_consult_content = []
        m_consult_reply_content = []
        m_consult_reply_name = []
        m_consult_reply_title = []
        topic_id = []

        mode = re.compile(r'\d+')
        digit = mode.findall(response.url)  ##digit[0]=page digit[1]=id
        # print response.url
        body = response.body.decode('unicode_escape')
        content = re.findall(r'<ul class="p-zx-content-ul pb10 mt5 clearfix">(.*?)<\\/ul>', body, re.S)
        # print content[0]
        for each in content:
            each = each.replace('\n', '')
            # print each ,"hahahahhah"
            con_name = re.findall(r'<span class="co1">(.*?)<\\/span>', each)[0]
            med_id = digit[1]
            consult_content = re.findall(r'<span class="p-zx-wen-cut">(.*?)<\\/span>', each)[0]
            reply_content = re.findall(r'<\\/span><span class="p-zx-da-cut">(.*?)<\\/span>', each)[0]
            doctor = re.findall(r'<span class="co1">(.*?)<\\/span>', each)
            reply_name = doctor[1].split()[0]
            title = doctor[1].split()
            if title:
                reply_title = title[1]
            else:
                reply_title = None

            post_id = re.findall(r'href="(.*?)" class="ml10 none"', each)
            t_id = post_id[0].replace('\/', '/')
            consult_id = str(digit[0]) + str(digit[1]) + str(len(reply_content)) + str(len(consult_content))

            # print con_name,'&&&&',consult_id,'&&&&',med_id,'&&&&',consult_content,'&&&&',reply_content,'&&&&',reply_name,'&&&&',reply_title,'&&&&',t_id

            m_consult_name.append(con_name)
            m_consult_id.append(consult_id)
            medicine_id.append(med_id)
            m_consult_content.append(consult_content)
            m_consult_reply_content.append(reply_content)
            m_consult_reply_name.append(reply_name)
            m_consult_reply_title.append(reply_title)
            topic_id.append(t_id)

        item['m_consult_name'] = m_consult_name
        item['m_consult_id'] = m_consult_id
        item['medicine_id'] = medicine_id
        item['m_consult_content'] = m_consult_content
        item['m_consult_reply_content'] = m_consult_reply_content
        item['m_consult_reply_name'] = m_consult_reply_name
        item['m_consult_reply_title'] = m_consult_reply_title
        item['topic_id'] = topic_id
        # print len(m_consult_name),len(m_consult_id),len(medicine_id),len(m_consult_content),len(m_consult_reply_content),len(m_consult_reply_name),len(m_consult_reply_title),len(topic_id)
        # return item