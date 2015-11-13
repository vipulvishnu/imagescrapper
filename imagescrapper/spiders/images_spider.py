import scrapy

from lxml import html
from scrapy.http import Request
from imagescrapper.items import ImagescrapperItem


class ImagescrapperSpider(scrapy.Spider):
 name = "pixabay"
 domain = "https://pixabay.com/"
 start_urls = [
      "https://pixabay.com/"
  ]

 def parse(self, response):
   doc = html.fromstring(response.body)
   item = ImagescrapperItem()
   img_urls = []
   image_urls1 = doc.xpath('.//img/@src')
   image_urls2 = doc.xpath('.//img/@data-src')
   image_urls = image_urls1 + image_urls2
   for image_url in image_urls:
    if "https://" not in image_url:
      img_urls.append(self.domain + image_url)
    else:
      img_urls.append(image_url)
   item['image_url'] = img_urls
   yield item

   # Finding next urls
   next_urls = doc.xpath('.//a/@href')
   for next_url in next_urls:
    if "https://" not in next_url:
      next_url = self.domain + next_url
      yield Request(url=next_url)