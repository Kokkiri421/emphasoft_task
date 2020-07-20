import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout


def index(request):
    context = {}
    if request.user.is_authenticated:
        try:
            token = request.user.social_auth.get(provider='vk-oauth2').extra_data['access_token']
            req = requests.get('https://api.vk.com/method/friends.get?v=5.120&fields=name&count=5&access_token={}'
                               .format(token)).json()['response']['items']
            context['friend_list'] = req
        except KeyError:
            auth_logout(request)

    return HttpResponse(render(request, 'index.html', context))



