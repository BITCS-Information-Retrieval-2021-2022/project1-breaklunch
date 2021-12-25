

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
|      ACM      |  460229  |    8415     |  18220   |
|   Springer    | 1421228  |      -      |    -     |
| ScienceDirect |  791428  |      -      |    -     |



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
2. 安装MongoDB
3. 进入项目目录，终端输入scrapy crawl {spidername}
   - 例如：scrapy crawl acm

## 六、项目设计说明

### 6.1 爬虫框架
爬虫项目基于scrapy框架
#### 6.1.1 爬取策略
爬取策略分为两个阶段，将连接遍历和网页解析分离，分为URL爬取和Item爬取。
 - URL爬取：根据站点特点设计爬取策略，遍历数据库，将爬取文章的URL保存到本地目录。
 - Item爬取：遍历URL目录访问数据库，解析网页并将相关 Item保存到本地。

#### 6.1.1 技术手段
 - 日志记录
   - 除了scrapy框架提供的日志功能以外，将爬取的URL另行保存。
 - 增量爬取
   - 设置全局时间戳，跳过早于时间戳的文章，爬取结束后更新时间戳。
 - 断点续爬
   - 每一个URL有一个编号，按照爬取顺序递增，发生故障后从日志查看最后爬取编号，继续爬取。
 - 并行爬取
   - 除了scrapy提供的并行爬取功能之外，将URL目录分为多份，在多台机器爬取。
 - 文章去重
   - 保存文章之前检索数据库，不存在则插入文章，已存在则插入数据源。


#### 6.1.2 网络反爬
 - 动态间隔
   - 爬取网页时遇到403后，倍增爬取间隔时间，每成功爬取一定数量后，间隔时间逐渐减小。
 - IP池
   - 存储多条IP地址，每次访问网页之前随机选择一条IP地址。
 - 虚假代理
   - 类似IP池，存储多个用户代理，在每次访问前随机选择。

### 6.2 数据爬取

#### 6.2.1 ACM

- 爬虫工作流程

  ACM数据库爬虫的工作流程主要分为收集论文列表URL和爬取论文信息两个步骤，爬虫的具体工作流程如下图所示：

![image](https://github.com/BITCS-Information-Retrieval-2021-2022/project1-breaklunch/blob/main/extra/acm_spider.png)

- 收集论文列表URL

  ​	每一个论文列表包含50条论文的概况信息，可以从列表页中获取论文的URL，进一步爬取论文的详细信息，当一个列表页的论文全部爬取完毕后可以通过页面底部下一页指向的链接获取新的论文列表。按照这样的方法，我们通过三种方法收集初始页的论文列表URL：

  - 通过ACM DL主页的Search by Subject版块获取初始列表URL；
  - 通过ACM DL的期刊和会议列表获取初始列表URL；
  - 通过ACM DL的搜索功能获取初始列表URL。

- 爬取论文信息

  ​	通过论文列表中获取的论文主页URL可以获取论文的信息：

  - 论文的标题、摘要和doi等基本信息通过请求论文URL的response获取，并保存到MongoDB，唯一标识为论文的doi；
  - 论文的pdf如果可以获取，将论文pdf保存到本地；
  - 论文如有视频信息，从论文URL的response中获取video和thumbnail的URL保存到MongoDB。(为保证有视频的论文数量，收集的论文列表主要为带视频的论文列表，和按照cited数量排序的论文列表)

#### 6.2.2 Springer

- 爬虫工作流程

  Springer数据库爬虫的工作流程主要分为收集论文列表URL和爬取论文信息两个步骤，爬虫的具体工作流程与6.2.1相似。

- 收集论文列表URL
  ​	获取初始页的论文列表URL共分为以下三步：
  - 在https://link.springer.com/journals/{a-z}/{1-2}页面获取所有刊物的页面链接
  - 进入刊物页面，获取该刊物所有历史期刊
  - 进入期刊页面，获取该期刊下所有文章链接

- 爬取论文信息
  ​	通过论文列表中获取的论文主页URL可以获取论文的信息：
  - 论文的标题、摘要和doi等基本信息通过请求论文URL的response获取，并保存到MongoDB，唯一标识为论文的doi；
  - 通过字符串拼接的方式，直接获取包括付费论文在内的所有论文的pdf链接；

#### 6.2.3 ScienceDirect

- 爬虫工作流程

  Springer数据库爬虫的工作流程主要分为收集论文列表URL和爬取论文信息两个步骤，爬虫的具体工作流程与6.2.1相似。

- 收集论文列表URL
  ​	获取初始页的论文列表URL共分为以下三步：
  - 在https://www.sciencedirect.com/browse/journals-and-books?page={1-12}&contentType=JL&accessType=openAccess页面获取所有刊物的页面链接
  - 进入刊物页面，获取该刊物所有历史期刊
  - 进入期刊页面，获取该期刊下所有文章链接

- 爬取论文信息
  ​	通过论文列表中获取的论文主页URL可以获取论文的信息：
  - 论文的标题、摘要和doi等基本信息通过请求论文URL的response获取；
  - 论文的引用数、被引用数通过异步请求XHR获取；
  - 组装数据，保存到MongoDB，唯一标识为论文的doi。


### 6.3 数据清洗

为了加速爬取，本项目将URL目录分为多份，在多台机器爬取。为了进行kibana数据分析，还需将这些数据合并为同一数据源。

- 把不同数据源的MongoDB Collection以Json格式分别导出
- 创建总和Collection，并以doi作为唯一索引
- 读取Json文件，将每条记录清洗为统一的数据格式，尝试插入总和Collection，这仅在doi唯一时发生。


### 6.4 检索系统

#### 6.4.1 Elasticsearch搭建

- 安装Elasticsearch

  查看官网地址，下载安装对应平台的版本即可。

- 启动Elasticsearch

  进入Elasticsearch目录，终端输入

  ```
  ./bin/elasticsearch
  ```

  默认启动的是9200端口，可打开http://localhost:9200进行验证。

- 安装管理界面

  elasticsearch-head可以很方便的查看es集群状态，终端输入以下命令进行安装。

  ```
  git clone git://github.com/mobz/elasticsearch-head.git
  cd elasticsearch-head
  npm install
  npm run start
  ```

  默认启动的是9100端口，可打开http://localhost:9100进行验证。

#### 6.4.2 Kibana搭建

- 安装Kibana

  查看官网地址，下载对应平台的版本即可。

- 启动Kibana

  进入Kibana目录，终端输入

  ```
  ./bin/kibana
  ```

  默认启动的是5601端口，可打开http://localhost:5601进行验证。

#### 6.4.3 MongoDB和Elasticsearch实时同步

- 安装mongo-connector

  ```
  pip install mongo-connector
  ```

- 安装elastic2-doc-manager

  ```
  pip install elastic2-doc-manager
  ```

- mongo开启副本集

  首先关闭正在运行的MongoDB服务，然后通过指定--replSet选项来启动MongoDB

  ```
  mongod --port "PORT" --dbpath "YOUR_DB_DATA_PATH" --replSet "REPLICA_SET_INSTANCE_NAME"
  ```

  另外打开一个终端，连接MongoDB服务，在MongoDB客户端使用命令来启动一个新的副本集

  ```
  >rs.initiate()
  ```

- 开启实时同步

  终端中输入以下命令即可

  ```
  mongo-connector -m localhost:27017 -t localhost:9200 -d elastic2_doc_manager
  ```

#### 6.4.4 数据可视化

- 在Kibana中添加自定义索引
- 点击Kibana的Visualize菜单，进入可视化图表创建界面
  - Kibana自带垂直条形图、水平条形图、饼图、折线图等10种图表
- 使用Kibana的仪表盘展示保存的可视化结果集合

## 七、其他说明

暂无
