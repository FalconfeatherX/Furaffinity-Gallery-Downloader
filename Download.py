from Kits import Kits
import time
from multiprocessing import Pool,Process,Manager
import os
import requests
from itertools import repeat

class Download:
    version = 1.0
    def __init__(self):
        self.artist_lenth = Kits.get_artist_name_lenth(Kits)
        self.path         = Kits.dir_created(Kits)


    @staticmethod
    def connect(url):
        return requests.session().get(url,timeout = 15)

    def single_download(self,args):
        time.sleep(0.5)
        results,list_share = args
        print(results)
        AL = self.artist_lenth
        Startline = AL + 43#43
        Startline_for_long = AL + 60
        size = 0 #确保size永远有定义

        try:
            source = Download.connect(results)
            file_type = source.headers["content-type"]
        except requests.exceptions.RequestException:
            print("timeout")
            return

        if not source.status_code == 200:
            print("connect error %s"%(results))
            return

        if not '/' in results[Startline:]:
            file_path = self.path + '%s'%(results[Startline:])
            size   = source.headers["Content-Length"]           #目标文件大小

        else:
            file_path = self.path + '%s'%(results[Startline_for_long:])
            list_share.append(results)

        with open(file_path, 'wb') as dest:
            dest.write(source.content)
        if file_type == "text/plain":
            return

        file_size = os.path.getsize(file_path)              #实际文件大小

        if file_size == int(size) and file_size != 0:
            list_share.append(results)
        else:                                               #大小不匹配，则重新下载
            print("size difference! goal:%d downloaded:%d url:%s"%(int(size),file_size,results))


    def multi_download(self,list_result):
        list_share = Manager().list()
        list_total = len(list_result)
        data = zip(list_result,repeat(list_share))
        print(list(list_result))
        #vice_Processing = Process(target = Processingbar,args = ((list_share,len(list_total),))
        workers = Pool(8)
        #vice_Processing.start()
        workers.map(self.single_download,data)
        workers.close()
        workers.join()
        return list_share
