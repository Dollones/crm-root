from unidecode import unidecode
from django.utils.text import slugify as dj_slugify


def slugify(value):
    return dj_slugify(unidecode(value))
