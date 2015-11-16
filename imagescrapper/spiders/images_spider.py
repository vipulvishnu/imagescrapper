import re
from urlparse import urlparse

from lxml import html

import scrapy
from scrapy.http import Request

from imagescrapper.items import ImagescrapperItem


class BaseSpider(scrapy.Spider):
    """
    Base spider that help you crawl all images
    through out the domain given in start urls
    """
    name = "sayone.images" # over ride with your spider name

    start_urls = [
        "http://sayonetech.com/"
    ]  # over ride to scrape your website

    # allowed_domains = ['sayonetech.com', ]

    allowed_domains = []
    banned_responses = [404, 500, ]

    def __init__(self):
        super(BaseSpider, self).__init__()
        self.domain = self.__get_domain_with_schema()
        self.__set_allowed_domain_from_start_url()

    def __set_allowed_domain_from_start_url(self):
        self.allowed_domains.append(urlparse(self.domain).netloc)

    def __get_domain_with_schema(self):
        """
        Get the domain name with schema
        :return: String
        """
        parsed_uri = urlparse(self.start_urls[0])
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain

    def __avoid_unwanted_responses(self, status):
        """
        Checks for valid responses
        :param status:
        :return: Boolean
        """
        if status in self.banned_responses:
            return False
        return True

    def parse(self, response):
        """
        Parses the main html response
        :param response:
        :return:
        """
        if self.__avoid_unwanted_responses(response.status):
            doc = html.fromstring(response.body)

            item = ImagescrapperItem()
            for image_url in self.get_images_logic(doc):
                item['image_url'] = image_url
                yield item

            # Get the next urls
            next_urls = doc.xpath('.//a/@href')
            for url in next_urls:
                url = self._make_up_url(url)
                if not url:
                    continue
                next_url = self._apply_schema_to_url(url)
                yield Request(url=next_url)

    def _make_up_url(self, url):
        url_object = urlparse(url)
        if (not(url_object.scheme) or not(url_object.netloc)) and url_object.path:
            if re.search('(/.+?/)', url_object.path):
                return self.domain+url_object.path
        return url

    def _apply_schema_to_url(self, url):
        """
        Applies schema to urls fed.
        :param url: String
        :return: String
        """
        if not urlparse(url).scheme:
            #Applied default scheme if no scheme found
            return urlparse(url)._replace(scheme='http').geturl()

        return url

    def get_images_logic(self, doc):
        """
        Get all images logic

        :param doc:
        :return: List
        """
        image_urls = doc.xpath('.//img/@src') + doc.xpath('.//img/@data-src')
        for image_url in image_urls:
            current_url_index = image_urls.index(image_url)
            if self.image_url_validation(image_url):
                parsed_uri = urlparse(image_url)
                if not parsed_uri.netloc:
                    image_url = '{domain}{uri.path}'.format(domain=self.domain, uri=parsed_uri)
                image_urls[current_url_index] = self._apply_schema_to_url(image_url)
            else:
                # Remove the invalid urls form the
                image_urls.pop(current_url_index)

        return image_urls

    def image_url_validation(self, image_url):
        """
        Different cases of image url validation
        :param url:  String
        :return: Boolean
        """
        FLAG = True

        #CASE 1
        if 'blank' in image_url:
            FLAG = False

        #CASE 2 #TODO for future scope

        return FLAG
