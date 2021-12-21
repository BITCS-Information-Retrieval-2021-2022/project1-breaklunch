# Scrapy settings for breaklunch project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import os

BOT_NAME = 'breaklunch'

SPIDER_MODULES = ['breaklunch.spiders']
NEWSPIDER_MODULE = 'breaklunch.spiders'

Today=datetime.datetime.now()
LOG_FILE="breaklunch/log/{}.{}.{}_{}.{}.{}.log".format(
    Today.year
    ,Today.month
    ,Today.day
    ,Today.hour
    ,Today.minute
    ,Today.second)



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#设置虚假代理，防反爬
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

USER_AGNET_LIST = [ 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" 
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", 
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", 
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", 
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", 
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", 
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

IP_LIST=[
    "https://221.125.138.189:8193",
    "https://14.215.212.37:9168",
    "https://183.247.211.151:30001",
    "https://121.13.252.58:41564",
    "https://183.236.232.160:8080",
    "https://115.29.170.58:8118",
    "https://115.218.0.233:9000",
    "https://101.200.123.105:8118",
    "https://202.55.5.209:8090",
    "https://103.37.141.69:80",
    "https://183.236.232.160:8080",
    "https://118.180.166.195:8060",
    "https://180.97.87.63:80",
    "https://222.78.6.2:8083",
    "https://139.198.121.76:8811",
    "https://121.40.116.3:8071",
    "https://117.34.25.11:55443",
    "https://121.40.116.3:8071",
    "https://14.215.212.37:9168",
    "https://115.235.23.185:9000",
    "https://121.40.116.3:8071",
    "https://14.215.212.37:9168",
    "https://61.216.156.222:60808",
    "https://202.55.5.209:8090",
    "https://58.20.235.180:9091",
    "https://223.100.166.3:36945",
    "https://103.37.141.69:80",
    "https://111.160.169.54:41820",
    "https://47.243.190.108:7890",
    "https://27.42.168.46:55481",
    "https://61.216.156.222:60808",
    "https://61.150.96.27:36880",
    "https://61.216.156.222:60808",
    "https://82.156.207.216:59394",
    "https://180.97.87.63:80",
    "https://183.247.211.151:30001",
    "https://222.78.6.190:8083",
    "https://121.13.252.58:41564",
    "https://14.215.212.37:9168",
    "https://120.26.160.120:7890",
    "https://115.218.1.122:9000",
    "https://14.215.212.37:9168",
    "https://118.181.226.166:44640",
    "https://110.189.152.86:40698",
    "https://222.242.106.7:80",
    "https://61.216.156.222:60808",
    "https://101.200.238.204:3128",
    "https://61.216.156.222:60808",
    "https://101.200.238.204:3128",
    "https://121.232.148.58:9000",
    "https://121.40.116.3:8071",
    "https://139.198.121.76:8811",
    "https://115.223.195.187:9000",
    "https://124.93.201.59:42672",
    "https://183.247.211.151:30001",
    "https://101.34.214.152:8001",
    "https://183.236.232.160:8080",
    "https://220.135.165.38:8080",
    "https://182.16.103.192:3128",
    "https://47.106.105.236:80"
]

# Obey robots.txt rules
#机器人协议，有些网站不让爬可以改为False
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#并发请求数
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

#爬取延时，防反爬,单位s
DOWNLOAD_DELAY = 2

# The download delay setting will honor only one of:
#单域名请求并发数
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#单IP请求并发数
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'breaklunch.middlewares.BreaklunchSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'breaklunch.middlewares.BreaklunchDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#定义pipeline，项目管道，数越小，优先度越高
#可以一个管道爬取，一个管道下载或者爬取多个网站
ITEM_PIPELINES = {
    'breaklunch.pipelines.BreaklunchPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MONGODB_URI = "mongodb://localhost:27017"
MONGODB_DB = "breaklunch"
