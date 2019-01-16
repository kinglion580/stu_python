# -*- coding: utf-8 -*-
import scrapy
from github.items import GithubItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains = ['github.com']

    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?tab=repositories', )

    def parse(self, response):
        for repo in response.css('li.public'):
            item = GithubItem({
                'name': repo.css('h3 a::text').extract_first().strip(),
                'update_time': repo.css('relative-time::attr(datetime)').extract_first()
            })
            url = response.xpath('.//a[contains(@itemprop,"codeRepository")]/@href')
            request = response.follow(url, callback=self.parse_detail)
            yield item

    def parse_detail(self, response):
            
