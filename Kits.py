# -*- coding: utf-8 -*-
import json
import os
import Constant

class Kits:
    def __init__(self):
        self.cookies = []
        self.tag = []

    def cookies(self):
        with open(Constant.PATH + 'cookies.txt', 'r') as file:       #获取cookies文件，否则无法下载18X文件，请确保已开启敏感内容选项
            self.cookies = json.load(file)                           #会自动创建cookies.txt文件
        return self.cookies

    def get_artist_name(self):
        with open(Constant.PATH + 'artists.txt','r') as file:            #先自动创建artist.txt文件
            self.tag = file.readline()
        return self.tag

    def get_artist_name_lenth(self):
        with open(Constant.PATH + 'artists.txt','r') as file:            #先自动创建artist.txt文件
            self.tag = file.readline()
        return len(self.tag)

    def dir_created(self):
        if not os.path.exists(Constant.PATH + self.tag):
            print('dir created')
            os.mkdir(Constant.PATH + self.tag)
        return Constant.PATH + self.tag + '\\'
