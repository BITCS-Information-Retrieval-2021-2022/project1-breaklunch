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
    "https://123.160.1.244:9999",
    "https://115.221.241.114:9999",
    "https://223.215.6.14:9999",
    "https://1.196.177.67:9999",
    "https://223.199.20.168:9999",
    "https://114.99.5.7:9999",
    "https://110.243.11.227:9999",
    "https://218.73.118.194:9999",
    "https://110.243.21.234:9999",
    "https://183.166.97.158:9999",
    "https://223.199.24.230:9999",
    "https://223.199.28.237:9999",
    "https://175.44.109.194:9999",
    "https://58.212.43.145:9999",
    "https://222.240.184.126:8086",
    "https://117.64.237.142:9999",
    "https://27.38.98.162:9797",
    "https://122.228.19.7:3389",
    "https://221.13.156.158:55443",
    "https://58.244.52.175:8080",
    "https://60.167.21.181:8118",
    "https://111.160.169.54:42626",
    "https://183.129.244.20:14153",
    "https://153.101.64.50:12034",
    "https://58.249.55.222:9797",
    "https://114.99.15.150:6890",
    "https://115.171.85.225:9000",
    "https://123.160.1.244:9999",
    "https://115.221.241.114:9999",
    "https://223.215.6.14:9999",
    "https://1.196.177.67:9999",
    "https://223.199.20.168:9999",
    "https://114.99.5.7:9999",
    "https://110.243.11.227:9999",
    "https://218.73.118.194:9999",
    "https://110.243.21.234:9999",
    "https://183.166.97.158:9999",
    "https://223.199.24.230:9999",
    "https://222.240.184.126:8086",
    "https://223.199.28.237:9999",
    "https://175.44.109.194:9999",
    "https://58.212.43.145:9999",
    "https://171.12.113.76:9999",
    "https://114.99.25.98:18118",
    "https://223.199.26.142:9999",
    "https://223.199.18.98:9999",
    "https://112.85.176.179:9999"
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
