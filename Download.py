# -*- coding: utf-8 -*-
from Kits import Kits
import time
from multiprocessing import Pool,Process,Manager
import requests
from itertools import repeat
import Constant

class Download:
    version = 1.0
    def __init__(self):
        self.artist_lenth = Kits.get_artist_name_lenth(Kits)
        self.path         = Kits.dir_created(Kits)


    @staticmethod
    def connect(url):
        return requests.Session().get(url,timeout = 30)

    def single_download(self,args):
        results,list_share = args
        print(results)
        AL = self.artist_lenth
        Startline = AL + 43

        if not results[Startline:]:
            print('Name Error')
            return False

        try:
            source = Download.connect(results)
        except:
            print('Connected error' + results)

        try:
            with open(self.path + '%s'%(results[Startline:]), 'wb') as dest:
                dest.write(source.content)
                if source:
                    list_share.append(results)
                    time.sleep(Constant.INTERVAL)
        except IOError as e:
            print('IOError:',e)

    def multi_download(self,list_result):
        list_share = Manager().list()
        list_total = len(list_result)
        data = zip(list_result,repeat(list_share))
        #vice_Processing = Process(target = Processingbar,args = ((list_share,len(list_total),))
        workers = Pool(Constant.THREADS)
        #vice_Processing.start()
        workers.map(self.single_download,data)
        workers.close()
        workers.join()
        return list_share
