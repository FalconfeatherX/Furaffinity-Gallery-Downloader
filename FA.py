# -*- coding: utf-8 -*-
from Scrape import Scrape
from Database import Database
from Download import Download
import argparse
import time
import Constant
import logging
import logging.config
from Kits import Kits

def logger_creator():
    logging.config.dictConfig(Constant.LOG_CONGIF)
    logger = logging.getLogger('print')
    return logger


def rescrape_module(links):
    spider.post_list = links
    data, error = spider.multi_crawler()
    logger.debug('Received urls: \n' + str(data))
    db.database_insert(data)
    logger.info('Data inserted completed.')

    if error:
        logger.warning('Connection issues, now rescraping...')
        redata, error_still = spider.multi_crawler(error)
        db.database_insert(redata)
        if error_still:
            logger.warning('Scrape failed still list as followed:')
            logger.warning(' '.join(error_still))
            logger.warning('You can use -r to rescrape links above. (Paste the list to the iput line)')


def scrapy_module(single_url):
    spider.get_post_url(single_url)
    data, error = spider.multi_crawler()
    logger.debug('Received urls: \n' + str(data))
    db.database_insert(data)
    logger.info('Data(' + ownerName + ') inserted completed.')

    if error:
        logger.warning('Connection issues, now rescraping...')
        redata, error_still = spider.multi_crawler(error)
        db.database_insert(redata)
        if error_still:
            logger.warning('Scrape failed still list as followed:')
            logger.warning(' '.join(error_still))
            logger.warning('You can use -r to rescrapy links above. (Paste the list to the iput line)')


def download_module():
    logger.info('Downloading(' + ownerName + ') according to database...')
    output = db.database_output(spider.tag)
    data = Down.multi_download(output)
    db.database_downloaded(data)
    logger.info('Download(' + ownerName + ') completed')


def update_module():
    update_counter = 0
    logger.info('Updating(' + ownerName + ') artworks information into database...')
    (maxUpdateDate, result) = db.database_update(ownerName)
    spider.page_check()
    for single_url in spider.page_list:
        spider.get_post_url(single_url)
        data, error = spider.multi_crawler()
        db.database_insert(data)

        # 一般来说，更新一次要小于72，则会在第一页便完成更新，因此大概率只需要检索第一页的时间戳
        # 更新模式不具备健壮性，只要出现网络波动导致的爬取失败，就有可能使maxUpdateData越过一些post，进而丢失掉这些post更新
        # 目前没有更好的解决方法，只能强制性进行scrape全部
        # 除此之外，如果出现网络波动可能导致的爬取失败使得计数器小于72，也会导致没办法进行到第二页，这也是不推荐使用更新模式爬取的原因之一
        (maxUpdateDateNow, result) = db.database_update(ownerName)
        for updateThing in result:
            if updateThing > maxUpdateDate:
                update_counter += 1
        if update_counter < 72:
            logger.info(str(update_counter) + ' artworks are Updated!')
            return
        else:
            update_counter = 0

    # 这是一种极端情况，当时隔很久之后，画师更新了72张以上，则需要用以下方法
    # 当使用更新模式进行爬取模式时（这是可行的，但不推荐），也会调用到此段
    update_counter = 0
    (maxUpdateDateNow, result) = db.database_update(ownerName)
    for i in result:
        if i < maxUpdateDate:
            update_counter += 1
    logger.info(str(update_counter) + ' artworks are Updated!')


if __name__ == '__main__':
    logger = logger_creator()

    if Constant.FAVS:
        logger.info("favorite pattern confirmed")

    parser = argparse.ArgumentParser(prog='Furaffinity Gallery Downloader',
                                     description=Constant.TEXT)
    parser.add_argument('-s', '--scrapy', action='store_true', help='Scrape only')
    parser.add_argument('-d', '--download', action='store_true', help='Download from database')
    parser.add_argument('-m', '--mix', action='store_true', help='Scrape and download，not recommended')
    parser.add_argument('-c', '--check', action='store_true', help='Check how many pages')
    parser.add_argument('-u', '--update', action='store_true', help='Update Gallery')
    parser.add_argument('-r', '--rescrapy', action='store_true', help='Rescrape for sepecial reasons')
    args = parser.parse_args()

    spider = Scrape()
    db = Database()
    Down = Download()
    db.database_create()
    Kits = Kits()
    ownerName = Kits.get_owner_name()

    if args.rescrapy:
        logger.info('***Rescrapy modual starting...***')
        rescrape_input = input('Enter links in list format(ex:[' ',' ']): ').split(' ')

        rescrape_module(rescrape_input)

    if args.check:
        logger.info('Page Check(' + ownerName + ') processing...')
        page_num = spider.page_check()
        logger.info(page_num + ' pages can be found currently.')

    if args.scrapy:
        logger.info('***Scrape(' + ownerName + ') modual starting...***')
        time.sleep(1)
        logger.info('Page Check(' + ownerName + ') processing...')
        spider.page_check()
        logger.info('Posted urls(' + ownerName + ') retrieving...')
        for single_url in spider.page_list:
            scrapy_module(single_url)
        logger.info('***Scrape(' + ownerName + ') completed***')

    if args.download:
        logger.info('***Download(' + ownerName + ') modual starting...***')
        download_module()
        logger.info('***Download(' + ownerName + ') completed***')

    if args.mix:
        logger.info('***Scrape and Download(' + ownerName + ') modual starting...***')
        logger.info('Page Check(' + ownerName + ') processing...')
        spider.page_check()
        for single_url in spider.page_list:
            logger.info('Posted urls(' + ownerName + ') retrieving...')
            scrapy_module(single_url)

            download_module()

    if args.update:
        try:
            update_module()
        except:
            logger.info("connection timeout")
