# -*- coding: utf-8-*-
"""
    笑话插件
    减少对AIUI的依赖
    功能:
        随机选择某句笑话播放出来
"""

import os
import sys
import random
import logging


WORDS = [u"XIAOHUA"]
SLUG = u"joke"

def handle(text, mic, profile, wxbot=None, pixels=None, oled=None):
    messages = [u"全家去旅行,小明扶着桥栏看河水,爸爸对他说,中午了,我们吃饭吧。小明却说,不,我等河水流完了再吃",
                u"小明看电视，在看到小鸡孵化的过程后，突然好奇的问，妈妈，你在孵化我的时候，蛋壳到底有多大啊",
                u"幼儿园，老师问，小朋友们，有谁知道世界上有多少个国家呀？小明举手说，我知道，有两个，就是中国和外国。"]
    message = random.choice(messages)
    mic.say(message, cache=True)


def isValid(text):
    return any(word in text for word in [u"开心一下",u"笑话"])