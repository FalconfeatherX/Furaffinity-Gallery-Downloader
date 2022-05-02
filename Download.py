import sys

from pip._internal.utils import logging

from Kits import Kits
import time
from multiprocessing import Pool, Manager
import os
import requests
from itertools import repeat

logger = logging.getLogger('print')

out_put = sys.stdout


def processing_bar(args):
    now, total = args
    while True:
        sys.stdout.write(u'\rProcessing percent %d / %d:' % (len(now), total))
        sys.stdout.flush()
        if len(now) == total:
            return
        time.sleep(0.5)


class Download:
    version = 1.0

    def __init__(self):
        self.artist_length = Kits.get_owner_name_length(Kits)
        self.path = Kits.dir_created(Kits)

    @staticmethod
    def connect(url):
        return requests.session().get(url, timeout=15)

    def single_download(self, args):
        print("running")
        """
        参数：args：携带单个网址和一个用于插入下载成功文件的列表
        功能：执行单次下载
        模块解释：除了使用文件创建和requests请求之外，还有一些问题的对应处理：
                网络波动引起的文件下载不完整（使用响应头中的信息判断大小并和本地文件比较，不同则视为下载失败）
                文件为图片文件之外的，通过content-type判断类型或检测文件名是否合法，采取不同的名称截断策略
        """
        time.sleep(0.5)
        result, list_share = args
        logger.debug(result)

        download_link = result[0]
        artist_name_length = len(result[1])
        start_line = artist_name_length + 43
        start_line_for_long = artist_name_length + 60

        size = 0  # 确保size永远有定义

        try:
            source = Download.connect(download_link)
            file_type = source.headers["content-type"]
        except requests.exceptions.RequestException:
            logger.warning("Timeout")
            return
        except:
            logger.warning("unexpected error" + download_link)
            return

        if not source.status_code == 200:
            logger.warning("Connect error %s" % download_link)
            return

        if '/' not in download_link[start_line:]:
            file_path = self.path + '%s' % (download_link[start_line:])
            size = source.headers["Content-Length"]  # 目标文件大小，对mp3似乎是无效的，可能响应头没有CL吧

        else:
            file_path = self.path + '%s' % (download_link[start_line_for_long:])
            list_share.append(download_link)

        with open(file_path, 'wb') as dest:
            dest.write(source.content)
        if file_type == "text/plain":
            return

        file_size = os.path.getsize(file_path)  # 实际文件大小

        if file_size == int(size) and file_size != 0:
            list_share.append(download_link)
            # self.db.database_downloaded(results)

        else:  # 大小不匹配，则重新下载
            logger.warning("Size difference! goal:%d Downloaded:%d url:%s" % (int(size), file_size, download_link))

    def multi_download(self, list_result):
        """参数：list_result：携带图片网址列表
           功能：多进程下载
           模块返回：list_share: 下载成功的网址
        """
        # processing = Manager().list()
        list_share = Manager().list()
        list_total = len(list_result)
        # [(url1,list_share),(url2,list_share),]
        data = zip(list_result, repeat(list_share))
        logger.info('Amount of to-be downloaded urls: ' + str(list_total))
        # vice_Processing = Process(target = self.processing_bar,args = ((list_share,list_total),))
        # vice_Processing.start()
        workers = Pool(8)
        workers.map(self.single_download, data)
        workers.close()
        workers.join()
        return list_share


if __name__ == "__main__":
    downloader = Download()
    list_result = [
        ('http://d.furaffinity.net/art/falconfeather/1623253160/1623253160.falconfeather_整楼模型.jpg', 'falconfeather'), (
            'http://d.furaffinity.net/art/falconfeather/1623257823/1623257823.falconfeather_untitled.jpg',
            'falconfeather')]
    downloader.multi_download(list_result)
