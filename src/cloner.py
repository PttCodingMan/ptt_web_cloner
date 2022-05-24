import scrapy
from SingleLog.log import Logger

import utils

logger = Logger('Cloner')


class ClonerSpider(scrapy.Spider):
    name = 'Cloner'

    def start_requests(self):
        self.start_link = 'https://www.ptt.cc/cls/1'
        self.domain = 'https://www.ptt.cc/'

        self.visited = set()

        yield scrapy.Request(
            url=self.start_link,
            callback=self.cloner,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0'
            },
            cookies={'over18': 'yes'}
        )

    def cloner(self, response: scrapy.http.Response):

        utils.save_page(self.domain, response)

        urls = response.css('a::attr(href)').getall()

        for url in urls:
            if not url.startswith('/'):
                continue
            if '/search?' in url:
                continue
            if url in self.visited:
                continue

            self.visited.add(url)

            yield scrapy.Request(
                url=f"{self.domain}{url}",
                callback=self.cloner,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0'
                },
                cookies={'over18': 'yes'}
            )
