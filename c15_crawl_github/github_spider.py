# -*- coding:utf-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.xpath('//li[@itemprop="owns"]'):
            yield{
                'name': repository.css('h3 a::text').extract_first().strip(),
                'updated': repository.css('relative-time::attr(datetime)').extract_first()
            }
