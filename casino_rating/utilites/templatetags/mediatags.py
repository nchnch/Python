#coding: utf-8
import settings
import Image
from django.template import Library
from os import path
from utils.media import image_thumbnail


register = Library()


@register.simple_tag
def thumbnail(value, size='200x200', default=""):
    """
    Filter for create thumbnail from image field
    """
    filename = value if isinstance(value, basestring) else value.name
    thumbnail = image_thumbnail(filename, size, ("photo", "images",))
    return thumbnail if thumbnail else default
