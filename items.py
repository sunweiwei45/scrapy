# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Medicine(scrapy.Item):
    medicine_id = scrapy.Field()
    medicine_name = scrapy.Field()
    medicine_license_number = scrapy.Field()
    medicine_madeby = scrapy.Field()
    medicine_attending = scrapy.Field()
    medicine_usage = scrapy.Field()
    medicine_related_illness = scrapy.Field()
    medicine_general_name = scrapy.Field()
    medicine_adr = scrapy.Field()
    medicine_avoid = scrapy.Field()
    medicine_notice = scrapy.Field()
    medicine_component = scrapy.Field()
    medicine_interactions = scrapy.Field()
    medicine_consult_number = scrapy.Field()
    medicine_evaluate_number = scrapy.Field()
    medicine_prescribed = scrapy.Field()
    medicine_chinese = scrapy.Field()
    medicine_insurance = scrapy.Field()
    medicine_made_in_china = scrapy.Field()

class MIllness(scrapy.Item):
    m_illness_id = scrapy.Field()
    m_illness_name = scrapy.Field()
    m_illness_number = scrapy.Field()


class MedAndIll(scrapy.Item):
    m_illness_id = scrapy.Field()
    medicine_id = scrapy.Field()

class MEvaluate(scrapy.Item):
    m_evaluate_id = scrapy.Field()
    medicine_id = scrapy.Field()
    m_evaluate_level = scrapy.Field()
    m_evaluate_content = scrapy.Field()
    m_evaluate_illness = scrapy.Field()
    m_evaluate_location = scrapy.Field()
    m_evaluate_date = scrapy.Field()

class MConsult(scrapy.Item):
    m_consult_id = scrapy.Field()
    m_consult_name = scrapy.Field()
    medicine_id = scrapy.Field()
    m_consult_content = scrapy.Field()
    m_consult_reply_content = scrapy.Field()
    m_consult_reply_name = scrapy.Field()
    m_consult_reply_title = scrapy.Field()
    topic_id = scrapy.Field()



















