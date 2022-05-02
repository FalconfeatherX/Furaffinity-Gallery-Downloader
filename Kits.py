# -*- coding: utf-8 -*-
import json
import os

from pip._internal.utils import logging

import Constant

logger = logging.getLogger('print')


class Kits:
    def __init__(self):
        self.cookies = []
        self.catalogue = {"fav": "_fav", "scraps": "_scraps"}
        self.tag = []

    def cookies(self):
        if not os.path.exists(Constant.PATH + 'cookies.txt'):
            with open(Constant.PATH + 'cookies.txt', 'a'):
                logger.info('cookies.txt created')
        try:
            with open(Constant.PATH + 'cookies.txt', 'r') as file:  # 获取cookies文件，否则无法下载X文件，请确保已开启敏感内容选项
                self.cookies = json.load(file)
        except:
            logger.info('Cookies not found')
        return self.cookies

    def get_owner_name(self):
        if not os.path.exists(Constant.PATH + 'owner.txt'):
            with open(Constant.PATH + 'owner.txt', 'a'):
                logger.info('owner.txt created')
        with open(Constant.PATH + 'owner.txt', 'r') as file:
            self.tag = file.readline()
        return self.tag

    def get_owner_name_length(self):
        with open(Constant.PATH + 'owner.txt', 'r') as file:
            self.tag = file.readline()
        return len(self.tag)

    def dir_created(self):
        catalogue = {"fav": "_fav", "scraps": "_scraps"}
        if Constant.FAVS:
            self.tag += catalogue["fav"]
        elif Constant.SCRAPS:
            self.tag += catalogue["scraps"]
        if not os.path.exists(Constant.PATH + self.tag):
            logger.info('dir created')
            os.mkdir(Constant.PATH + self.tag)
        return Constant.PATH + self.tag + '/'
