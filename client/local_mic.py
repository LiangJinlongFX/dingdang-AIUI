# -*- coding: utf-8-*-
"""
A drop-in replacement for the Mic class that allows for all I/O to occur
over the terminal. Useful for debugging. Unlike with the typical Mic
implementation, Dingdang is always active listening with local_mic.
"""
from __future__ import print_function
import time
import pyaudio
from . import player
try:
	raw_input	#python2
except NameError:
	raw_input = input

class Mic():
	"""docstring for Mic"""
	prev = None
	def __init__(self, speaker,passive_stt_engine,active_stt_engine):
		self.speaker = speaker	#获取发声方法
		self._audio = pyaudio.PyAudio()
		self.sound = player.get_sound_manager(self._audio)	#获取声音播放方法
		self.stop_passive =False
		self.skip_passive =False
		self.chatting_mode =False
        #音乐播放相关定义
		self.music = player.get_music_manager() #添加音乐播放实例
		self.music_list = []    #音乐播放列表
		self.music_idx = -1 #当前播放的音乐序号
		self.music_playing = False  #当前是否在播放音乐
		return
	
	#本地调试默认已主动唤醒
	def passiveListen(self, PERSONA):
		return True, "DINGDANG"

    #主动倾听对外识别方法
	def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True,MUSIC=False):
		return [self.activeListen(THRESHOLD=THRESHOLD, LISTEN=LISTEN,MUSIC=MUSIC)]

	def activeListenWithButton(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
		if not LISTEN:
			return self.prev
		input = raw_input("YOU: ")
		return input

		
	#用文本输入替代主动语音识别
	def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
		if not LISTEN:
			return self.prev
		input = raw_input("YOU: ")
		self.prev = input
		print(input)
		return input

    #机器人回复方式
	def say(self, phrase,
		OPTIONS=" -vdefault+m3 -p 40 -s 160 --stdout > say.wav",cache=False):
		print("DINGDANG: %s" % phrase)
		self.stop_passive = True
        # incase calling say() method which
        # have not implement cache feature yet.
        # the count of args should be 3.
		if self.speaker.say.__code__.co_argcount > 2:
			self.speaker.say(phrase, cache)
		else:
			self.speaker.say(phrase)
		time.sleep(1)  # 避免叮当说话时误唤醒
		self.stop_passive = False
	
	def play(self, src):
        # play a voice
		self.sound.play_block(src)

	def play_no_block(self, src):
		self.sound.play(src)
	
	def music_play(self,src):
		self.music.play(src)