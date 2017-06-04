#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on 2017��5��17��
@author: luhaiya
@id: 2016110274
@description:
'''
from selenium import webdriver
import time
import json
import re  
# from HTMLParser import HTMLParser 
from myNLP import *
# from lxml import html
# import requests
class Crawler:
    url = ''
    newurl = set()
    headers = {}
    cookies = {}
    def __init__(self, stocknum, page):
        self.url = 'http://guba.eastmoney.com/list,'+stocknum+',5_'+page+'.html'
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        #cap["phantomjs.page.settings.loadImages"] = False
        #cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        self.driver = webdriver.PhantomJS(desired_capabilities=cap)
    def crawAllHtml(self,url):
        self.driver.get(url)
        time.sleep(2)
#         htmlData = requests.get(url).content.decode('utf-8')
#         domTree = html.fromstring(htmlData)
#         return domTree
    def getNewUrl(self,url):
        self.newurl.add(url)
    def filterHtmlTag(self, htmlStr):
        self.htmlStr = htmlStr  
        #先过滤CDATA  
        re_cdata=re.compile('//<!CDATA\[[^>]*//\]>',re.I) #匹配CDATA  
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script  
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style  
        re_br=re.compile('<br\s*?/?>')#处理换行  
        re_h=re.compile('</?\w+[^>]*>')#HTML标签  
        re_comment=re.compile('<!--[^>]*-->')#HTML注释  
        s=re_cdata.sub('',htmlStr)#去掉CDATA  
        s=re_script.sub('',s) #去掉SCRIPT  
        s=re_style.sub('',s)#去掉style  
        s=re_br.sub('\n',s)#将br转换为换行  
        blank_line=re.compile('\n+')#去掉多余的空行  
        s = blank_line.sub('\n',s)  
        s=re_h.sub('',s) #去掉HTML 标签  
        s=re_comment.sub('',s)#去掉HTML注释  
        #去掉多余的空行  
        blank_line=re.compile('\n+')  
        s=blank_line.sub('\n',s)  
        return s
    def getData(self):
        comments = []
        self.crawAllHtml(self.url)
        postlist = self.driver.find_elements_by_xpath('//*[@id="articlelistnew"]/div')
        for post in postlist:
            href = post.find_elements_by_tag_name('span')[2].find_elements_by_tag_name('a')
            if len(href):
                self.getNewUrl(href[0].get_attribute('href'))
#             if len(post.find_elements_by_xpath('./span[3]/a/@href')):
#                 self.getNewUrl('http://guba.eastmoney.com'+post.find_elements_by_xpath('./span[3]/a/@href')[0])
        for url in self.newurl:
            self.crawAllHtml(url)
            time = self.driver.find_elements_by_xpath('//*[@id="zwconttb"]/div[2]')
            post = self.driver.find_elements_by_xpath('//*[@id="zwconbody"]/div')
            age = self.driver.find_elements_by_xpath('//*[@id="zwconttbn"]/span/span[2]')
            if len(post) and len(time) and len(age):
                text = self.filterHtmlTag(post[0].text)
                if len(text):
                    tmp = myNLP(text)
                    comments.append({'time':time[0].text,'content':tmp.prob, 'age':age[0].text})
            commentlist = self.driver.find_elements_by_xpath('//*[@id="zwlist"]/div')  
            if len(commentlist):
                for comment in commentlist:
                    time = comment.find_elements_by_xpath('./div[3]/div[1]/div[2]')
                    post = comment.find_elements_by_xpath('./div[3]/div[1]/div[3]')
                    age = comment.find_elements_by_xpath('./div[3]/div[1]/div[1]/span[2]/span[2]')
                    if len(post) and len(time) and len(age):
                        text = self.filterHtmlTag(post[0].text)
                        if len(text):
                            tmp = myNLP(text)
                            comments.append({'time':time[0].text,'content':tmp.prob, 'age':age[0].text})
        return json.dumps(comments)
