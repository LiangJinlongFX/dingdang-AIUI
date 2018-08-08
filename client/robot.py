# -*- coding: utf-8-*-
'''
	智能对话机器人实现
	包含:
		AIUI
		图灵机器人
		小影机器人
	建议使用AIUI
'''
from __future__ import print_function
from __future__ import absolute_import
import requests
import json
import logging
import hashlib
import base64
import urllib2
import time
from uuid import getnode as get_mac
from .app_utils import sendToUser, create_reminder
from abc import ABCMeta, abstractmethod

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class AbstractRobot(object):
	"""docstring for AbstractRobot"""
	__metaclass__ = ABCMeta

	@classmethod
	def get_instance(cls,mic,profile,wxbot=None):
		'''获取机器人实例'''
		instance = cls(mic,profile,wxbot)
		cls.mic = mic
		cls.wxbot = wxbot
		return instance

	def __init__(self,**kwargs):
		#创建模块日志记录器
		self._logger = logging.getLogger(__name__)

	@abstractmethod
	def chat(self,texts):
		pass

class AIUIRobot(AbstractRobot):
	"""docstring for AIUIRobot"""
	SLUG = "AIUI"
	
	def __init__(self,mic,profile,wxbot=None):
		super(self.__class__, self).__init__()	#继承AbstractRobot
		self.mic = mic
		self.profile = profile
		self.wxbot = wxbot
		self.aiui_url = "http://openapi.xfyun.cn/v2/aiui"
		self.appid = self.get_appid()
		self.api_key = self.get_key()	#获取AIUI API信息
		self.auth_id = self.get_authid()
	
	def get_appid(self):
		if 'AIUI' in self.profile:
			if 'appid' in self.profile['AIUI']:
				appid = \
					self.profile['AIUI']['appid']
		return appid
	
	def get_key(self):
		if 'AIUI' in self.profile:
			if 'api_key' in self.profile['AIUI']:
				api_key = \
					self.profile['AIUI']['api_key']
		return api_key

	def get_authid(self):
		if 'AIUI' in self.profile:
			if 'auth_id' in self.profile['AIUI']:
				auth_id = \
					self.profile['AIUI']['auth_id']
		return auth_id

	def chat(self,texts):
		'''
		使用AIUI聊天
		'''
		answer,data_flag,data_body = self.Conversation(texts) #传入对话参数
		if answer == None:
			self.mic.say(u"抱歉,我的大脑短路了，请稍后再试试",cache=True)
		else:
			self.mic.say(answer)
			#self._logger.debug("附加的数据:"+data_body['playUrl'])

	def Conversation(self,text):
		'''
		AIUI会话请求函数
		'''
		Param = {
			"scene":"main",			#情景模式
			"auth_id":self.auth_id,		#用户ID
			"data_type":"text",		#数据类型	文本：text  音频：audio
			"result_level":"plain"	#结果级别
		}
		# 配置参数编码为base64字符串，过程：字典→明文字符串→utf8编码→base64(bytes)→base64字符串
		Param_str = json.dumps(Param)    #得到明文字符串
		Param_utf8 = Param_str.encode('utf8')    #得到utf8编码(bytes类型)
		Param_b64 = base64.b64encode(Param_utf8)    #得到base64编码(bytes类型)
		Param_b64str = Param_b64.decode('utf8')    #得到base64字符串

		# 构造HTTP请求的头部
		time_now = str(int(time.time()))
		checksum = (self.api_key + time_now + Param_b64str).encode('utf8')
		checksum_md5 = hashlib.md5(checksum).hexdigest()
		header = {
    		"X-Appid": self.appid,
    		"X-CurTime": time_now,
    		"X-Param": Param_b64str,
    		"X-CheckSum": checksum_md5
		}
		#构造HTTP 请求body
		Body_utf8 = text.encode('utf8')    #得到utf8编码(bytes类型)
		Body_b64 = base64.b64encode(Body_utf8)    #得到base64编码(bytes类型)
		Body_data = Body_b64.decode('utf8')    #得到base64字符串
		#发送请求
		try:
			req = urllib2.Request(self.aiui_url, data=text.encode('utf8'), headers=header)
		except requests.exceptions.ConnectionError:
			self._logger.debug("连接失败...")
		try:
			response = urllib2.urlopen(req)
		except:
			self._logger.debug("请求失败")
			return None,None,None
		#处理响应数据
		#self._logger.debug("请求响应状态码："+response.status)

		return self.Deal_ResData(response)


	def Deal_ResData(self,response):
		'''
		处理响应数据的方法
		'''
		data_flag = False 	#是否有附加数据 无:0  有:1
		data_body = {}		#创建附加数据的字典
		json_data = json.loads(response.read().decode('utf8'))
		#如果是非零的错误码,直接返回
		self._logger.debug("对话响应状态码："+str(json_data['code']))
		if json_data['code'] != '0':
			res_data = "响应失败"
			return res_data,data_flag,data_body
		json_str = json_data['data']
		json_str1 = json_str[0]['intent']
		#检查是否有智能答复的键值
		if 'answer' in json_str1.keys():
			answer_text = json_str1['answer']['text']	#获取AIUI答复的文本
			if 'data' in json_str1.keys():	#如果有附加的数据
				#如果有附加的数据
				try:
					if json_str1['data']['result'] != []:
						data_flag = True	#附加数据标志
						#获取返回结果的第一个
						answer_data = json_str1['data']['result'][0]
						if 'playUrl' in answer_data.keys():		#判断是否有播放连接
							data_body.setdefault("playUrl",answer_data['playUrl'])
							self._logger.debug("playUrl"+str(answer_data['playUrl']))
						elif 'url' in answer_data.keys():
							data_body.setdefault("playUrl",answer_data['url'])
							self._logger.debug("url"+str(answer_data['url']))
						else:
							data_flag = False
				except Exception:
					self._logger.debug("获取附加数据异常!")
			res_data = answer_text
		else:	#没有相应的场景将回显
			res_data = json_str1['text']

		#去除诗词中存在的[k3]-[k0]符号
		if '[k3]' in res_data:
			res_data = res_data.replace('[k3]','')
			if '[k0]' in res_data:
				res_data = res_data.replace('[k0]','')

		return res_data,data_flag,data_body

def get_robot_by_slug(slug):
    """
    Returns:
        A robot implementation available on the current platform
    """
    if not slug or type(slug) is not str:
    	raise TypeError("Invalid slug '%s'", slug)

    selected_robots = filter(lambda robot: hasattr(robot, "SLUG") and
		robot.SLUG == slug, get_robots())

    if len(selected_robots) == 0:
    	raise ValueError("No robot found for slug '%s'" % slug)
    else:
    	if len(selected_robots) > 1:
    		print("WARNING: Multiple robots found for slug '%s'. " +
				"This is most certainly a bug." % slug)
    	robot = selected_robots[0]
    	return robot


def get_robots():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [robot for robot in
            list(get_subclasses(AbstractRobot))
            if hasattr(robot, 'SLUG') and robot.SLUG]
		
		