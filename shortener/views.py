from random import choice
import re
import string
import urllib.parse

import django.core.exceptions
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import URLShortener


def index(request):
    if request.method == 'GET':
        data = {'shorten': ''}
    elif request.method == 'POST':
        body_decoded = request.body.decode('utf-8')
        body = urllib.parse.parse_qs(body_decoded)
        data = {'shorten': ''}

        url_regex = re.compile(r'^https?://')
        try:
            if url_regex.match(body['url'][0]):
                shorten_id = ''.join([choice(string.ascii_letters) for i in range(8)])
                while True:
                    try:
                        URLShortener.objects.get(shorten_id=shorten_id)
                    except django.core.exceptions.ObjectDoesNotExist:
                        URLShortener.objects.create(origin_url=body['url'][0], shorten_id=shorten_id)
                        data['shorten'] = 'http://localhost:8000/' + shorten_id
                        break
            else:
                data['error'] = 'Please enter valid URL.'
        except KeyError:
            data['error'] = 'Error occured. Please retry.'

    return render(request, 'shortener/index.html', data)


def reverse(request, url_id):
    urlobj = get_object_or_404(URLShortener, shorten_id=url_id)
    next_url = urlobj.origin_url
    response = HttpResponse(status=301)
    response['Location'] = next_url
    return response
