import password as password
import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    def __init__(self, login, password, **kwargs):
        super().__init__(**kwargs)
        self.insta_login = login
        self.insta_pass = password

    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    user_parse = ['avznamensky', 'shtanudachi']
    api_url = 'https://i.instagram.com/api/v1/friendships/'
    status_info = ['following', 'followers']

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf})

    def user_login(self, response: HtmlResponse):
        print()
        j_body = response.json()
        if j_body['authenticated']:
            for user_p in self.user_parse:
                yield response.follow(f'/{user_p}',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': user_p})

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        info = {
            'count': 12
        }
        for status in self.status_info:
            url_posts = f'{self.api_url}{user_id}/{status}?{urlencode(info)}'
            yield response.follow(url_posts,
                                  callback=self.user_posts_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'info': deepcopy(info),
                                             'status': status},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                                  )

    def user_posts_parse(self, response: HtmlResponse, username, user_id, info, status):

        if response.status == 200:
            j_data = response.json()
            if j_data.get('big_list'):
                info['max_id'] = j_data.get('next_max_id')
                url_posts = f'{self.api_url}{user_id}/{status}?{urlencode(info)}'
                yield response.follow(url_posts,
                                      callback=self.user_posts_parse,
                                      cb_kwargs={'username': username,
                                                 'user_id': user_id,
                                                 'info': deepcopy(info),
                                                 'status': status},
                                      headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                                      )

            users = j_data.get('users')
            for user_info in users:
                item = InstaparserItem(parse_user_id=user_id,
                                       parse_username=username,
                                       user_id=user_info.get('pk'),
                                       user_name=user_info.get('username'),
                                       name=user_info.get('full_name'),
                                       picture=user_info.get('profile_pic_url'),
                                       status=status
                                       )
                yield item

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
