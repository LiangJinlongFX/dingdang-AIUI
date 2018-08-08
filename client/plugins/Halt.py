# -*- coding: utf-8-*-
'''
    系统相关的控制插件
    功能包括:
        关闭系统
        重启系统
        增大音量
        减少音量
'''
import logging
import sys
import time
import subprocess

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')


WORDS = ["GUANJI"]
SLUG = "halt"

def handle(text,mic,profile,wxbot=None, pixels=None, oled=None):
    logger = logging.getLogger(__name__)
    try:
        if any(word in text for word in [u'关机',u'关闭系统']):
            mic.say('将要关闭系统，请在滴一声后进行确认，授权相关操作', cache=True)
            input = mic.activeListen(MUSIC=True)
            if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
                mic.say('授权成功，开始进行相关操作', cache=True)
                subprocess.Popen("sudo shutdown -t 5 now",shell=True)
                return
            else:
                mic.say('授权失败，操作已取消，请重新尝试', cache=True)
        elif any(word in text for word in [u'重启',u'重启系统']):
            mic.say('将要重启系统，请在滴一声后进行确认，授权相关操作', cache=True)
            input = mic.activeListen(MUSIC=True)
            if input is not None and any(word in input for word in [u"确认", u"好", u"是", u"OK"]):
                mic.say('授权成功，开始进行相关操作', cache=True)
                subprocess.Popen("sudo reboot",shell=True)
                return
            else:
                mic.say('授权失败，操作已取消，请重新尝试', cache=True)
        elif any(word in text for word in [u'大声点',u'增大音量']):
            subprocess.Popen("amixer -c 0 set PCM 10dB+",shell=True)
            mic.say('好的', cache=True)
        elif any(word in text for word in [u'小声点',u'减少音量']):
            subprocess.Popen("amixer -c 0 set PCM 10dB-",shell=True)
            mic.say('好的', cache=True)
    except Exception as e:
        logger.error(e)
        mic.say('设置失败', cache=True)



def isValid(text):
    return any(word in text for word in [u'关机',u'关闭系统',u'重启',u'重启系统','大声点',u'小声点'])