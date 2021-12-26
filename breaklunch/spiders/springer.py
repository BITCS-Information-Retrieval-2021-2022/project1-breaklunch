import scrapy
from bs4 import BeautifulSoup
import calendar


class SpringerSpider(scrapy.Spider):
    name = 'springer'
    # 计划爬取的域名列表，不在其中的无法爬取
    allowed_domains = [
        'springeropen.com',
        'link.springer.com',
        'idp.springer.com',
        'springer.com']
    start_urls = ['https://link.springer.com/']
    # 未爬取的url
    url_path = "breaklunch/List/springer.txt"
    # 已爬取的url
    url_done_path = "breaklunch/List/springer_done.txt"

    def parse(self, response):

        # 未爬取/已爬取的url
        url_list = []
        url_done_list = []
        # 读取url目录
        with open(self.url_path, 'r', encoding='utf-8') as f:
            url_list = f.readlines()[:5]
        with open(self.url_done_path, 'r', encoding='utf-8') as f:
            url_done_list = f.readlines()

        # 按照列表顺序爬取
        for url in url_list:
            if url not in url_done_list:
                yield scrapy.Request(
                    url, callback=self.parse_page, dont_filter=False)

    # 每个网址的解析
    def parse_page(self, response):
        item = {}

        soup = BeautifulSoup(response.text, features="lxml")
        try:
            title = soup.select_one(
                '#main-content > main > \
                article > div.c-article-header > header > h1'
                ).text
        except Exception:
            title = ""

        try:
            abstract = soup.find(
                'div', {'id': "Abs1-content"}).contents[0].text
        except Exception:
            abstract = ""

        try:
            authors = [
                author.find(
                    'a', {'data-test': 'author-name'}).text for author in
                soup.find_all('li', class_='c-article-author-list__item')]
        except Exception:
            authors = []

        try:
            doi = soup.select_one(
                '#article-info-content > div > div > \
                ul.c-bibliographic-information__list > \
                    li.c-bibliographic-information__list-item\
                        .c-bibliographic-information__list-item--doi\
                             > p > span.c-bibliographic-information__value > a'
                             ).text
        except Exception:
            doi = ""

        try:
            url = response.url
        except Exception:
            url = ""

        try:
            time_info = soup.find_all(
                'span', {'class': 'c-bibliographic-information__value'}
                )[1].text
            year = time_info[-4:]
            month = list(calendar.month_name).index(time_info[:-5])
        except Exception:
            year = ''
            month = ''

        type_ = "journal"
        source = "Springer"

        try:
            venue = soup.select_one(
                '#main-content > main > article > \
                div.c-article-header > header > p > a:nth-child(1) > i'
                ).text
        except Exception:
            venue = ""

        try:
            pdf_url = "https://link.springer.com/content/pdf/"
            + url.split('/')[-2] + '/' + url.split('/')[-1] + '.pdf'
        except Exception:
            pdf_url = ""

        try:
            inCitations = soup.find_all(
                'p', {'class': 'c-article-metrics-bar__count'})[1].text
            inCitations = inCitations[:-10]
        except Exception:
            inCitations = ""

        try:
            outCitations = str(len(soup.select_one(
                '#Bib1-content > div > ol').find_all('li')))
        except Exception:
            outCitations = ""

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
        item['inCitations'] = inCitations
        item['outCitations'] = outCitations

        item['video_url'] = ''
        item['video_path'] = ''
        item['thumbnail_url'] = ''
        item['pdf_path'] = ''

        # 解析完成后将url加入已爬取目录
        with open(self.url_done_path, 'a', encoding='utf-8') as f:
            f.write(response.url + "\n")
        yield item
