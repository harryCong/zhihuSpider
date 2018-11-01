# -*- coding: utf-8 -*-
import json

import scrapy
from zhuhuSpider.items import zhihuItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']

    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    flower_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    flower_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    fans_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    fans_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield scrapy.Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        yield scrapy.Request(self.flower_url.format(user=self.start_user,include=self.flower_query,offset=0,limit=20),callback=self.parse_folwer)
        yield scrapy.Request(self.fans_url.format(user=self.start_user,include=self.fans_query,offset=0,limit=20),callback=self.parse_fans)


    def parse_user(self, response):
        result = json.loads(response.text)
        item = zhihuItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)

        yield item
        # print(response.text)
        yield scrapy.Request(self.flower_url.format(user=result.get("url_token"),include=self.flower_query,offset=0,limit=20),callback=self.parse_folwer)

        yield scrapy.Request(self.fans_url.format(user=result.get("url_token"),include=self.fans_query,offset=0,limit=20),callback=self.parse_fans)


    def parse_folwer(self, response):
        results = json.loads(response.text)

        if "data" in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            currut_user = results.get('paging').get('next').split('/')[4]
            # next_page = results.get('paging').get('next').split('&')[0] + '&' + results.get('paging').get('next').split('&')[2] + '&' + results.get('paging').get('next').split('&')[1]
            next_page = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}' + '&' + results.get('paging').get('next').split('&')[2] + '&' + results.get('paging').get('next').split('&')[1]
            page_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
            yield scrapy.Request(next_page.format(user=currut_user,include=page_query),callback=self.parse_folwer)
        # print(response.text

    def parse_fans(self, response):
        results = json.loads(response.text)

        if "data" in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            currut_user = results.get('paging').get('next').split('/')[4]
            # next_page = results.get('paging').get('next').split('&')[0] + '&' + results.get('paging').get('next').split('&')[2] + '&' + results.get('paging').get('next').split('&')[1]
            next_page = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}' + '&' + results.get('paging').get('next').split('&')[2] + '&' + results.get('paging').get('next').split('&')[1]
            page_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
            yield scrapy.Request(next_page.format(user=currut_user,include=page_query),callback=self.parse_fans)