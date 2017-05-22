#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on 2017��5��17��
@author: luhaiya
@id: 2016110274
@description:
'''
from selenium import webdriver
from lxml import html
import requests
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
#         htmlData = requests.get(url).content.decode('utf-8')
#         domTree = html.fromstring(htmlData)
#         return domTree
    def getNewUrl(self,url):
        self.newurl.add(url)
    def getData(self):
        comments = []
        self.crawAllHtml(self.url)
        postlist = self.driver.find_elements_by_xpath('//*[@id="articlelistnew"]/div')
        for post in postlist:
            if len(post.xpath('./span[3]/a/@href')):
                self.getNewUrl('http://guba.eastmoney.com'+post.xpath('./span[3]/a/@href')[0])
        for url in self.newurl:
            self.crawAllHtml(url)
            time = self.driver.find_elements_by_xpath('//*[@id="zwconttb"]/div[2]/text()')
            post = self.driver.find_elements_by_xpath('//*[@id="zwconbody"]/div/text()')
            age = self.driver.find_elements_by_xpath('//*[@id="zwconttbn"]/span/span[2]/text()')
            if len(post) and len(time) and len(age):
                comments.append({'time':time[0],'content':post[0], 'age':age[0]})
            commentlist = self.driver.find_elements_by_xpath('//*[@id="zwlist"]/div')  
            if len(commentlist):
                for comment in commentlist:
                    time = comment.xpath('./div[3]/div[1]/div[2]/text()')
                    post = comment.xpath('./div[3]/div[1]/div[3]/text()')
                    age = comment.xpath('./div[3]/div[1]/div[1]/span[2]/span[2]/text()')
                    if len(post) and len(time) and len(age):
                        comments.append({'time':time[0],'content':post[0], 'age':age[0]})
        return comments
