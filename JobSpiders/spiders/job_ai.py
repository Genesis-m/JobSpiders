# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse  # 如果url不是完整的就加上这个
import re
from JobSpiders.items import Job51Item, Job51ItemLoader
from JobSpiders.utils.common import get_md5
from datetime import datetime
from JobSpiders.utils.parse_detail import parse_detail_utils

class JobAiSpider(scrapy.Spider):
    name = 'job_ai'
    allowed_domains = ['jobs.51job.com', 'search.51job.com']
    start_urls = ['https://search.51job.com/list/000000%252C00,000000,0000,00,9,99,%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD,2,1.html']


    def parse(self, response):
        # 1获取到每一条招聘的url并将url给具体的解析函数进行解析字段
        all_url = response.xpath('//*[@id="resultList"]//div/p/span/a/@href').extract()
        for one_url in all_url:
            yield Request(url=parse.urljoin(response.url, one_url), callback=self.parse_detail, )

        # 2获取下一页的url并交给scrapy下载
        next_url = response.xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[8]/a/@href').extract_first("")
        if next_url:
            # yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        yield parse_detail_utils(self, response, '人工智能')
