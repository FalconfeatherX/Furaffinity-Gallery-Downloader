# FA-Gallery-Downloader
## Description
A scraper and downloader targeted at Furaffinity written with python. Use BeautifulSoup and multiprocessing to scrape and download artworks.

## About the downloader
This is a simple and highspeed downloader which may lead to mass network accesses if have no limit. In this case, this downloader is for studying database and multiprocessing.

When using, please set a reasonbale interval and make sure the amount of artworks is not excessive. We all want FA a better place to browse.

## Requirements:
MYSQL 5+

Python 3.6+

BeautifulSoup4

requests

pymysql

## Installing
Just run 'python FA.py' with command-line interface.

## How to use
```
usage: Furaffinity Gallery Downloader [-h] [-s] [-d] [-m] [-c] [-u]

Furaffinity Gallery Downloader use multiprocessing to scrapy full size
download urls which will be insert into mysql database and download artwork
from the database rapidly.

optional arguments:
  -h, --help      show this help message and exit
  -s, --scrape    Scrape only
  -d, --download  Download from database
  -m, --mix       Scrape and download，one page scrape, one page download.
  -c, --check     Check how many pages,72 per page
  -u, --update    Update Gallery
  ```

After the first run,artist.txt and cookies.txt will be created, you can only put one artist into the txt with no \n followed.

## Config
Downloader has no default config, so three parameters are requried in Constant.py

Requrie cookies to login if want to download adult content.

cookies, for instance, should be like:
```
{
'id':'ssasasa',
'name':'falcon'
 }
 ```
 
 cookies.txt file will be created when running for the first time.
 
 This downloader uses MYSQL database to manage everything it scraped, so you should at least create a database.If have one,password(PASSWORD) and database name(DB) are required in Constant.py.
 
 The path(PATH) of storage space to store artist.txt, cookies.txt and downloaded artworks which should be like:
 
 ```'E:\\FA\\'```
 
 Now you can download SCRAPS and FAV by turning 'XX = False' to 'XX = True'.

## Nothing important
好长啊，我还是第一次用python写爬虫，写的有点烂，见谅啊。
