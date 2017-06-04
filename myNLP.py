#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from snownlp import SnowNLP
class myNLP:
    prob = 0.5
    def _init_(self, text):
        self.prob = SnowNLP(text).sentiments
