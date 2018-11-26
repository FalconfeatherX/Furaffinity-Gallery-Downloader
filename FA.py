# -*- coding: utf-8 -*-
from Scraper import Scraper
from DATABASE import Database
from Download import Download
import argparse
import time
import Constant
if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog = 'Furaffinity Gallery Downloader',
                                    description = Constant.TEXT)
    parser.add_argument('-s','--scrape',action = 'store_true',help = 'Scrape only')
    parser.add_argument('-d','--download',action = 'store_true',help = 'Download from database')
    parser.add_argument('-m','--mix',action = 'store_true',help = 'Scrape and download，not recommended')
    parser.add_argument('-c','--check',action = 'store_true',help = 'Check how many pages')
    args = parser.parse_args()

    spider = Scraper()
    db     = Database()
    Down   = Download()
    db.databaseCreate()

    if args.check:
        spider.page_check()

    if args.scrape:
        spider.page_check()
        for singleurl in spider.page_list:
            spider.get_post_url(singleurl)
            datum = spider.multi_crawler()
            db.databaseinsert(datum)

            for i in spider.ERRORLIST:
                arg = zip(i,[])
                try:
                    spider.get_download_urls_and_table_stuffs(arg)
                except:
                    print('Scrape failed')
            time.sleep(1)
            print(singleurl + ' done.')

    if args.download:
        print('Downloading start.')
        output = db.databaseoutput(spider.tag)
        datum = Down.multi_download(output)
        db.databasedownloaded(datum)
        print('Download finished')

    if args.mix:
        spider.page_check()
        for singleurl in spider.page_list:
            spider.get_post_url(singleurl)
            datum = spider.multi_crawler()
            db.databaseinsert(datum)
            print(singleurl + ' done.')
            print(singleurl + ' start downloading.')
            output = db.databaseoutput(spider.tag)
            datum = Down.multi_download(output)#not recommended
            db.databasedownloaded(datum)
            print(singleurl + ' downloading finished')
        print('Downloading all finished')
