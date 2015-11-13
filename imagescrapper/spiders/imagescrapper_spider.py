import scrapy

from lxml import html




class ImagescrapperSpider(scrapy.Spider):
    name = "pixabay"
    allowed_domains = ["pixabay.com"]
    start_urls = [
        "https://pixabay.com/"
    ]

    def parse(self, response):
        urls = []
        doc = html.fromstring(response.body)
        image_urls1 = doc.xpath('.//img/@src')
        image_urls2 = doc.xpath('.//img/@data-src')
        next_urls = doc.xpath('.//a/@href')
        domain = self.allowed_domains[0]
        for url in next_urls:
          if domain in url:
            urls.append(url)
        # print 'dddddddddddddd\n\n\n\n\n\n', urls
        # filename = response.url.split("/")[-2] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)