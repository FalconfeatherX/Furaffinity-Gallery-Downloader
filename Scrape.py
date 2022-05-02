import logging

from bs4 import BeautifulSoup
import re
import time
from Kits import Kits
from multiprocessing import Pool,Manager
from itertools import repeat
import Constant
import requests

logger = logging.getLogger('print')


def time_shifter(updateTime):
    no_12H_time = updateTime.replace('PM', '').replace('AM', '')
    times = time.strptime(no_12H_time, "%b %d, %Y %H:%M ")
    timestamp = int(time.mktime(times))
    if 'PM' in updateTime:
        timestamp += 43200  # 12小时
    return timestamp


class Scrape:
    def __init__(self):
        self.url = Constant.URL + 'gallery/'
        self.scraps = Constant.URL + 'scraps/'
        self.favs = Constant.URL + 'favorites/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/64.0.3282.186 Safari/537.36"}
        self.scraper = requests.session()
        self.data = Kits.cookies(Kits)
        self.tag = Kits.get_owner_name(Kits)
        self.page_list = []
        self.post_list = []

    def connect_urls(self, url):
        try:
            return self.scraper.get(url, headers=self.headers, cookies=self.data, timeout=15)
            logger.info(url)
        except:
            logger.warning('Connected error: %s' % url)
            return False

    def get_gallery_url(self):
        if Constant.SCRAPS:
            self.scraps = self.scraps + self.tag
            return self.scraps
        elif Constant.FAVS:
            self.favs = self.favs + self.tag
            return self.favs
        else:
            self.url = self.url + self.tag
            return self.url

    def get_post_url(self, single_url):
        self.post_list = []
        try:
            url_content = self.connect_urls(single_url).text
        except:
            logger.info('Reconnected: ')
            url_content = self.connect_urls(single_url).text
        compiler = re.compile(r'view/\d+/')
        result = compiler.findall(url_content)
        for transfers in result:
            self.post_list.append(transfers)
        self.post_list = set(self.post_list)
        self.post_list = list(self.post_list)

    def get_download_urls_and_table_stuffs(self, args):
        download_links, datum, error_list = args
        keyword = ''
        download_content = self.connect_urls(Constant.URL + download_links)
        if not download_content:
            error_list.append(download_links)
            return False

        else:
            download_content = download_content.text

        time.sleep(Constant.INTERVAL)
        try:
            soup = BeautifulSoup(download_content, 'lxml')
            compiler = re.compile(r'//d.furaffinity.net\S+[fgt3]')
            adults = soup.find('div', {'class': "rating"})
            tags = soup.find('section', {'class': "tags-mobile"})
            links = soup.find('div', {'class': "download"})  # fa日常会更改域名，要注意（旧域名还能用）
            name = soup.find('div', {'class': "submission-title"}).text.strip()
            times = soup.find('span', {'class': "popup_date"})["title"]
            artist = soup.find('div', {'class': "submission-id-sub-container"}).find('a').text
            links = compiler.findall(str(links))
        except:
            logger.warning("fatal error")
            return

        for link in links:
            dump_link = link
        adult = 1 if ' Adult' in str(adults) else 0  # 如果NFSW元素成立，置1，否则为0
        try:
            for i in tags.text.split():
                keyword = keyword + i + ' '  # 关键词爬取
        except:
            keyword = 'None'
        times = time_shifter(times)
        keywords = keyword.rstrip()
        link = dump_link
        name = name.replace('"', '\'')
        owner = self.tag

        nametup = (str(name),)
        artisttup = (str(artist),)
        keywordstup = (str(keywords),)
        linktup = (str(link),)
        adulttup = (adult,)
        times = (times,)
        ownerup = (str(owner),)
        # if Constant.FAVS:
        #     owner  = self.tag #在fav模式下获取fav用户名
        #     data = nametup + artisttup + keywordstup + linktup + adulttup + times +(str(owner))
        #     datum.append(data)
        #     return

        data = nametup + artisttup + keywordstup + linktup + adulttup + times + ownerup
        logger.debug(data)
        datum.append(data)

    def page_check(self):
        MAX = 'There are no submissions to list'  # 这是FA默认的空画廊页标志
        page_list = self.page_list
        url = self.get_gallery_url()
        if not Constant.FAVS:
            for pages in range(Constant.MAXPAGE):
                real = url + '/' + str(pages + 1) + '/?perpage=72'  # FA画廊采用顺序页码
                content = self.connect_urls(real)  # 获取最大页码
                if len(re.findall(MAX, content.text)):  # 由于FA会出现超出画廊最大数后不会404，所以
                    break  # 用唯一字符串匹配结束循环
                else:
                    logger.debug(real)
                    page_list.append(real)
        # FAV模式下的页码检索，无序页码，需要获取下一页的链接，所以较为麻烦
        else:
            pages = 1
            self.page_list.append(url)
            while True:
                real = self.page_list[-1]
                logger.debug(real)
                content = self.connect_urls(real)
                compiler = re.compile(r'/[0-9]+/next')
                result = compiler.findall(content.text)
                logger.debug(result)
                if result:
                    page_list.append(url + str(result[0]))
                    pages += 1
                else:
                    logger.debug(self.page_list)
                    break
        logger.debug(str(pages) + ' can be found')
        logger.debug(self.page_list)
        return str(pages)

    # 所有多进程函数千万不要动，可能会出一些问题
    '''error携带的是爬取失败的链接'''

    def multi_crawler(self, post_list=None):
        if post_list is None:
            post_list = []
        results = Manager().list()
        error = Manager().list()
        if post_list:
            pass
        else:
            post_list = self.post_list
        data = zip(post_list, repeat(results), repeat(error))
        workers = Pool(Constant.THREADS)
        logger.debug(post_list)
        workers.map(self.get_download_urls_and_table_stuffs, data)
        workers.close()
        workers.join()
        return results, error

if __name__ == "__main__":
    sm = Scrape()
    args = ("view/43980772/",[],[])
    mc = sm.get_download_urls_and_table_stuffs(args)