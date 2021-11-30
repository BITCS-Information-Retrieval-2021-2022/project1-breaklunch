##项目结构
* spider文件夹里为爬虫文件，每一个数据库可以建立一个爬虫
* 项目里有一个springer数据库是框架，可以借鉴
* 在parse_page中完成网页解析
* pipeline.py连接数据库
* setting.py全局配置
* List文件为目录
* item.py和middleware.py可以实现一些高端操作，非必要，量力而行


##目录
* url每行一个存储在目录文件中
* 目录分为未爬取和已爬取,(没有未爬取建立一个空文件，否则会报错，懒得判断文件是否存在了。。。）
* 动态爬取太难，部分网站有现成的目录
* 没找到现成的目录可以在网站搜索界面搜索空白，基本也有几万项了，把链接扒下来做成目录

##日志
* 日志改为了文件写入，可以通过tail命令查看
* 或者删掉setting文件里的LOG-FILE，日志会在命令行输出

##运行
* 进入项目目录，终端输入scrapy crawl {spidername}
* 例如：scrapy crawl springer

##数据存储
* 参考上届项目
* 建立item字典，然后yield
* 数据库连接在pipeline.py中，数据库名称和端口在setting.py末尾，根据需求修改

##网页解析
* 在爬虫文件中parse

##数据库和pipeline
* 参考上届项目

##具体看注释
