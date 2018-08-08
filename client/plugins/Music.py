# -*- coding: utf-8-*-
'''
    音乐播放插件
'''
import os
import sys
import subprocess
import logging
import random
import re

try:
    reload         # Python 2
except NameError:  # Python 3
    from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')

# Standrd module stuff
WORDS = ["YINYUE"]
SLUG = "music"

def handle(text,mic,profile,wxbot=None, pixels=None, oled=None):
    logger = logging.getLogger(__name__)
    try:
        if any(word in text for word in [u'听歌',u'听儿歌',u'讲故事',u'听故事','故事',u'儿歌']):
            local_path = '/home/pi/Music'
            if 'local_path' in profile[SLUG]:
                local_path = profile[SLUG]['local_path']
            playlist = Get_LocalMusic(local_path)
            song = random.choice(playlist)
            mic.say('即将为你播放,%s' % song['song_name'], cache=True)
            play(song)
        elif any(word in text for word in [u'不听了',u'关闭音乐']):
            Del_Thread("play")
            mic.say(u'已关闭音乐', cache=True)
            
    except Exception as e:
        logger.error(e)
    


def Get_LocalMusic(local_path):
    ''' 获取本地播放列表 '''

    playlist = []
    for(dirpath,dirnames,filenames) in os.walk(local_path):
        for filename in filenames:
            try:
                # only mp3/wav accept
                if os.path.splitext(filename)[1] == ".mp3" or os.path.splitext(filename)[1] == ".wav":
                    # read mp3 properties and add to the playlist
                    music_path = os.path.join(dirpath,filename)
                    #print(music_path)
                    music_info = {}
                    music_info.setdefault("song_name",os.path.splitext(filename)[0])
                    music_info.setdefault("play_path",music_path)
                    playlist.append(music_info)
            except Exception as e:
                pass
        break
    #使本机音乐播放列表随机化
    random.shuffle(playlist)
    return playlist

def play(song):
    ''' 播放歌曲 '''
    Del_Thread("paly")
    subprocess.Popen("nohup play %s &" % song['play_path'],shell=True)

def Del_Thread(thread_name):
    ''' 删除线程的函数 '''
    res = subprocess.Popen("ps -ef|grep %s|grep -v grep" % thread_name,stdout=subprocess.PIPE,shell=True)
    thread_line = res.stdout.readlines()
    for line in thread_line:
        if re.search(thread_name,line):
            thread_pid = line.split()[1]
            subprocess.Popen("sudo kill -9 %d" % int(thread_pid),shell=True)


def isValid(text):
    ''' 匹配有效性查询 '''
    return any(word in text for word in [u'听歌',u'听儿歌',
                u'讲故事',u'听故事','故事',u'儿歌',u'不听了',u'关闭音乐'])