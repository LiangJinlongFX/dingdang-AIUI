# -*- coding: utf-8-*-
"""
    获取当前时间的功能插件
    减少对AIUI的依赖
    功能:
        获取当前的时间
"""
import datetime
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = [u"TIME", u"SHIJIAN", u"JIDIAN"]
SLUG = "time"

def handle(text, mic, profile, wxbot=None, pixels=None, oled=None):
    
    tz = getTimezone(profile)
    now = datetime.datetime.now(tz=tz)
    service = DateService()
    response = service.convertTime(now)
    if "AM" in response:
        response = u"上午" + response.replace("AM","")
    elif "PM" in response:
        response = u"下午" + response.replace("PM","")
    mic.say(u'现在时间是%s' % response, cache=False)

def isValid(text):
    return any(word in text for word in [u"时间", u"几点",u"多少点"])

