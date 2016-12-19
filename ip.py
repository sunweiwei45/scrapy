#coding: utf-8
import json
import urllib
import xlrd
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf-8')


def get_data(ip):
    url = "http://ip.taobao.com/service/getIpInfo.php?ip="+ ip
    result = []
    jsondata = json.loads(urllib.urlopen(url).read())
    if jsondata['code'] == 0:
        result.append(jsondata[u'data'][u'ip'].encode('utf-8'))
        result.append(jsondata[u'data'][u'country'].encode('utf-8'))
        result.append(jsondata[u'data'][u'country_id'].encode('utf-8'))
        result.append(jsondata[u'data'][u'area'].encode('utf-8'))
        result.append(jsondata[u'data'][u'area_id'].encode('utf-8'))
        result.append(jsondata[u'data'][u'region'].encode('utf-8'))
        result.append(jsondata[u'data'][u'region_id'].encode('utf-8'))
        result.append(jsondata[u'data'][u'city'].encode('utf-8'))
        result.append(jsondata[u'data'][u'city_id'].encode('utf-8'))
        result.append(jsondata[u'data'][u'county'].encode('utf-8'))
        result.append(jsondata[u'data'][u'county_id'].encode('utf-8'))
        result.append(jsondata[u'data'][u'isp'].encode('utf-8'))
        result.append(jsondata[u'data'][u'isp_id'].encode('utf-8'))
        row = [str(result[0]), str(result[1]), str(result[5]),str(result[7])]
        print str(result[0])+','+str(result[1])+','+str(result[5])+','+str(result[7])
        city_write.writerow(row)
        return (jsondata['data']['region'], jsondata['data']['city'], jsondata['data']['isp'])
    else:
        return None



if __name__ == "__main__":
#211.162.62.161 61.135.157.156 220.198.192.0 119.124.101.221
    excel = xlrd.open_workbook('F:/vote_user_2.xls')
    table = excel.sheet_by_name('Sheet1')
    city_file = open('F:/vote_user_city_2.csv', 'w')
    city_write = csv.writer(city_file,dialect='excel')
    city_write.writerow(['ip','countyr','province','city'])
    print '**********'

    print table.nrows
    for index in range(1,table.nrows,1):
        ip = table.row(index)[6].value
        # print ip
        result = get_data(ip)
        print 'index:', index
        # print(result[0]+result[1]+result[2])

    city_file.close()
