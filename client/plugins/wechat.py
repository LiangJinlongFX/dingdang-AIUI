# -*- coding: utf-8-*-
"""
    微信助手插件
    功能:
        登录微信(若启动时没有登录微信或者微信线程意外终止的话)
        登出微信
        发送录音给微信账号文件传输助手
"""

import os
import sys
import logging
from app_utils import sendToUser

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')

WORDS = [u"WEIXIN"]
SLUG = u"weixin"

def handle(text, mic, profile, wxbot=None, pixels=None, oled=None):
    #logger = logging.getLogger(__name__)
    dest_file = '/home/pi/out.mp3'
    if any(word in text for word in [u'微信留言']):
        if wxbot:
            mic.say('请在滴一声后开始录音', cache=True)
            if sendToUser(profile, wxbot, u"这是刚刚的语音留言", "", [dest_file], []):
                mic.say('发送成功', cache=True)
            else:
                mic.say('发送失败', cache=True)


def isValid(text):
    ''' 匹配有效性查询 '''
    return any(word in text for word in [u'微信留言'])