#coding:utf-8
from django import template
from django.utils.translation import ugettext as _
from old_site.models import CasinoArticle


register = template.Library()


class CasinoArticleSet(template.Node):
    """
    Node for load and structuring casino articles
    """
    def __init__(self, casino):
        """
        Constructor. Set input values info 
        """
        self.casino = casino

    def render(self, context):
        """
        Get list of groupped casino articles
        """
        casino = self.casino.resolve(context, True)

        article_list = {}
        for item in casino.casinoarticle_set.filter().order_by("type"):
            if not article_list.has_key(item.type):
                article_list[item.type] = {"title" : item.get_type_display(), "list" : []}
            article_list[item.type]["list"].append(item)

        context['article_list'] = article_list
        return ''


class CasinoScreenshotSet(template.Node):
    """
    Node for load and structuring casino articles
    """
    def __init__(self, casino):
        """
        Constructor. Set input values info 
        """
        self.casino = casino

    def render(self, context):
        """
        Get list of groupped casino articles
        """
        casino = self.casino.resolve(context, True)

        screenshot_list = {}
        for item in casino.casinoscreenshot_set.filter().order_by("type"):
            if not screenshot_list.has_key(item.type):
                screenshot_list[item.type] = {"title" : item.get_type_display(), "list" : []}
            screenshot_list[item.type]["list"].append(item)

        context['screenshot_list'] = screenshot_list
        return ''


@register.tag
def load_casino_articles(parser, token, *args, **kwargs):
    """
    Tag give casino articles list

    Example of using
    {% load_casino_articles casino %}

    `casino` must be Casino instance object
    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires one argument') % bits[0])
    casino = parser.compile_filter(bits[1])
    return CasinoArticleSet(casino)


@register.tag
def load_casino_screenshots(parser, token, *args, **kwargs):
    """
    Tag give casino screenshot list

    Example of using
    {% load_casino_screenshots casino %}

    `casino` must be Casino instance object
    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires one argument') % bits[0])
    casino = parser.compile_filter(bits[1])
    return CasinoScreenshotSet(casino)


