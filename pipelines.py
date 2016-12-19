# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import json
import codecs
import MySQLdb.cursors
from twisted.enterprise import adbapi

class ConsultPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        reload(sys)
        sys.setdefaultencoding("utf-8")

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWD'],
                charset = 'utf8',
                cursorclass= MySQLdb.cursors.DictCursor,
                use_unicode = True,
                )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d =self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return d

    def _do_upinsert(self, conn, item, spider):
        m_consult_name = item['m_consult_name']
        m_consult_id = item['m_consult_id']
        medicine_id = item['medicine_id']
        m_consult_content = item['m_consult_content']
        m_consult_reply_content = item['m_consult_reply_content']
        m_consult_reply_name = item['m_consult_reply_name']
        m_consult_reply_title = item['m_consult_reply_title']
        topic_id = item['topic_id']
        m_consult_id = item['m_consult_id']

        for i in range(0,len(m_consult_id)):
            conn.execute("SET NAMES utf8")
            conn.execute("select * from m_consult where m_consult_id = '%s'" % m_consult_id[i])
            ret = conn.fetchone()
            if ret:
                pass
            else:
                conn.execute("""
                insert into m_consult(m_consult_id,m_consult_name,medicine_id,m_consult_content,m_consult_reply_content,
                m_consult_reply_name,m_consult_reply_title,topic_id)
                values('%s','%s','%s','%s','%s','%s','%s','%s') """ %
                (m_consult_id[i], m_consult_name[i], medicine_id[i],m_consult_content[i], m_consult_reply_content[i],
                    m_consult_reply_name[i], m_consult_reply_title[i], topic_id[i]))



class EvaluatePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        reload(sys)
        sys.setdefaultencoding( "utf-8" )

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWD'],
                charset = 'utf8',
                cursorclass= MySQLdb.cursors.DictCursor,
                use_unicode = True,
                )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d =self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return d

    def _do_upinsert(self, conn, item, spider):

        m_evaluate_id = item['m_evaluate_id']
        medicine_id = item['medicine_id']
        m_evaluate_level = item['m_evaluate_level']
        m_evaluate_content = item['m_evaluate_content']
        m_evaluate_illness = item['m_evaluate_illness']
        m_evaluate_location = item['m_evaluate_location']
        m_evaluate_date = item['m_evaluate_date']

        for i in range(0,len(m_evaluate_id)):
            conn.execute("SET NAMES utf8")
            conn.execute("select * from m_evaluate where m_evaluate_id = '%s'" % m_evaluate_id[i])
            ret = conn.fetchone()
            if ret:
                pass
            else:
                conn.execute("""
                  insert into m_evaluate(m_evaluate_id,medicine_id,m_evaluate_level,m_evaluate_content,m_evaluate_illness,
                m_evaluate_location,m_evaluate_date)
                  values('%s','%s',%s,'%s','%s','%s','%s') """ %
                    (m_evaluate_id[i], medicine_id[i], m_evaluate_level[i], m_evaluate_content[i], m_evaluate_illness[i],
                     m_evaluate_location[i], m_evaluate_date[i]))



class IllnessPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        reload(sys)
        sys.setdefaultencoding( "utf-8" )

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWD'],
                charset = 'utf8',
                cursorclass= MySQLdb.cursors.DictCursor,
                use_unicode = True,
                )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d =self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return d

    def _do_upinsert(self, conn, item, spider):
        conn.execute("SET NAMES utf8")
        conn.execute("select * from m_illness where m_illness_id = '%s'" % item['m_illness_id'])
        ret = conn.fetchone()
        if ret:
            pass
        else:

            conn.execute("""
                insert into m_illness(m_illness_id,m_illness_name,m_illness_number)
                values('%s','%s',%s) """ %
                (item['m_illness_id'], item['m_illness_name'], item['m_illness_number']))



class MedicinePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        reload(sys)
        sys.setdefaultencoding( "utf-8" )

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWD'],
                charset = 'utf8',
                cursorclass= MySQLdb.cursors.DictCursor,
                use_unicode = True,
                )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d =self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return d

    def _do_upinsert(self, conn, item, spider):
        conn.execute("SET NAMES utf8")
        conn.execute("select * from medicine where medicine_id = '%s'" % item['medicine_id'])
        ret = conn.fetchone()
        if ret:
            pass
        else:

            conn.execute("""
                insert into medicine(medicine_id, medicine_name, medicine_license_number, medicine_madeby,
                medicine_attending, medicine_usage, medicine_related_illness, medicine_general_name, medicine_adr, medicine_avoid,
                medicine_notice,medicine_component,medicine_interactions,medicine_consult_number,medicine_evaluate_number,
                medicine_prescribed,medicine_chinese,medicine_insurance,medicine_made_in_china)
                values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', %s, %s, %s, %s, %s, %s) """ %
                (item['medicine_id'], item['medicine_name'], item['medicine_license_number'], item['medicine_madeby'], item['medicine_attending'],
                    item['medicine_usage'], item['medicine_related_illness'], item['medicine_general_name'], item['medicine_adr'], item['medicine_avoid'],
                 item['medicine_notice'], item['medicine_component'], item['medicine_interactions'], item['medicine_consult_number'], item['medicine_evaluate_number'],
                 item['medicine_prescribed'], item['medicine_chinese'], item['medicine_insurance'], item['medicine_made_in_china']))

class MedIllnessPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        reload(sys)
        sys.setdefaultencoding( "utf-8" )

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWD'],
                charset = 'utf8',
                cursorclass= MySQLdb.cursors.DictCursor,
                use_unicode = True,
                )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d =self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return d

    def _do_upinsert(self, conn, item, spider):
        conn.execute("SET NAMES utf8")
        conn.execute("select * from medicine_illness where m_illness_id = '%s' and medicine_id = '%s'" % (item['m_illness_id'],item['medicine_id']))
        ret = conn.fetchone()
        if ret:
            pass
        else:

            conn.execute("""
                insert into medicine_illness(m_illness_id,medicine_id)
                values('%s','%s') """ %
                (item['m_illness_id'], item['medicine_id']))

