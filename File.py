#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on 2017��5��17��
@author: luhaiya
@id: 2016110274
@description:
'''
import io
class File:
    name = ''
    type = ''
    src = ''
    file = ''
    def __init__(self,name, type, src):
        self.name = name
        self.type = type
        self.src = src  
        filename = self.src+self.name+'.'+self.type
        self.file = io.open(filename,'w+', encoding = 'utf-8')
    def inputData(self,data):
        self.file.write(data.decode('utf-8'))
        self.file.close()
    def closeFile(self):
        self.file.close()
