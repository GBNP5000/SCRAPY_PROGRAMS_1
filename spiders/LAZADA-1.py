"""
            SOURCE CODE GOT FROM
            
        https://stackoverflow.com/questions/56920623/how-do-i-scrape-this-kind-of-dynamic-generated-website-data
"""
import scrapy
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess


class DynamicSpider(scrapy.Spider):
    name = 'products'
    url = [
        'https://www.lazada.sg/products/esogoal-tactical-sling-bag-outdoor-chest-pack-shoulder-backpack-military-sport-bag-for-trekking-camping-hiking-rover-sling-daypack-for-men-women-i204814494-s353896924.html?mp=1',
        'https://www.lazada.sg/products/esogoal-2-in-1-selfie-stick-tripod-bluetooth-selfie-stand-with-remote-shutter-foldable-tripod-monopod-i279432816-s436738661.html?mp=1',
        'https://www.lazada.sg/products/esogoal-selfie-stick-tripod-extendable-selfie-stick-monopod-with-integrated-tripod-and-bluetooth-remote-shutter-wireless-selfie-stick-tripod-for-cellphonecameras-i205279097-s309050125.html?mp=1',
        'https://www.lazada.sg/products/esogoal-mini-umbrella-travel-umbrella-sun-rain-umbrella8-ribs-98cm-big-surface-lightweight-compact-parasol-uv-protection-for-men-women-i204815487-s308312226.html?mp=1',
        'https://www.lazada.sg/products/esogoal-2-in-1-selfie-stick-tripod-bluetooth-selfie-stand-with-remote-shutter-foldable-tripod-monopod-i279432816-s436738661.html?mp=1',
    ]

    script = """
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(1.5))
          return {
            html = splash:html()
          }
        end
    """

    def start_requests(self):
        for link in self.url:
            yield SplashRequest(
                url=link,
                callback=self.parse,
                endpoint='execute',
                args={'wait': 0.5, 'lua_source': self.script},
                dont_filter=True,
            )

    def parse(self, response):
        yield {
            'title': response.xpath("//span[@class='pdp-mod-product-badge-title']/text()").extract_first(),
            'price': response.xpath("//span[contains(@class, 'pdp-price')]/text()").extract_first(),
            'description': response.xpath("//div[@id='module_product_detail']/h2/text()").extract_first()
        }


process = CrawlerProcess()
process.crawl(DynamicSpider)
process.start()
