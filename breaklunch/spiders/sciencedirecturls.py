import scrapy


class SciencedirecturlsSpider(scrapy.Spider):
    name = 'sciencedirecturls'
    allowed_domains = ['sciencedirect.com']
    baseurl = 'https://www.sciencedirect.com'
    start_urls = ['https://www.sciencedirect.com']
    download_delay = 1

    def parse(self, response, **kwargs):

        journal_list_url = "https://www.sciencedirect.com/browse/" \
                           "journals-and-books?page={}" \
                           "&contentType=JL&accessType=openAccess "
        startpage = 2
        maxpage = 12
        for num in range(startpage, maxpage + 1, 1):
            yield scrapy.Request(journal_list_url.format(num),
                                 callback=self.parse_journal_list,
                                 dont_filter=False)

    def parse_journal_list(self, response):
        journal_list = response.xpath('// *[ @ id = "publication-list"] / li')
        for li in journal_list:
            link = li.xpath('./a/@href').extract_first()
            link = str(link)
            if link.startswith("/journal/"):
                yield scrapy.Request("https://www.sciencedirect.com/" + link,
                                     callback=self.parse_journal_page,
                                     dont_filter=False)

    def parse_journal_page(self, response):
        """
        latest_vol_link可能爬到两种格式
        /journal/addiction-neuroscience/vol/1/suppl/C
        /journal/actas-dermo-sifiliograficas-english-edition/vol/112/issue/10
        """
        latest_vol_link = response.xpath(
            '//a[@data-aa-name="latest-volume-issue"]/@href').extract_first()
        latest_vol_link = str(latest_vol_link)
        yield scrapy.Request(
            self.baseurl + latest_vol_link,
            callback=self.parse_journal_vol,
            dont_filter=False)

    def parse_journal_vol(self, response):
        print("parse_journal_vol called.", response.url)
        article_links = response.xpath(
            '//a[@class="anchor article-content-title '
            'u-margin-xs-top u-margin-s-bottom"]/@href').extract()
        for link in article_links:
            if "pii" in link:
                # 保存文章详情页url到文件 之后再爬
                item = {"article_link": link}
                yield item
            else:
                print("非法的文章详情页链接：" + link)

        # 递归调用 翻上一页
        prev_vol_link = response.xpath(
            '//a[ @ navname = "prev-next-issue"]/@href').extract_first()
        prev_vol_link = str(prev_vol_link)
        if prev_vol_link.startswith("/journal/"):  # 翻页到头的时候会空
            yield scrapy.Request(
                self.baseurl + prev_vol_link,
                callback=self.parse_journal_vol,
                dont_filter=False)
