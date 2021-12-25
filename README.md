# 项目介绍

- 本项目实现了一个大规模爬虫系统，从**ACM**、**Springer**、**ScienceDirect**三个网站爬取含作者、摘要、会议、引文等论文相关信息的数据。
- 其中，ACM爬取到的论文数据中包含一定比例的视频（以在线观看的url地址给出），ScienceDirect爬取到的论文数据包含多领域的数据，并对来自不同数据源的相同论文进行了去重。
- 同时，本项目实现了增量式爬取、多线程技术提升爬虫效率、使用IP池和调整等待时间抵御网站反爬、断点续爬等功能。
- 最后，本项目基于Elasticsearch+Kibana搭建了一个基本的检索系统，对爬取的数据建立索引，并进行数据分析。

## 一、小组分工

|  姓名  |    学号    |        分工        |
| :----: | :--------: | :----------------: |
| 任翔渝 | 3120210990 | 检索系统、项目管理 |
| 赵建飞 | 3120211015 |      爬虫框架      |
| 池夏烨 | 3120211019 |      爬虫框架      |
|  赵烁  | 3120121000 |      ACM爬取       |
|  徐进  | 3120210994 |    Springer爬取    |
|  葛琪  | 3120201967 | ScienceDirect爬取  |



## 二、爬取数据信息

|     网站      | 数据总量 | 本地PDF数量 | 视频数量 |
| :-----------: | :------: | :---------: | :------: |
|      ACM      |          |             |          |
|   Springer    |          |             |          |
| ScienceDirect |          |             |          |



## 三、开发框架和工具

- 系统：Windows10
- IDE：Pycharm
- 开发语言：Python
- 爬虫框架：Scrapy
- 依赖的Python库：

​	

| 第三方库 |   版本   |
| :------: | :------: |
|  scrapy  | >=2.5.1  |
|   bs4    | >=0.0.1  |
| pymongo  | >=3.12.0 |



## 四、代码目录结构

- Assignment-Description//作业内容描述
- breaklunch//项目主工程文件
  - List//存取待爬取和已爬取的url信息
  - log//爬取日志信息
  - spiders
    - acm.py//用于爬取ACM网站的爬虫脚本
    - sciencedirect.py//用于爬取ScienceDirect网站的爬虫脚本
    - springer.py//用于爬取Springer网站的爬虫脚本
  - items.py//存放爬虫爬取数据的模型
  - middlewares.py//存放各种中间件
  - pipelines.py//用于将数据存储到mongodb中
  - settings.py//爬虫的配置信息

- README.md//说明文档
- scrapy.cfg//项目的配置文件

## 五、部署过程及使用

1. git clone
2. 安装上述项目依赖的Python第三方库
3. 进入项目目录，终端输入scrapy crawl {spidername}
   - 例如：scrapy crawl acm

## 六、项目设计说明

### 6.1 爬虫框架



### 6.2 数据爬取

#### 6.2.1 ACM



#### 6.2.2 Springer



#### 6.2.3 ScienceDirect



### 6.3 检索系统



## 七、其他说明
