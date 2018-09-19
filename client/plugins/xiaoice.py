# -*- coding: utf-8-*-
"""
    与微信公众号的小冰机器人聊天的插件
"""
import sys
import logging

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')

WORDS = [u"XIAOBING"]
SLUG = "xiaoice"

def handle(text, mic, profile, wxbot=None, pixels=None, oled=None):
    logger = logging.getLogger(__name__)
    if wxbot == None:
        mic.say(u"你还没有登录微信呢", cache=True)
        return
    xiaoice_uid = wxbot.get_user_id(u'小冰')
    if not xiaoice_uid:
        mic.say(u"小冰不见了", cache=True)
        return
    mic.say(u"我是人见人爱的小冰，快来和我聊聊天吧", cache=True)
    while True:
        input = mic.activeListenWithButton()
        if input:
            if any(word in input for word in [u"退出",u"不聊"]):
                break
            try:
                if wxbot.send_msg_by_uid(input,xiaoice_uid):
                    logger.debug("发送成功")
                else:
                    logger.debug("发送失败")
                    mic.say(u"哼,不理你", cache=True)
            except Exception as e:
                logger.error(e)
        else:
            mic.say(u"说啥呢", cache=True)
    mic.say(u"轻轻的我走了，正如我轻轻地来。我们下次再聊吧", cache=True)

def isValid(text):
    return any(word in text for word in [u"女神",u"小冰",u"小兵"])