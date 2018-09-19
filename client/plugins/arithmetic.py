# -*- coding: utf-8-*-
"""
    数学运算插件
    减少对AIUI的依赖
    功能:
        实际生活情景算术问答
        九九乘法表问答
"""


import os
import sys
import logging


WORDS = [u"SUANSU"]
SLUG = "arithmetic"


def handle(text, mic, profile, wxbot=None, pixels=None, oled=None):
    if any(word in text for word in [u"算术", u"数学乐园", u"数学题"]):
        mic.say(u"进入数学乐园，小朋友可要听好了", cache=True)
        subtraction(mic)
    elif any(word in text for word in [u"九九乘法表",u"乘法"]):
        mic.say(u"让我出一些乘法的题考考你吧", cache=True)
        multiplication(mic)



def subtraction(mic, profile=None):
    """ 基本减法算术题 """
    mic.say(u"有六个苹果，妈妈吃了一个，爸爸吃了一个，还剩多少个苹果呢", cache=True)
    Error_flag = False
    message = ""
    while not message:
        if mic.chatting_mode:
            message = mic.activeListenWithButton()    #按键录入音频
        else:
            message = mic.activeListen(MUSIC=True)
    if any(word in message for word in [u"四",u"4"]):
        mic.say(u"真棒！要是你也吃了一个还剩多少个苹果呢", cache=True)
    else:
        mic.say(u"回答错误,应该还剩四个苹果，那接着听题吧，剩下的四个苹果你也吃了一个还剩多少个苹果呢", cache=True)
        Error_flag = True
    message = ""
    while not message:
        if mic.chatting_mode:
            message = mic.activeListenWithButton()    #按键录入音频
        else:
            message = mic.activeListen(MUSIC=True)
    if any(word in message for word in [u"三",u"3"]):
        mic.say(u"真棒，真是一个聪明的宝宝，我先退下了", cache=True)
    else:
        if not Error_flag:
            mic.say(u"哎呀，回答错误，应该还剩三个，要多练习一下", cache=True)
        else:
             mic.say(u"很遗憾，你一题也没有答对，要好好加油，回去多练习一下吧", cache=True)

def multiplication(mic, profile=None):
    mic.say(u"请听题，2乘8等于多少", cache=True)
    Error_flag = False
    message = ""
    while not message:
        if mic.chatting_mode:
            message = mic.activeListenWithButton()    #按键录入音频
        else:
            message = mic.activeListen(MUSIC=True)
    if any(word in message for word in [u"16",u"十六"]):
        mic.say(u"真棒！九乘九等于多少", cache=True)
    else:
        mic.say(u"回答错误,二八十六，九乘九等于多少呢", cache=True)
        Error_flag = True
    message = ""
    while not message:
        if mic.chatting_mode:
            message = mic.activeListenWithButton()    #按键录入音频
        else:
            message = mic.activeListen(MUSIC=True) 
    if any(word in message for word in [u"81",u"八十一"]):
        mic.say(u"真棒，真是一个聪明的宝宝，我先退下了", cache=True)
    else:
        if not Error_flag:
            mic.say(u"哎呀，回答错误，九九八十一，要多练习一下", cache=True)
        else:
             mic.say(u"很遗憾，你一题也没有答对，要好好加油，回去多练习一下吧", cache=True)

def isValid(text):
    return any(word in text for word in [u"数学乐园",u"乘法",u"算术"])