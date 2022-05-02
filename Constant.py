
INTERVAL = 0.5 #爬取的默认间隔，下载默认为0.5，大于默认可能被服务器拦截
URL      = 'http://www.furaffinity.net/'
THREADS  = 6 #爬取的默认最大进程数，下载默认为8，大于默认可能被服务器拦截
MAXPAGE  = 40 #默认最大为40页，请视情况更改
PATH     = ''
PASSWORD = ''
DB       = ''
HOST     = ''
TEXT     = '''Furaffinity Gallery Downloader use multiprocess tech
        to scrape urls of artwork which will be inserted into mysql database
        and download artwork by urls fetched from the database rapidly.'''
SCRAPS   = False
FAVS     = False
WINPATH  =''

LOG_CONGIF = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'fa.log',
            'level': 'DEBUG',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'print': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
