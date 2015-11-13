import scrapy

from lxml import html
from urlparse import urlparse
from scrapy.http import Request
from imagescrapper.items import ImagescrapperItem


class ImagescrapperSpider(scrapy.Spider):
  name = "pixabay"

  start_urls = [
      "https://pixabay.com/en/photos/?order=best&cat=feelings"
  ]

  def parse(self, response):
    parsed_uri = urlparse(response.url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    doc = html.fromstring(response.body)
    item = ImagescrapperItem()
    img_urls = self.get_images(doc, domain)
    item['image_url'] = img_urls
    yield item

    # Get the next urls
    next_urls = doc.xpath('.//a/@href')
    for url in next_urls:
      next_url = self.get_urls_logic(url, domain)
      yield Request(url=next_url)

  def get_urls_logic(self, url, domain):
    if 'http' not in url:
      url = domain + url
      return url
    else:
      return url

  def get_images(self, doc, domain):
    img_urls = []
    image_urls1 = doc.xpath('.//img/@src')
    image_urls2 = doc.xpath('.//img/@data-src')
    image_urls = image_urls1 + image_urls2
    for image_url in image_urls:
      if 'blank' not in image_url:
        img_urls.append(self.get_urls_logic(image_url, domain))
    return img_urls
