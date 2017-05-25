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
    page = str(1)
    crawler = Crawler(stocknum, page)
    datalist = crawler.getData()
    strdata = ''
#     for data in datalist:
#         strdata += data['content']
    txt = File(stocknum,'json','./data/')
    txt.inputData(datalist)
            
if __name__ == "__main__":
    main()
