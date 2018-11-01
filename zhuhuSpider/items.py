# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class zhihuItem(Item):

    id = Field()
    name = Field()
    headline = Field()
    avatar_url = Field()
    follower_count = Field()
    url_token = Field()
    answer_count = Field()
    articles_count = Field()
    gender = Field()
    user_type = Field()
    url = Field()
    vip_info = Field()


