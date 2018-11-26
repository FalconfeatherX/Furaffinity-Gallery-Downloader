# -*- coding: utf-8 -*-
import json
import os
import Constant

class Kits:
    def __init__(self):
        self.cookies = []
        self.tag = []

    def cookies(self):
        if not os.path.exists(Constant.PATH + 'cookies.txt'):
            with open(Constant.PATH + 'cookies.txt','a'):
                print('cookies.txt created')
        try:
            with open(Constant.PATH + 'cookies.txt', 'r') as file:       #获取cookies文件，否则无法下载18X文件，请确保已开启敏感内容选项
                self.cookies = json.load(file)
        except:
            print('Please enter your cookies')
        return self.cookies

    def get_artist_name(self):
        if not os.path.exists(Constant.PATH + 'artist.txt'):
            with open(Constant.PATH + 'artist.txt','a'):
                print('artist.txt created')
        with open(Constant.PATH + 'artist.txt','r') as file:
            self.tag = file.readline()
        return self.tag

    def get_artist_name_lenth(self):
        with open(Constant.PATH + 'artist.txt','r') as file:            
            self.tag = file.readline()
        return len(self.tag)

    def dir_created(self):
        if not os.path.exists(Constant.PATH + self.tag):
            print('dir created')
            os.mkdir(Constant.PATH + self.tag)
        return Constant.PATH + self.tag + '\\'
