# -*- coding:utf-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repo in response.css('li.public'):
            yield{
                'name': repo.css('h3 a::text').extract_first().strip(),
                'updated': repo.css('relative-time::attr(datetime)').extract_first()
            }
