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
                comments.append({'time':time[0].text,'content':post[0].text, 'age':age[0].text})
            commentlist = self.driver.find_elements_by_xpath('//*[@id="zwlist"]/div')  
            if len(commentlist):
                for comment in commentlist:
                    time = comment.find_elements_by_xpath('./div[3]/div[1]/div[2]')
                    post = comment.find_elements_by_xpath('./div[3]/div[1]/div[3]')
                    age = comment.find_elements_by_xpath('./div[3]/div[1]/div[1]/span[2]/span[2]')
                    if len(post) and len(time) and len(age):
                        comments.append({'time':time[0].text,'content':post[0].text, 'age':age[0].text})
        return comments
