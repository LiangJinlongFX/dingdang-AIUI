# -*- coding: utf-8-*-
"""
    猜猜我是谁交互式问答插件
    功能:
        通过对职业的描述，让儿童回答出所描述的职业
"""

import os
import sys
import logging

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')


WORDS = [u"GUESS"]
SLUG = u"guess"

def handle(text, mic, profile, wxbot=None, pixels=None, oled=None):
    mic.say(u"小朋友，欢迎来到猜猜我是谁。我是神秘人我无处不在，认真听我说的提示，猜出我是谁", cache=True)
    mic.say(u"我工作的时候挥动指挥棒，知道我是谁了吗", cache=True)
    message = ""
    while not message:
        if mic.chatting_mode:
            message = mic.activeListenWithButton()    #按键录入音频
        else:
            message = mic.activeListen(MUSIC=True)
    if any(word in message for word in [u"指挥",u"指挥家"]):
        mic.say(u"真棒！一下子就猜对了，下次再找我玩吧", cache=True)
        return
    else:
        mic.say(u"给你一个提示，我的工作能看到各种乐器，这次知道我是谁了吗？", cache=True)
    message = ""
    while not message:
        if mic.chatting_mode:
            message = mic.activeListenWithButton()    #按键录入音频
        else:
            message = mic.activeListen(MUSIC=True)
    if any(word in message for word in [u"指挥",u"指挥家"]):
        mic.say(u"恭喜你，猜对了哦", cache=True)
        return
    else:
        mic.say(u"很遗憾，你还是没有猜对，答案是指挥家，下次再找我玩吧", cache=True)

def isValid(text):
    return any(word in text for word in [u"猜猜我是谁"])

