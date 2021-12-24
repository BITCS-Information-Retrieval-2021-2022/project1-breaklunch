import scrapy
import random
import time


class ACMSpider(scrapy.Spider):
    name = 'acm'

    acm_prefix = 'https://dl.acm.org'
    month_dict = {
        'January': '1', 'February': '2', 'March': '3',
        'April': '4', 'May': '5', 'June': '6',
        'July': '7', 'August': '8', 'September': '9',
        'October': '10', 'November': '11', 'December': '12'
    }
    # pdf下载路径
    pdf_download_path = 'breaklunch/acm_pdf_download/'
    # 用于debug
    debug_flag = True

    def start_requests(self):
        # 起始url，按ACM的subject分类，在此基础上按被引用量排序（引用量高的文章更有可能有视频）
        urls = [
            # 'https://dl.acm.org/subject/ai?sortBy=cited&startPage=0&pageSize=50'
            # 'https://dl.acm.org/subject/is?sortBy=cited&startPage=0&pageSize=50'
            # 'https://dl.acm.org/subject/mobile?sortBy=cited&startPage=0&pageSize=50'
            # 'https://dl.acm.org/subject/mobile?startPage=0&pageSize=50&sortBy=cited'
            'https://dl.acm.org/subject/society?startPage=0&pageSize=50&sortBy=cited'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # 爬取论文概况栏
        paper_items = response.css('div.issue-item__content-right')

        for paper_item in paper_items:
            # 增加一个随机时延，减小服务器地址被屏蔽的可能
            wait = random.randint(1, 10)
            time.sleep(wait * 0.1)
            try:
                paper_url = self.acm_prefix + paper_item.css('span.hlFld-Title a').attrib['href']
                yield scrapy.Request(paper_url, callback=self.parse_paper_homepage, dont_filter=True)
            except:
                continue

        # 爬完的页写入文档，以实现断点续爬
        with open('breaklunch/List/acm_done.txt', 'a') as f:
            f.write(response.url + '\n')

        # 爬取下一页论文列表
        next_page = response.css('a.pagination__btn--next').attrib['href']
        if next_page is not None and self.debug_flag is True:
            # self.debug_flag = False
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)

    def parse_paper_homepage(self, response):
        # 获取breadcrumb信息，判断是否为会议期刊论文，如果是获取类型，如果不是不收集数据
        paper_type_url = response.css('nav.article__breadcrumbs.separator a:nth-child(2)').attrib['href']
        if paper_type_url == '/journals' or paper_type_url == '/conferences':
            paper_type = paper_type_url[1:-1]
        else:
            with open('breaklunch/List/acm_done.txt', 'a') as f:
                f.write(response.url + '\n')
            return

        # 获取title, abstract, authors, doi和url
        title = response.css('h1.citation__title::text').get()
        abstract = response.css('div.abstractSection.abstractInFull p::text').get()
        authors = response.css('span.loa__author-name span::text').getall()
        # doi = response.css('a.issue-item__doi').attrib['href']
        url = response.url
        doi = url.replace('dl.acm.org/doi', 'doi.org')

        # 获取时间
        date = response.css('span.CitationCoverDate::text').get().split(' ')
        year = date[2]
        month = self.month_dict[date[1]]

        # 获取来源
        venue = response.css('nav.article__breadcrumbs.separator a:nth-child(3)').attrib['href'].split('/')[
            2].upper()
        source = 'ACM'

        # 获取视频相关信息
        video_element = response.css('div.article-media__item.separated-block--dashed--bottom.clearfix')
        if video_element is not None:
            try:
                video_postfix = video_element.css('div.video__links.table__cell-view a:nth-child(2)').attrib['href']
                video_url = self.acm_prefix + video_postfix
            except:
                video_url = None
            video_path = None
            try:
                thumbnail_path = video_element.css('stream.cloudflare-stream-player').attrib['poster']
            except:
                thumbnail_path = None
        else:
            video_url = None
            video_path = None
            thumbnail_path = None

        # 获取pdf相关信息
        pdf_red_button = response.css('a.btn.red')
        try:
            if pdf_red_button is not None:
                pdf_url = self.acm_prefix + pdf_red_button.attrib['href']
                saved_title = title.replace('\\', '').replace('/', '').replace(':', '：')
                saved_title = saved_title.replace('*', '').replace('?', '？').replace('"', '')
                saved_title = saved_title.replace('<', '').replace('>', '').replace('|', '')
                pdf_path = self.pdf_download_path + saved_title + '.pdf'
                yield scrapy.Request(pdf_url, meta={'pdf_path': pdf_path},
                                     callback=self.parse_pdf_download, dont_filter=True)
            else:
                pdf_url = None
                pdf_path = None
        except KeyError:
            pdf_url = None
            pdf_path = None

        # 获取引用信息
        in_citations = response.css('span.citation span:nth-child(2)::text').get().replace(',', '')
        out_citations_list = response.css('ol.rlist.references__list.references__numeric li')
        if len(out_citations_list) == 0:
            out_citations_list = response.css('ol.rlist.references__list li')
        if out_citations_list is not None:
            out_citations = str(len(out_citations_list))
        else:
            out_citations = str(0)

        # 爬完的页写入文档，以实现断点续爬
        with open('breaklunch/List/acm_done.txt', 'a') as f:
            f.write(response.url + '\n')

        # yield
        yield {
            'title': title,
            'abstract': abstract,
            'authors': authors,
            'doi': doi,
            'url': url,
            'year': year,
            'month': month,
            'type': paper_type,
            'venue': venue,
            'source': source,
            'video_url': video_url,
            'video_path': video_path,
            'thumbnail_path': thumbnail_path,
            'pdf_url': pdf_url,
            'pdf_path': pdf_path,
            'inCitations': in_citations,
            'outCitations': out_citations
        }

    def parse_pdf_download(self, response):
        # 下载pdf
        try:
            path = response.meta['pdf_path']
            with open(path, 'wb') as f:
                f.write(response.body)
        except:
            self.log(f"\n下载pdf出错，出错url为：{response.url}\n")
