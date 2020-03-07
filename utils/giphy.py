import re
import random
import requests
from urllib import parse
from settings import GIPHY_KEY


HELP_MSG = [
    'giphy 에서 움짤을 검색하고 싶으면 \'!움짤 [검색어]\' 이라고 해주세요.',
    '검색어는 `영어`만 됩니다. 검색어에 띄어쓰기가 들어있다면 큰따옴표로 감싸주세요.',
]

URL = 'http://api.giphy.com/v1/gifs/search?'


def get_giphy_image_url(query):
    params = {
        'q': query,
        'api_key': GIPHY_KEY,
        'offset': random.randint(0, 100),
        'limit': 1,
    }
    data = requests.get(URL, params=params).json()

    if data['pagination']['count'] < 1:
        return None
    else:
        el = data['data'][0]
        return el['images']['downsized']['url']
