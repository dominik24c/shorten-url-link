import hashlib
import re

from django.conf import settings

from .exceptions import InvalidLengthOfGeneratedUrl

BASE_62 = 62


def get_base_62() -> str:
    lowercase_letters = 'a', 'z'
    uppercase_letters = 'A', 'Z'
    digits = '0', '9'
    base_62 = ''
    for s, e in [lowercase_letters, uppercase_letters, digits]:
        for i in range(ord(s), ord(e) + 1):
            base_62 += chr(i)

    return base_62


def generate_url(url: str) -> str:
    base_62 = get_base_62()
    hashed_url = hashlib.md5(url.encode()).hexdigest()
    length_of_hashed_url = len(hashed_url)
    counter = 0
    generated_url = ''

    if settings.LENGTH_OF_GENERATED_URL > length_of_hashed_url:
        raise InvalidLengthOfGeneratedUrl

    for i in range(settings.LENGTH_OF_GENERATED_URL):
        value = hashed_url[i]
        if '0' <= value <= '9':
            counter = (counter + ord(value) - ord('0')) % BASE_62
        else:
            counter = (counter + ord(value) - ord('a') + 10) % BASE_62

        generated_url += base_62[counter]

    return generated_url


def utilize_url(url: str) -> str | None:
    utilized_url = re.match('^(http(s|)://(www\.|)|www\.|)(.*)', url)
    if utilized_url is not None:
        return utilized_url.groups()[3]
