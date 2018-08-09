#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	用于叮当机器人的OLED显示驱动模块
'''
from queue import Queue
from luma.core.interface.serial import i2c,spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.sprite_system import framerate_regulator
from PIL import ImageOps
from PIL import ImageFont
from PIL import Image, ImageSequence
import os
import time
import threading
import random
from client import dingdangpath
try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class OLED():
	''' OLED显示驱动类 '''
	def __init__(self):
		self.next = threading.Event()
		self.queue = Queue()
		self.thread = threading.Thread(target=self._run)
		self.thread.daemon = True
		self.thread.start()
    
	def wakeup(self):
		''' 用于唤醒动画或启动动画 '''
		a = ['1','2','3']
		b = random.sample(a,1)
		name = "welcome" + str(b[0]) + ".gif"
		image_path = dingdangpath.data('images',name)
		def f():
			self._DisplayGIFOnce(image_path=image_path)

		self.next.set()
		self.queue.put(f)

	def listen(self):
		''' 用于正在监听的动画 '''
		image_path = dingdangpath.data('images','free6.gif')
		def f():
			self._DisplayGIF(image_path=image_path)

		self.next.set()
		self.queue.put(f)

	def speak(self):
		''' 用于正在说话的动画 '''
		image_path = dingdangpath.data('images','free4.gif')
		def f():
			self._DisplayGIF(image_path=image_path)

		self.next.set()
		self.queue.put(f)
	
	def sys_info(self,text1,text2,text3,text4):
		''' 用于显示系统信息文本 '''
		font_path = dingdangpath.data('fonts','C&C Red Alert [INET].ttf')
		def f():
			self._DisplayText(font_path=font_path,text1=text1,text2=text2,text3=text3,text4=text4)

		self.next.set()
		self.queue.put(f)

	def show_QR(self,image_path):
		''' 显示微信登录二维码 '''
		def f():
			self._DisplayPNG(image_path)

		self.next.set()
		self.queue.put(f)

	def off(self):
		self.next.set()
		self.queue.put(self._off)

	def _run(self):
		while True:
			func = self.queue.get()
			func()

	def _DisplayText(self,font_path, text1, text2=None, text3=None, text4=None, size=12):
		'''
		显示多行文本
		最少显示一行,最多显示四行
		非特殊情况,请勿修改字体大小
		'''
		self.next.clear()
		serial = i2c(port=1,address=0x3c)
		device = ssd1306(serial) #挂载设备
		Text_font = ImageFont.truetype(font_path,size)	#设置文本字体
		while not self.next.is_set():
			with canvas(device) as draw:
				draw.text((0,0),text1,font=Text_font,fill="white")
				if text2 != None:
					draw.text((0,14),text2,font=Text_font,fill="white")
					if text3 != None:
						draw.text((0,26),text3,font=Text_font,fill="white")
						if text4 != None:
							draw.text((0,38),text4,font=Text_font,fill="white")
	

	def _DisplayGIF(self,image_path):
		''' 显示GIF动图 '''
		self.next.clear()
		serial = i2c(port=1,address=0x3c)
		device = ssd1306(serial) #挂载设备
		regulator = framerate_regulator(fps=30)
		ImageFile = Image.open(image_path) # Open a picture
		size = [min(*device.size)] * 2
		posn = ((device.width - size[0]) // 2, device.height - size[1])
		while not self.next.is_set():
			for frame in ImageSequence.Iterator(ImageFile):
				with regulator:
					background = Image.new('RGB',device.size,'black')
					background.paste(frame.resize(size,resample=Image.LANCZOS),posn)
					background = background.convert(device.mode)
					device.display(background)

	def _DisplayGIFOnce(self,image_path):
		''' 显示GIF动图 '''
		self.next.clear()
		serial = i2c(port=1,address=0x3c)
		device = ssd1306(serial) #挂载设备
		regulator = framerate_regulator(fps=30)
		ImageFile = Image.open(image_path) # Open a picture
		size = [min(*device.size)] * 2
		posn = ((device.width - size[0]) // 2, device.height - size[1])
		for frame in ImageSequence.Iterator(ImageFile):
			with regulator:
				background = Image.new('RGB',device.size,'black')
				background.paste(frame.resize(size,resample=Image.LANCZOS),posn)
				background = background.convert(device.mode)
				device.display(background)

	def _DisplayPNG(self,image_path):
		''' 显示PNG静态图 '''
		self.next.clear()
		serial = i2c(port=1,address=0x3c)
		device = ssd1306(serial)	#挂载设备
		ImageFile = Image.open(image_path)	#打开图像对象
		size = [min(*device.size)] * 2
		posn = ((device.width - size[0]) // 2, device.height - size[1])		
		background = Image.new("RGBA", device.size, "black")	#创建背景图像
		background.paste(ImageFile.resize(size),posn)
		background = background.convert(device.mode)	#将图像转换为单色模式
		while not self.next.is_set():
			device.display(background)
	
	def _off(self):
		self.next.clear()
		serial = i2c(port=1,address=0x3c)
		device = ssd1306(serial)	#挂载设备
		device.cleanup()



if __name__ == '__main__':
	t = OLED()
	while True:
		t.wakeup()
		t.listen()
		time.sleep(10)
		t.off()
