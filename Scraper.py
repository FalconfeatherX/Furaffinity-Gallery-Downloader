# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import time
from Kits import Kits
from multiprocessing import Pool,Manager
from itertools import repeat
import Constant
import requests

class Scraper():
    ERRORLIST = []
    def __init__(self):
        self.url =  Constant.URL + 'gallery/'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
        self.data = Kits.cookies(Kits)
        self.tag = Kits.get_artist_name(Kits)
        self.page_list = []
        self.post_list = []

    def connect_urls(self,url):
        try:
            return requests.Session().get(url,headers = self.headers,cookies = self.data,timeout = 30)
        except:
            print('%s Connected error'%url)


    def get_gallery_url(self):
        self.url = self.url + self.tag
        return self.url


    def get_post_url(self,singleurl):
        self.post_list = []
        urlcontent = self.connect_urls(singleurl).text
        compiler = re.compile(r'view/\d+/')
        result = compiler.findall(urlcontent)
        for transfers in result:
            self.post_list.append(transfers)
        self.post_list = set(self.post_list)
        self.post_list = list(self.post_list)


    def get_download_urls_and_table_stuffs(self,args):
        download_links,datum = args;keyword = '';data = []
        try:
            downloadcontent = self.connect_urls(Constant.URL + download_links).text
            time.sleep(Constant.INTERVAL)

            soup = BeautifulSoup(downloadcontent,'lxml')
            adults = soup.find('div',{'align':"left"})
            tags   = soup.find('div', {'id': 'keywords'})

            if 'adult' in str(adults.img):
                adult = 1        #if have adult content,will be set to 1 else 0
            else:
                adult = 0

            try:
                for i in tags.text.split():
                    keyword = keyword + i + ' '#keywords parser
                if len(keyword) > 100:
                    keyword = keyword[:100]    #cut the lenth of keywords
            except:
                keyword = 'None'               #if have no keywords

            keywords = keyword
            name     = soup.find('th',{'class':"cat"}).text.strip()#artwork name
            link     = soup.find('img',{'id':"submissionImg"})['data-fullview-src']#artwork fullsize link
            artist   = self.tag      #artwork artisr

            data.append(str(name));data.append(str(artist));data.append(str(keywords))
            data.append(str(link));data.append(adult)
            datum.append(data)

        except:
            print('error' + download_links)
            Scraper.ERRORLIST.append(Constant.URL + download_links)


    def page_check(self):
        MAX = 'There are no submissions to list'
        page_list = self.page_list
        self.get_gallery_url()
        for pages in range(Constant.MAXPAGE):
            realurl = self.url + '/' + str(pages+1) + '/?perpage=72'
            newcontent = self.connect_urls(realurl)             #search for the max page
            if len(re.findall(MAX,newcontent.text)):            #由于FA会出现超出画廊最大数后不会404，所以
                break                                           #用唯一字符串匹配结束循环
            else:
                print(realurl)
                page_list.append(realurl)
        print(str(pages) + ' ' + 'can be found')
        return str(pages)


    def multi_crawler(self):
        results = Manager().list()
        data = zip(self.post_list,repeat(results))
        workers = Pool(Constant.THREADS)
        workers.map(self.get_download_urls_and_table_stuffs,data)
        workers.close()
        workers.join()
        return results
