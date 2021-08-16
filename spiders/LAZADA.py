import scrapy
from scrapy_splash import SplashRequest

from scrapy.crawler import CrawlerProcess


class LaptopSpider(scrapy.Spider):
    name = 'laptop'

    headers = {
        'accept': 'application/json, text/javascript',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.lazada.com.my',
        'referer': 'https://www.lazada.com.my/',
        'sec-ch-ua': '"Chromium"; v = "92", " Not A;Brand"; v = "99", "Google Chrome"; v = "92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    def start_requests(self):
        url1 = 'https://www.lazada.com.my/shop-laptops-gaming/?spm=a2o4k.home.cate_1_2.2.75f82e7e1Mg1X9'
        yield SplashRequest(
            url=url1,
            method='GET',
            callback=self.parse,
            endpoint='render.html',
            args={'wait': 0.5},
            dont_filter=True
        )

    def parse(self, response):
        products_selector = response.css('[data-tracking="product-card"]')
        for product in products_selector:
            nam = product.css('a[title]::attr(title)').get()
            print(nam)
            yield {
                'title': product.css('title').get(),
                'name': product.css('a[title]::attr(title)').get(),
                'price': product.css('span:contains("RM")::text').get()
            }


process = CrawlerProcess()
process.crawl(LaptopSpider)
process.start()
