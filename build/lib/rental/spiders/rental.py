# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re


class RentalSpider(scrapy.Spider):
    # name of spider
    name = 'rental'
    # list of allowed domains
    allowed_domains = ['gayshare.com.au']
    # starting urls
    start_urls = [
        'https://www.gayshare.com.au/share-accommodation/newtown-2042',
        'https://www.gayshare.com.au/share-accommodation/parramatta'
    ]

    # after every successful crawl parse is called
    def parse(self, response):
        # get all the listing blocks
        listings = response.xpath('//a[@class="col-xs-12 profitem"]').getall()

        # within each listing block get the details
        for i in listings:
            # there is more than 1 heading or suburb, just get the first one
            suburb = Selector(text=i).xpath('//h4[@class="mat-header"]/text()').get().strip()
            # new or updated listing
            status = Selector(text=i).xpath('//span[@class="mat-text-span text-uppercase mat-new hidden-xs"]/text()').get()

            # price
            price = Selector(text=i).xpath('//h4[@class="mat-header mat-price"]').get()
            # some regex to extract the price
            loc = re.search("</sup>",price)
            price = price[loc.span()[1]:]
            price = price.replace('<sup>','')
            price = price.replace('</sup>','')
            price = price.replace('</h4>','')
            price = re.sub('\xa0',' ',price)
            price = price.strip()

            # get all feature details in a list
            details = Selector(text=i).xpath('//ul[@class="mat-feture"]/li/div[@class="mat-fetaure-avl"]/text()').getall()
            # listing details
            home_type = details[0].strip()
            available = details[1].strip()
            occupants = details[2].strip()

            # get description
            desc = Selector(text=i).xpath('//div[@class="col-sm-4 col-md-6 hidden-xs hidden-sm mathes-list"]/p/text()').get().strip()
            desc = desc.replace('\r','')
            desc = desc.replace('\n','')

            listing = {
                'suburb' : suburb,
                'status' : status,
                'price' : price,
                'home_type' : home_type,
                'available' : available,
                'occupants' : occupants,
                'description': desc,
            }
            yield(listing)


        # good reference - https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
