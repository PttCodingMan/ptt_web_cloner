import glob
import os.path
import re

import scrapy
from SingleLog.log import Logger

import utils

logger = Logger('Cloner')


# logging.getLogger('scrapy').setLevel(logging.WARNING)

class ClonerSpider(scrapy.Spider):
    name = 'Cloner'

    custom_settings = {
        # 'DOWNLOAD_DELAY': '0.1',
        'CONCURRENT_REQUESTS_PER_DOMAIN': '100',
        'COOKIES_ENABLED': 'True',
    }

    def start_requests(self):
        self.board = 'DramaTalk'
        self.start_link = f'https://www.ptt.cc/bbs/{self.board}/index.html'
        self.domain = 'https://www.ptt.cc/'

        self.visited = set()

        self.index_pattern = re.compile(r'/bbs/DramaTalk/index[\d]*.html')

        yield scrapy.Request(
            url=self.start_link,
            callback=self.cloner,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
            },
            cookies={'over18': '1'}
        )

    def cloner(self, response: scrapy.http.Response):

        utils.save_page(self.domain, response, temp=False)

        if self.index_pattern.search(response.url):
            urls = response.css('a::attr(href)').getall()

            for url in urls:
                if not url.startswith(f'/bbs/{self.board}/'):
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
                    cookies={'over18': '1'}
                )


