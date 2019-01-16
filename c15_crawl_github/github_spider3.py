# -*- coding:utf-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
       return ('https://github.com/shiyanlou?tab=repositories', )

    def parse(self, response):
        for repo in response.css('li.public'):
            yield{
                'name': repo.css('h3 a::text').extract_first().strip(),
                'updated': repo.css('relative-time::attr(datetime)').extract_first()
            }
