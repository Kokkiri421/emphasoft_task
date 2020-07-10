import requests
from flask import current_app


def get_user_name(token):
    req = requests.get('https://api.vk.com/method/users.get?v=5.120&access_token=' + token).json()
    if 'error' in req:
        return {}, 400
    user = req['response'][0]
    return [user, 200]


def get_friends_names(token, count):
    req = requests.get('https://api.vk.com/method/friends.get?v=5.120&fields=name&count={}&access_token={}'
                       .format(count, token)).json()
    if 'error' in req:
        return {}, 400
    friend_list = req['response']['items']
    return [friend_list, 200]


class VkOAuth(object):
    def __init__(self):
        self.authorization_url = 'https://oauth.vk.com/authorize'
        self.client_id = 'client_id=' + current_app.config['CLIENT_ID']
        self.scope = 'scope=' + '+3+2+offline'
        self.redirect_uri = 'redirect_uri=' + current_app.config['REDIRECT_URI']
        self.response_type = 'response_type=code'
        self.version = 'v=5.120'

        self.recieve_url = 'https://oauth.vk.com/access_token'
        self.client_secret = 'client_secret=' + current_app.config['CLIENT_SECRET']

    def get_authorization_url(self):
        url = '{}?{}&{}&{}&{}&{}'.format(self.authorization_url, self.client_id, self.scope,
                                         self.redirect_uri, self.response_type, self.version)
        return url

    def get_receive_url(self, code):
        url = '{}?{}&{}&code={}&{}'.format(self.recieve_url, self.client_id,
                                           self.client_secret, code, self.redirect_uri)
        return url

