#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on 2017年5月17日
@author: luhaiya
@id: 2016110274
@description:
'''
#http://data.eastmoney.com/stockcomment/  所有股票的列表信息
#http://guba.eastmoney.com/list,600000,5.html 某只股票股民的帖子页面
#http://quote.eastmoney.com/sh600000.html?stype=stock 查询某只股票
from Crawler import *
from File import *
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
           
def main():
    stocknum = str(600000)
    total = dict()
    for i in range(1,10):
        page = str(i)
        crawler = Crawler(stocknum, page)
        datalist = crawler.getData()
        comments = File(stocknum+'_page_'+page,'json','./data/')
        comments.inputData(datalist)
        data = open('./data/'+stocknum+'_page_'+page+'.json','r').read()
        jsonData = json.loads(data)
        for detail in jsonData:
            num = '1' if '年' not in detail['age'].encode('utf-8') else detail['age'].encode('utf-8').replace('年','')
            num = float(num)
            date = detail['time'][4:14].encode('utf-8')
            total[date] = total[date] if date in total.keys() else {'num':0, 'content':0}
            total[date]['num'] = total[date]['num'] + num if total[date]['num'] else num
            total[date]['content'] = total[date]['content'] + detail['content']*num if total[date]['content'] else detail['content']*num
    total = json.dumps(total)
    totalfile = File(stocknum,'json','./data/')
    totalfile.inputData(total)
if __name__ == "__main__":
    main()
