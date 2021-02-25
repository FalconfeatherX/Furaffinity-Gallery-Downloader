
INTERVAL = 1

URL      = 'http://www.furaffinity.net/'

THREADS  = 4

MAXPAGE  = 40

PATH     = ''

PASSWORD = ''

DB       = ''

TEXT     = '''Furaffinity Gallery Downloader use multiprocess tech
        to scrape full size download urls which will be inserted into mysql database
        and download artwork from the database rapidly.'''

SCRAPS   = False

FAVS     = False

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
