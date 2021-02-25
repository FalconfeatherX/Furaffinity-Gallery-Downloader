# Furaffinity画廊下载器
## 描述
使用多进程高速爬取画廊作品

## 关于下载器
此下载器仅限于学习，由于存在多进程行为，会增加服务器负荷，所以请合理设置爬取间隔，合理使用下载器
## 依赖
MYSQL 5+

Python 3.6+

BeautifulSoup4

requests

pymysql（此下载器使用mysql进行管理，其中包括了标签，下载网址，作者，年龄限制标记等信息）

## 安装
在命令符中执行'python FA.py'

## 使用
```
用法: Furaffinity Gallery Downloader [-h] [-s] [-d] [-m] [-c] [-u]

Furaffinity Gallery Downloader use multiprocessing to scrapy full size
download urls which will be insert into mysql database and download artwork
from the database rapidly.

参考:
  -h, --help      帮助
  -s, --scrape    仅爬取信息到数据库
  -d, --download  从数据库中获取链接并下载
  -m, --mix       爬取信息后下载，行为是每爬取72张后执行一次下载
  -c, --check     以72张为一页，查询页数
  -u, --update    更新，此功能暂不能使用
  ```

在第一次运行后，artist.txt和cookies.txt将被创建，在前者输入作者名，注意，只能输一个，且不能有回车
## 配置
下载器没有默认设置，Constant.py需要配置三个参数

如果要爬取成人内容，需将你的cookies信息添加进去

cookies示例：
```
{
'id':'ssasasa',
'name':'falcon'
 }
 ```
 你需要至少创建一个数据库，并将用户名和密码加入配置才能启动，本下载器完全依赖数据库管理所有数据

 关于配置文件中的路径名应遵循如下格式
 ```'E:\\FA\\'```

FAV与SCRAPS中的作品现在也可以下载：''XX = False'关闭 'XX = True'开启' 如果全部开启，仅会下载SCRAPS中的作品
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
