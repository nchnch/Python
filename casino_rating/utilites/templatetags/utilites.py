#coding:utf-8
from django.template import Library
from settings import STATIC_URL


DESC_ICO = "%simages/arrow-down.png" % STATIC_URL
ASC_ICO = "%simages/arrow-up.png" % STATIC_URL


register = Library()


@register.simple_tag
def order_icon(field, ordering, asc_ico=ASC_ICO, desc_ico=DESC_ICO):
    """
    Get image for show ordering icon
    """
    return desc_ico if ordering == ("-%s" % field) else asc_ico


@register.simple_tag
def order_string(field, ordering, key="s", mode_key="mode"):
    """
    Get string for needed order mode
    `field` - field for what apply sorting
    `ordering` - current ordering field
    `key` - key which contains order field name
    `mode_key` - key which contains mode of ordering
    """
    return "%s=%s&%s=%s" % (key, field, mode_key, "asc" if ordering == ("-%s" % field) else "desc")

# @register.filter
