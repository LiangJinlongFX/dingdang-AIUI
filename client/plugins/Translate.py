# -*- coding: utf-8 
"""
    有道翻译插件
    功能
        将要翻译的文本转换成英文并发声
"""

import logging
import json
import urllib
import time
import re
import requests
import hashlib
import random
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

SLUG = "youdao"
WORDS = ["FANYI"]


def handle(text, mic, profile, wxbot=None, pixels=None, oled=None):
    logger = logging.getLogger(__name__)
    if SLUG not in profile or \
        'appId' not in profile[SLUG] or\
        'appSecret' not in profile[SLUG]:
        mic.say('有道翻译插件配置有误，插件使用失败', cache=True)
        return
    #获取API的appid以及app_key 
    appId = profile[SLUG]['appId']
    appSecret = profile[SLUG]['appSecret']
    sentence = getSentence(text)
    logger.info('sentence: ' + sentence)
    if sentence:
        try:
            s = translate(appId,appSecret,sentence)
            if s:
                mic.say(sentence+"的翻译是" + s, cache=False)
            else:
                mic.say("翻译" + sentence +"失败，请稍后再试", cache=False)
        except Exception as e:
            logger.error(e)
            mic.say('抱歉, 我不知道怎么翻译' + sentence, cache=False)
    else:
       mic.say(u"没有听清楚 请重试", cache=True) 

def translate(app_id,app_secret,sentence):
    """ 访问有道翻译API以获取翻译的英文结果 """
    url = 'https://openapi.youdao.com/api'
    salt = random.randint(1,65536)
    sign = app_id + sentence + str(salt) + app_secret
    sign = sign.encode('utf8')
    sign = hashlib.md5(sign).hexdigest()
    Params = {
        'q' : sentence,
        'from' : 'auto',
        'to' : 'EN',
        'appKey' : app_id,
        'salt' : salt,
        'sign' : sign
	}
    r = requests.get(url,params=Params)
    if r.status_code != 200:
        return None
    json_data = json.loads(r.text,encoding='utf-8')
    try:
        translation = json_data['translation'][0]
    except Exception:
        return None
    return translation

def getSentence(text):
    """ 提取要翻译的内容 """
    pattern1 = re.compile("翻译.*?")
    pattern2 = re.compile(".*?的翻译")
    if re.match(pattern1, text) != None:
        sentence = text.replace("翻译", "")
    elif re.match(pattern2, text) != None:
        sentence = text.replace("的翻译", "")
    else:
        sentence = ""
    sentence = sentence.replace(",","")
    sentence = sentence.replace("，","")
    return sentence

def isValid(text):
    return u"翻译" in text