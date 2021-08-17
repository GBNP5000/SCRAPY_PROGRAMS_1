"""
        SOURCE-CODE 
    https://github.com/eupendra/scrapy_splash_demo
    
    https://www.youtube.com/watch?v=RgdaP54RvUM
"""

import scrapy
from scrapy_splash import SplashRequest

from scrapy.crawler import CrawlerProcess


class LaptopSpider(scrapy.Spider):
    name = 'laptop'

    def start_requests(self):
        url = 'https://www.lazada.com.my/shop-laptops-gaming/?spm=a2o4k.home.cate_1_2.2.75f82e7e1Mg1X9'
        yield SplashRequest(url)

    def parse(self, response):
        products_selector = response.css('[data-tracking="product-card"]')
        for product in products_selector:
            yield {
                'name': product.css('a[title]::attr(title)').get(),
                'price': product.css('span:contains("RM")::text').get()
            }


process = CrawlerProcess()
process.crawl(LaptopSpider)
process.start()
