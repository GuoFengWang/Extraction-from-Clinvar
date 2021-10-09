# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OrphanetcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    #disease = scrapy.Field()
    prevalence = scrapy.Field()
    #inheritance = scrapy.Field()
    onset_age = scrapy.Field()
    omim = scrapy.Field()
    disease_def = scrapy.Field()
    synonym = scrapy.Field()


