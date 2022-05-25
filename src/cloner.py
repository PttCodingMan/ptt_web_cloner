import glob

import scrapy
from SingleLog.log import Logger

import utils

logger = Logger('Cloner')


# logging.getLogger('scrapy').setLevel(logging.WARNING)

class ClonerSpider(scrapy.Spider):
    name = 'Cloner'

    custom_settings = {
        # 'DOWNLOAD_DELAY': '2',
        'CONCURRENT_REQUESTS_PER_DOMAIN': '20',
    }

    def start_requests(self):
        self.start_link = 'https://www.ptt.cc/index.html'
        self.domain = 'https://www.ptt.cc/'

        self.visited = set()

        self.temp_files = [f"{self.domain}{f[7:]}" for f in glob.glob('./temp/**/*.html', recursive=True)]

        if self.temp_files:
            for temp_files in self.temp_files:
                logger.info('restore', temp_files)
                yield scrapy.Request(
                    url=temp_files,
                    callback=self.cloner,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0'
                    },
                    cookies={'over18': 'yes'}
                )
        else:
            yield scrapy.Request(
                url=self.start_link,
                callback=self.cloner,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0'
                },
                cookies={'over18': 'yes'}
            )

    def cloner(self, response: scrapy.http.Response):

        utils.save_temp(self.domain, response)

        urls = response.css('a::attr(href)').getall()

        for url in urls:
            if not url.startswith('/'):
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

        utils.save_page(self.domain, response)
