# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiCompaniesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    hq = scrapy.Field()
    link = scrapy.Field()
    revenue = scrapy.Field()
    employee = scrapy.Field()
    # website = scrapy.Field()
    op_income = scrapy.Field()
    net_income = scrapy.Field()
    total_assets = scrapy.Field()
    total_equity = scrapy.Field()
    website = scrapy.Field()

