from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from spider.items import DoubanItem


class DoubanSpider(RedisCrawlSpider):
    name = "douban"
    redis_key = "douban:start_urls"

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=('//div[@class="paginator"]/a')),
            callback='parse',
            follow=True
        ),
    )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop("domain", "douban.com")
        self.allowed_domains = filter(None, domain.split(','))
        super().__init__(*args, **kwargs)

    def parse(self, response):
        movies = response.xpath('//li/div[@class="item"]')
        for movie in movies:
            item = DoubanItem()
            a = movie.xpath('.//div[@class="hd"]/a[1]')[0]
            item['detail'] = a.xpath('@href').extract_first()
            item['title'] = ''.join(a.xpath('span/text()').extract()).strip()
            item['info'] = movie.xpath('.//div[@class="bd"]/p[1]/text()').extract_first().strip()
            item['star'] = movie.xpath('.//span[@class="rating_num"]/text()').extract_first().strip()
            item['comment'] = movie.xpath('.//div[@class="star"]/span[last()]/text()').extract_first().strip()
            yield item
