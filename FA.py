# -*- coding: utf-8 -*-
from Scrapy import Scrapy
from DATABASE import Database
from Download import Download
import argparse
import time
import Constant
import logging
import logging.config

def Logger_creator():
    logging.config.dictConfig(Constant.LOG_CONGIF)
    logger = logging.getLogger('print')
    return logger

def scrapy_modual(singleurl):

    spider.get_post_url(singleurl)
    data,error = spider.multi_crawler()
    logger.debug('Received urls: \n' + str(data))
    db.databaseinsert(data)
    logger.info('Data inserted completed.')

    if error:
        logger.warning('Connection issues, now rescrapying...')
        redata,error = spider.multi_crawler(error)
        db.databaseinsert(redata)

def download_modual():
    logger.info('Downloading according to database...')
    output = db.databaseoutput(spider.tag)
    data = Down.multi_download(output)
    db.databasedownloaded(data)
    logger.info('Download completed')

if __name__ == '__main__':
    logger = Logger_creator()

    parser = argparse.ArgumentParser(prog = 'Furaffinity Gallery Downloader',
                                    description = Constant.TEXT)
    parser.add_argument('-s','--scrapy',action = 'store_true',help = 'Scrape only')
    parser.add_argument('-d','--download',action = 'store_true',help = 'Download from database')
    parser.add_argument('-m','--mix',action = 'store_true',help = 'Scrape and download，not recommended')
    parser.add_argument('-c','--check',action = 'store_true',help = 'Check how many pages')
    parser.add_argument('-u','--update',action = 'store_true',help = 'Update Gallery')

    args = parser.parse_args()

    spider = Scrapy()
    db     = Database()
    Down   = Download()
    db.databaseCreate()

    if args.check:
        logger.info('Page Check processing...')
        spider.page_check()

    if args.scrapy:
        logger.info('***Scrapy modual starting...***')
        time.sleep(1)
        logger.info('Page Check processing...')
        spider.page_check()
        logger.info('Posted urls retrieving...')
        for singleurl in spider.page_list:
            scrapy_modual(singleurl)

    if args.download:
        logger.info('***Download modual starting...***')
        download_modual()

    if args.mix:
        logger.info('***Scrapy and Download modual starting...***')
        logger.info('Page Check processing...')
        spider.page_check()
        for singleurl in spider.page_list:
            logger.info('Posted urls retrieving...')
            scrapy_modual(singleurl)

            download_modual()

    if args.update:
        spider.page_check()
        for singleurl in spider.page_list:
            spider.get_post_url(singleurl)
            data,error = spider.multi_crawler()
            ifupdate = db.databaseupdate(spider.tag,data)
            if ifupdate >=0 and ifupdate <72:
                break
