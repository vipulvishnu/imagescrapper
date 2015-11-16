# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagescrapperItem(scrapy.Item):
    """
    Items defined here.
    """
    image_url = scrapy.Field()
    alt_text = scrapy.Field()

