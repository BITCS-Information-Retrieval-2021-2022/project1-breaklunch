import scrapy
from bs4 import BeautifulSoup
import calendar


class SpringerSpider(scrapy.Spider):
    name = 'springer'
    # 计划爬取的域名列表，不在其中的无法爬取
    allowed_domains = ['springeropen.com']
    start_urls = ['https://www.springer.com/cn']
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
            url_list = f.readlines()
        with open(self.url_done_path, 'r', encoding='utf-8') as f:
            url_done_list = f.readlines()

        # 按照列表顺序爬取
        # url_list = set(url_list)
        # url_done_list = set(url_done_list)
        for url in url_list:
            if url not in url_done_list:
                yield scrapy.Request(url, callback=self.parse_page, dont_filter=False)

    # 每个网址的解析
    def parse_page(self, response):
        item = {}

        soup = BeautifulSoup(response.text, features="lxml")
        title = soup.select_one('#main-content > main > article > div.c-article-header > h1').text

        abstract = soup.select_one('#Abs1-content')
        if abstract:
            abstract = abstract.text
        else:
            abstract = ''

        authors = [author.find('a', {'data-test': 'author-name'}).text for author in
                   soup.find_all('li', class_='c-article-author-list__item')]
        doi = soup.select_one(
            '#article-info-content > div > div:nth-child(2) > ul.c-bibliographic-information__list > li.c-bibliographic-information__list-item.c-bibliographic-information__list-item--doi > p > span.c-bibliographic-information__value > a').text
        url = response.url
        year = soup.select_one(
            '#main-content > main > article > div.c-article-header > ul.c-article-identifiers > li:nth-child(3) > a > time').text[
               -4:]
        month = list(calendar.month_name).index(soup.select_one(
            '#main-content > main > article > div.c-article-header > ul.c-article-identifiers > li:nth-child(3) > a > time').text[
                                                3:-5])
        type_ = "journal"
        venue = soup.select_one('#main-content > main > article > div.c-article-header > p > a:nth-child(1) > i').text
        source = "Springer"
        pdf_url = "https:" + soup.select_one('#main-content > main > div > a').attrs['href']
        inCitations = soup.select_one(
            '#main-content > main > article > div.c-article-header > div.c-article-metrics-bar__wrapper.u-clear-both > ul > li:nth-child(1) > p').text[
                      :-9]
        outCitations = len(soup.select_one('#Bib1-content > div > ol').find_all('li'))

        item['title'] = title
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

        #解析完成后将url加入已爬取目录
        with open(self.url_done_path, 'a', encoding='utf-8') as f:
            f.write(response.url + "\n")

        yield item
