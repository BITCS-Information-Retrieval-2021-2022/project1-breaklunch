import scrapy


class SpringerSpider(scrapy.Spider):
    name = 'springer'
    #计划爬取的域名列表，不在其中的无法爬取
    allowed_domains = ['springeropen.com']
    #start_urls = ['https://www.springer.com/cn']
    #未爬取的url
    url_path="breaklunch/List/springer.txt"
    #已爬取的url
    url_done_path="breaklunch/List/springer_done.txt"

    def parse(self, response):
        
        #未爬取/已爬取的url
        url_list=[]
        url_done_list=[]
        
        #读取url目录
        with open(self.url_path,'r',encoding='utf-8') as f:
            url_list=f.readlines()
        with open(self.url_done_path,'r',encoding='utf-8') as f:
            url_done_list=f.readlines()
        
        #按照列表顺序爬取
        for url in url_list:
            if url not in url_done_list:        
                yield scrapy.Request(url,callback=self.parse_page,dont_filter=False)
            
    #每个网址的解析
    def parse_page(self,response):
        pass

        #解析完成后将url加入已爬取目录
        with open(self.url_done_path,'a',encoding='utf-8') as f:
                f.write(response.url+"\n")

