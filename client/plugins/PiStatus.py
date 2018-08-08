# -*- coding: utf-8-*-
'''
    树莓派状态查询插件
'''
import sys
import os
import subprocess
import logging
import time

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')

# Standard module stuff
WORDS = ['ZHUANGTAI']
SULG = "pi_status"

def GetCPUtemperature():
    '''
    获取CPU温度
    返回浮点数
    '''
    result = 0.0
    try:
        tempfile = open("/sys/class/thermal/thermal_zone0/temp")
        res = tempfile.read()
        result = float(res) / 1000
    except Exception as e:
        pass
    
    return result

def GetRAMinfo():
    '''
     获取RAM信息
    '''
    res = subprocess.Popen("free -h",stdout=subprocess.PIPE,shell=True)
    p = res.stdout.readlines()
    i = 0
    for line in p:
        i = i+1
        if i == 2:
            return (line.split()[1:4])

def GetDiskSpace():
    ''' 获取磁盘信息 '''
    res = subprocess.Popen("df -h /",stdout=subprocess.PIPE,shell=True)
    p = res.stdout.readlines()
    i = 0
    for line in p:
        i = i+1
        if i == 2:
            return (line.split()[1:5])

def GetIPAddress():
    '''
    获取当前IP地址
    '''
    res = subprocess.Popen("hostname -I",stdout=subprocess.PIPE,shell=True)
    p = res.stdout.readlines()
    return p

def handle(text,mic,profile,wxbot=None,pixels=None,oled=None):
    logger = logging.getLogger(__name__)
    try:
        Ram_result = GetRAMinfo()
        Disk_result = GetDiskSpace()
        IP_result = GetIPAddress()
        text1 = "sys_info"
        text2 = ("Mem: tol:%s used:%s" % (Ram_result[0],Ram_result[1]) )
        text3 = ("SD: tol:%s used:%s" % (Disk_result[0],Disk_result[1]) )
        text4 = ("IP: %s" % IP_result[0])
        if oled != None:
            oled.sys_info(text1,text2,text3,text4)
            mic.say(u'显示5秒后退出', cache=True)
            time.sleep(5)
        else:
            mic.say(u'没有找到可用的显示设备', cache=True)
    except Exception as e:
        logger.error(e)
        mic.say(u'抱歉，我没有获取到树莓派状态', cache=True)

def isValid(text):
    return any(word in text for word in [u"树莓派状态", u"运行状态"])




        

