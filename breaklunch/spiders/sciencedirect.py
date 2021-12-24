import re

import scrapy
from bs4 import BeautifulSoup


class SciencedirectSpider(scrapy.Spider):
    name = 'sciencedirect'
    allowed_domains = ['www.sciencedirect.com']
    start_urls = ['https://www.sciencedirect.com/']

    # 未爬取的url
    url_path = "breaklunch/List/sciencedirect.txt"
    # 已爬取的url
    url_done_path = "breaklunch/List/sciencedirect_done.txt"

    month2num = {"January": 1,
                 "February": 2,
                 "March": 3,
                 "April": 4,
                 "May": 5,
                 "June": 6,
                 "July": 7,
                 "August": 8,
                 "September": 9,
                 "October": 10,
                 "November": 11,
                 "December": 12,
                 }

    def parse(self, response):

        # testing code

        # url = '/science/article/pii/S2352853220301474'      # 正常
        # url = '/science/article/pii/S2092521220300572'      # 无摘要
        # url = '/science/article/abs/pii/0001691854900013'   # 无access
        # yield scrapy.Request('https://www.sciencedirect.com' + url,
        #                      callback=self.parse_page, dont_filter=False)
        # return

        # 读取url目录
        with open(self.url_path, 'r', encoding='utf-8') as f:
            url_list = f.readlines()
        with open(self.url_done_path, 'r', encoding='utf-8') as f:
            url_done_list = f.readlines()

        # 按照列表顺序爬取
        cnt = 0
        max_cnt = 500
        for url in url_list:
            if url not in url_done_list:
                yield scrapy.Request(
                    'https://www.sciencedirect.com' + url,
                    callback=lambda r: self.parse_page(r, url),
                    dont_filter=False)
                cnt += 1
                if cnt == max_cnt:
                    break

    def parse_page(self, response, origin_url):
        print("parsing {}...".format(response.url))
        if response.status != 200:
            print("unexpected status code:" + str(response.status))
            # 可能是被反爬了 不标记为已完成
            return
        if '/article/abs/pii' in response.url:
            # https://www.sciencedirect.com/science/article/abs/pii/0001691854900013
            self.save_done_url(origin_url)
            return

        try:
            # 'S2212671614001024
            pii = re.search(
                r'https://www.sciencedirect.com' +
                r'/science/article/pii/((\d|\w)+)',
                response.url).groups()[0]

        except Exception:
            # 可能是 no access.
            self.save_done_url(origin_url)
            return

        item = {}
        soup = BeautifulSoup(response.text, features="lxml")

        title = soup.select_one("#screen-reader-main-title > span").text

        abstract = ''
        if soup.select_one('#abstracts'):
            abstract = soup.select_one('#abstracts').text

        author_group = soup.select("#author-group")[0]
        authors = []
        for child in author_group:
            if child.has_attr('href'):
                names = child.find_all(name='span')
                names = [n.text for n in names]
                names = names[1:-1]
                authors.append(' '.join(names))

        doi = soup.select_one('#article-identifier-links > a.doi').text
        url = response.url
        month, year = '', ''
        pubtime = soup.select_one(
            '#publication > div.u-text-center.publication-volume > div')
        for li in pubtime:
            line = li.text
            if re.match(r'\w+ \d\d\d\d', line):
                m, y = line.split()
                if m in self.month2num:
                    month = str(self.month2num[m])
                year = y
        type_ = "journal"
        venue = soup.select_one("#publication-title > a").text
        source = "ScienceDirect"

        pdf_url = "https://www.sciencedirect.com/science/article/pii/{}/pdfft"

        # 当前能获取的先放着
        item['title'] = title
        item['abstract'] = abstract
        item['authors'] = authors
        item['doi'] = doi
        item['url'] = url
        item['year'] = year
        item['month'] = month
        item['type'] = type_
        item['venue'] = venue
        item['source'] = source
        item['pdf_url'] = pdf_url

        # 本来也要置空的
        item['video_url'] = ''
        item['video_path'] = ''
        item['thumbnail_url'] = ''
        item['pdf_path'] = ''

        # 然后是麻烦的异步加载问题
        # 获取token
        entitled = re.search(r'entitledToken":"((\d|\w)+)"',
                             response.text).groups()[0]
        reference_url_pattern = "https://www.sciencedirect.com/sdfe/arp/" \
                                "pii/{}/references?entitledToken={}"
        reference_url = reference_url_pattern.format(pii, entitled)
        citation_url_pattern = "https://www.sciencedirect.com/sdfe/arp/" \
                               "pii/{}/citingArticles?" \
                               "creditCardPurchaseAllowed=true" \
                               "&preventTransactionalAccess=true" \
                               "&preventDocumentDelivery=true "
        citation_url = citation_url_pattern.format(pii)

        yield scrapy.Request(reference_url, method='GET',
                             callback=lambda r:
                             self.parseXHR(r, item, citation_url),
                             dont_filter=False)

    def parseXHR(self, response, item, citation_url):
        try:
            content = response.json().get("content")[0]
            ref_list = content.get('$$')[1].get("$$")
            outCitations = len(ref_list)
            item['outCitations'] = outCitations
        except Exception:
            item['outCitations'] = 0

        yield scrapy.Request(citation_url, method='GET',
                             callback=lambda r: self.parseXHR2(r, item),
                             dont_filter=False)

    def parseXHR2(self, response, item):
        content = response.json()
        item['inCitations'] = content.get('hitCount')

        # 完成 item 组装 标记完成
        pii = re.search(r'https://www.sciencedirect.com/science'
                        r'/article/pii/((\d|\w)+)',
                        item['url']).groups()[0]
        url = '/science/article/pii/' + pii
        self.save_done_url(url)

        yield item

    def save_done_url(self, url):
        url = url.strip()
        print("saving done url:", url)
        with open(self.url_done_path, 'a', encoding='utf-8') as f:
            f.write(url + "\n")
