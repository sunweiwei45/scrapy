import re
import sys
import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from medicine_info.items import *


class IllnessSpider(Spider):
    name = "Illness"

    custom_settings = {
        'ITEM_PIPELINES' : {
            'medicine_info.pipelines.IllnessPipeline': 300,
        }
    }

    start_urls = ['http://yao.xywy.com/class.htm']

    allowed_domains = ["yao.xywy.com"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",

    }

    def make_requests_from_url(self, url):
        return Request(url = url, headers=self.headers)

    def parse(self, response):  ## Get the illness urls
        sel = Selector(response)
        # d = '_blank'
        # num = '//div[@class="re-sub-con mt5"]/a[@target="%s"]/@href'%(d)
        # print num
        num = '//div[@class="re-sub-con mt5"]/a[@target="_blank"]/@href'
        illness_urls = sel.xpath(num).extract()
        for url in illness_urls:
            url = "http://yao.xywy.com" + url
            # print url
            yield Request(url,callback=self.illness_info)



    def illness_info(self,response):## Get the illness information
        sel = Selector(response)
        item = MIllness()
        mode = re.compile(r'\d+')
        digit = mode.findall(response.url)
        # ill_id = "".join(digit)
        item['m_illness_id'] = digit[0]
        nam = 'fl'
        item['m_illness_name'] = sel.xpath("//li[@class='pr'][3]/a[@class='%s']/text()"%(nam)).extract()[0]

        mode = re.compile(r'\d+')
        m_str = sel.xpath('//span[@class="fl co1"]/text()').extract()[0]
        item['m_illness_number'] = mode.findall(m_str)[0]

        return item

        # print item['m_illness_id']
        # print item['m_illness_name']
        # print item['m_illness_number']