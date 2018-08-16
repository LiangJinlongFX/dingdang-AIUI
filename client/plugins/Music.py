# -*- coding: utf-8-*-
'''
    音乐播放插件
'''
import os
import sys
import subprocess
import requests
import logging
import random
import re
from client import config

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
        if any(word in text for word in [u'听歌',u'听儿歌',u'听音乐']):
            if mic.music_list == []:
                '''
                # 判断是否使能网络FM播放
                if config.get("BaiduFM",False):
                    try:
                        baiduFM = BaiduFM()
                        channel_id = config.get('channel_id',11)
                        web_song_list = baiduFM.Get_song_list(u'中国风') #获取网络频道歌单
                        mic.music_list = []
                        for x in range(0,len(web_song_list)):
                            music_info = baiduFM.Get_song_url(web_song_list,x)
                            mic.music_list.append(music_info)
                    except Exception as e:
                        logger.debug(e)
                '''   
                local_path = '/home/pi/Music'
                if 'local_path' in profile[SLUG]:
                    local_path = profile[SLUG]['local_path']
                mic.music_list = Get_LocalMusic(local_path)
                if mic.music_list == []:
                    mic.say('获取音乐列表失败', cache=True)
            if not mic.music_playing:
                mic.music_idx = 0
                play(mic)
        elif any(word in text for word in [u'上一首',u'换歌',u'下一首']):
            if any(word in text for word in [u'上一首']):
                mic.music_idx = mic.music_idx - 1
                play(mic)
            elif any(word in text for word in [u'换歌',u'下一首']):
                mic.music_idx = mic.music_idx + 1
                play(mic)
        elif any(word in text for word in [u'不听了',u'关闭音乐']):
            Del_Thread("play")
            mic.music_playing = False
            mic.say(u'已关闭音乐', cache=True)
            
    except Exception as e:
        logger.error(e)
    


def Get_LocalMusic(local_path):
    """ 获取本地播放列表 """
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

def play(mic):
    ''' 播放歌曲 '''
    if mic.music_playing:
        Del_Thread("play")   #终止当前播放的歌曲
    if mic.music_idx == -1 or mic.music_idx > len(mic.music_list):
        mic.music_idx = 0
    mic.say('即将为你播放,%s' % mic.music_list[mic.music_idx]['song_name'], cache=True)
    subprocess.Popen("play %s &" % mic.music_list[mic.music_idx]['play_path'],shell=True)
    mic.music_playing = True

def Del_Thread(thread_name):
    ''' 删除线程的函数 '''
    res = subprocess.Popen("ps -ef|grep %s|grep -v grep" % thread_name,stdout=subprocess.PIPE,shell=True)
    thread_line = res.stdout.readlines()
    for line in thread_line:
        if re.search(thread_name,line):
            thread_pid = line.split()[1]
            subprocess.Popen("sudo kill -9 %d" % int(thread_pid),shell=True)


class BaiduFM:
    """
    百度FM在线播放音乐
    """
    def __init__(self):
        self.page_url = 'http://fm.baidu.com/dev/api/?tn=channellist'
        self.channel_list = []
        self.channel_name = None
        self.channel_id = None

    def Get_channel_list(self):
        """ 获取频道列表 """
        try:
            r = requests.get(self.page_url)
        except Exception as e:
            return []
        
        content = r.json()
        channel_list = content['channel_list']

        return channel_list

    def Get_song_list(self,channel_name):
        """
        获取指定频道的歌单
        """
        self.channel_list = self.Get_channel_list()
        if self.channel_list == []: 
            return []
        for i in self.channel_list:
            if i['channel_name'] == channel_name:
                channel_id = i['channel_id']
        channel_url = 'http://fm.baidu.com/dev/api/' +\
            '?tn=playlist&format=json&id=%s' % channel_id
        try:
            r = requests.get(channel_url)
        except Exception as e:
            return []
        
        content = r.json()
        song_id_list = content['list']

        return song_id_list

    def Get_song_url(self,song_id_list,idx):
        """
        获取歌曲URL
        """
        song_url = "http://music.baidu.com/data/music/fmlink?type=mp3&rate=320&songIds=%s" % song_id_list[idx]['id']
        song_info = {}
        try:
            r = requests.get(song_url)
        except Exception:
            return {}
        
        content = r.json()
        song_info.setdefault("song_name",content['data']['songList'][0]['songName'])
        song_info.setdefault("play_path",content['data']['songList'][0]['songLink'])

        return song_info


def isValid(text):
    ''' 匹配有效性查询 '''
    return any(word in text for word in [u'听歌',u'听儿歌',
                u'上一首',u'换歌',u'下一首',u'关闭音乐','不听了'])