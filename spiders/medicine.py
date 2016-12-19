# -*- coding: utf-8 -*-

import re
import sys
import scrapy
# import requests
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from medicine_info.items import *


class MedicineSpider(Spider):
    name = "Medicine"

    custom_settings = {
        'ITEM_PIPELINES' : {
            'medicine_info.pipelines.MedicinePipeline': 300,
        }
    }


    start_urls = ['http://yao.xywy.com/class.htm']

    allowed_domains = ["yao.xywy.com"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",

    }

    def make_requests_from_url(self, url):
        return Request(url = url, headers=self.headers)

    def parse(self, response):  ## 获得所有疾病的url
        sel = Selector(response)
        illness_urls = sel.xpath('//div[@class="re-sub-con mt5"]/a[@target="_blank"]/@href').extract()
        for url in illness_urls:
            url = "http://yao.xywy.com" + url
            # print url
            yield Request(url, callback=self.get_m_urls, headers=self.headers)
        # yield Request("http://yao.xywy.com/class/522-0-0-1-0-1.htm",callback=self.get_m_urls)


    def get_m_urls(self,response):  ##从疾病页获得每一个药品的url
        # print response.url
        sel = Selector(response)
        urls = sel.xpath('//div[@class="s-mlist-top"]/a/@href').extract()
        for url in urls:
            url = "http://yao.xywy.com" + url
            yield Request(url,callback=self.grt_m_info,headers=self.headers)
            # print url

        home_url = response.url.split("-") ## 使用"-"将url分成几部分

        current = len(urls)   #检查每一页的药品数量，若不小于20就进入下一页
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
            if next_cont.text == response.body:#如果下一页内容和这一页一样就停止
                pass
            else:
                yield Request(url=next_url,callback=self.get_m_urls, headers=self.headers)



    def grt_m_info(self,response):  ##信息获取
        item = Medicine()
        sel = Selector(response)
        mode = re.compile(r'\d+')
        digit = mode.findall(response.url)

        item['medicine_id'] = digit[0]
        name = sel.xpath('//h1/text()').extract()
        if name:
            item['medicine_name'] =name[0]
        else:
            return None #如果没有名字就不采集

        license = sel.xpath('//li[@class="li1 li2"]/div/text()').extract()

        if license:
            mode = re.compile(r'\d+')
            digit = mode.findall(license[0])
        else:
            digit = None                                                                                                                                                                                                                                                     ## Let digit become none.

        if digit:
            item['medicine_license_number'] = license[0]
        else:
            list=[]
            list.append(sel.xpath('//span[@class="r-rumbox"]/b[@style="left:-63px;"]/text()').extract()[0])
            list.append(sel.xpath('//span[@class="r-rumbox"]/b[@style="left:-56px;"]/text()').extract()[0])
            list.append(sel.xpath('//span[@class="r-rumbox"]/b[@style="left:-49px;"]/text()').extract()[0])
            list.append(sel.xpath('//span[@class="r-rumbox"]/b[@style="left:-42px;"]/text()').extract()[0])
            list.append(sel.xpath('//span[@class="r-rumbox"]/b[@style="left:-35px;"]/text()').extract()[0])
            list.append(sel.xpath('//span[@class="r-rumbox"]/b[@style="left:-28px;"]/text()').extract()[0])
            list.append(sel.xpath('//span[@class="r-rumbox"]/b[@style="left:-21px;"]/text()').extract()[0])
            list.append(sel.xpath('//span[@class="r-rumbox"]/b[@style="left:-14px;"]/text()').extract()[0])
            list.append(sel.xpath('//span[@class="r-rumbox"]/b[@style="left:-7px;"]/text()').extract()[0])
            license = ""
            for i in range(9):
                license = license + list[i]

            l_cont = sel.xpath('//li[@class="li1 li2"]/div[1]/text()').extract()
            if l_cont:
                item['medicine_license_number'] = l_cont[0] + license
            else:
                item['medicine_license_number'] = license


        madeby = sel.xpath('//li[@class="li1"]/a[@target="_blank"]/text()').extract()
        if madeby:
            item['medicine_madeby'] = madeby[0]
        else:
            item['medicine_madeby'] = None

        attending = sel.xpath('//div[@id="smsList"]/ul[2]/li[2]')
        if attending:
            item['medicine_attending'] = attending.xpath("string(.)").extract()[0].replace('\'',' ')
        else:
            item['medicine_attending'] = None


        u_cont = sel.xpath('//li[@class="li1"][3]/div[@class="p-inf-ul-right p-inf-ul-rights fl"]/span')
        if u_cont:
            item['medicine_usage'] = u_cont.xpath('string(.)').extract()[0].replace('\'',' ')
        else:
            item['medicine_usage'] = None


        rel_ill_cont = sel.xpath('//li[@class="li1"][4]/div[@class="p-inf-ul-right p-inf-ul-jb fl"]')
        if rel_ill_cont:
            item['medicine_related_illness'] = rel_ill_cont.xpath('string(.)').extract()[0].replace('\'',' ')
        else:
            item['medicine_related_illness'] = None


        item['medicine_general_name'] = sel.xpath('//ul[@class="p-sms mt15 clearfix"][1]/li[2]/text()').extract()[0]

        adr = sel.xpath("//li[a[@name='fanying']]/following-sibling::li")
        if adr:
            item['medicine_adr'] = adr.xpath("string(.)").extract()[0].replace('\'',' ')
        else:
            item['medicine_adr'] = None


        avoid = sel.xpath("//li[a[@name='jinji']]/following-sibling::li")
        if avoid:
            item['medicine_avoid'] = avoid.xpath("string(.)").extract()[0].replace('\'',' ')
        else:
            item['medicine_avoid'] = None

        notice = sel.xpath("//li[a[@name='zhuyi']]/following-sibling::li")
        if notice:
            item['medicine_notice'] = notice.xpath("string(.)").extract()[0].replace('\'',' ')
        else:
            item['medicine_notice'] = None

        component = sel.xpath("//li[a[@name='chengfen']]/following-sibling::li")
        if component:
            item['medicine_component'] = component.xpath("string(.)").extract()[0].replace('\'',' ')
        else:
            item['medicine_component'] = None

        interactions = sel.xpath("//li[a[@name='zuoyong']]/following-sibling::li")
        if interactions:
            item['medicine_interactions'] = interactions.xpath("string(.)").extract()[0].replace('\'',' ')
        else:
            item['medicine_interactions'] = None


        mode = re.compile(r'\d+')  #由于网页改版，使用了ajax后台数据传输所以非常麻烦
        digit = mode.findall(response.url)
        url = "http://yao.xywy.com/index.php?s=NewProduct/advisory_arr&page=1&id="+str(digit[0])
        body = requests.get(url)
        body = body.text.decode('unicode_escape')
        c_num = re.findall(r'"count":(.*?)}', body, re.S)

        # consult_num = sel.xpath("//li[@class='current cp']/text()").extract()
        # mode = re.compile(r'\d+')
        c_num = mode.findall(c_num[0])
        if c_num:
            item['medicine_consult_number'] = c_num[0]

        else:
            item['medicine_consult_number'] = 0

        url = "http://yao.xywy.com/index.php?s=NewProduct/common_arr&page=1&id="+str(digit[0]) #由于网页改版，使用了ajax后台数据传输所以非常麻烦
        body = requests.get(url)
        body = body.text.decode('unicode_escape')
        e_num = re.findall(r'"count":(.*?)}', body, re.S)
        # evaluate_num = sel.xpath("//li[@class='cp']/text()").extract()
        # mode = re.compile(r'\d+')
        e_num = mode.findall(e_num[0])
        if e_num:
            item['medicine_evaluate_number'] = e_num[0]
        else:
            item['medicine_evaluate_number'] = 0




        m_character = sel.xpath("//li[@class='first f12']/div")
        m_list = []
        for each in m_character:
            m_list.append(each.xpath("string(.)").extract()[0])
        if u"处方药" in m_list:
            item['medicine_prescribed'] = 1
        else:
            item['medicine_prescribed'] = 0

        if u"中成药" in m_list:
            item['medicine_chinese'] = 1
        else:
            item['medicine_chinese'] = 0

        if u"医保甲类" in m_list:
            item['medicine_insurance'] = 1
        elif u"医保乙类" in m_list:
            item['medicine_insurance'] = 1
        else:
            item['medicine_insurance'] = 0


        if u"国产" in m_list:
            item['medicine_made_in_china'] = 1
        else:
            item['medicine_made_in_china'] = 0

        return item

        # print item['medicine_id']
        # print item['medicine_name']
        # print item['medicine_license_number']
        # print item['medicine_madeby']
        # print item['medicine_attending']
        # print item['medicine_usage']
        # print item['medicine_related_illness']
        # print item['medicine_general_name']
        # print item['medicine_adr']
        # print item['medicine_avoid']
        # print item['medicine_notice']
        # print item['medicine_component']
        # print item['medicine_interactions']
        # print item['medicine_consult_number']
        # print item['medicine_evaluate_number']
        # print item['medicine_prescribed']
        # print item['medicine_chinese']
        # print item['medicine_insurance']
        # print item['medicine_made_in_china']
        #





























