import scrapy

from env import game


class GameSpider(scrapy.Spider):
    name = 'game'
    allowed_domains = game['domain']

    cookies = game['cookies']
    url = game['url']
    aids = game['aids']

    download_delay = 2
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        #'COOKIES_DEBUG': True,
        #'JOBDIR': 'crawls/game',
        'ITEM_PIPELINES': {
            'scrapy_project.pipelines.GamePipeline': 300
        }
    }

    def start_requests(self):
        for aid in self.aids:
            yield scrapy.Request(self.url + str(aid), cookies=self.cookies)

    def parse(self, response):
        downlink = response.css('tr:first-child a::attr(href)').get()

        if downlink is not None:
            cdk = response.css('tr:last-child > td:last-child').re_first(
                '\d{6}')

            gift = response.css('tr:nth-child(2) a::attr(href)').get().strip()
            if gift == '敬请期待':
                gift = None

            yield {
                'id': response.url.split('?aid=')[1],
                'download': downlink.strip(),
                'gift': gift,
                'cdk': cdk
            }
