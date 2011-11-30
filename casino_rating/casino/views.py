#coding: utf-8
from casino.models import Game
# from common.models import Comment, CONTENT_TYPE_BLOG
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.simple import direct_to_template
from casino.models import Casino, Game


def casino_list(request):
    """
    Show list of casino
    """
    data = {}
    data["casino_list"] = Casino.objects.all()[:40]
    return direct_to_template(request, "casino/casino/index.html", data)


def casino_page(request, item_id):
    """
    Show single casino page
    """
    data = {}
    data["casino"] = get_object_or_404(Casino, pk=item_id)
    return direct_to_template(request, "casino/casino/entry.html", data)


def game_list(request):
    """
    Show list of games
    """
    data = {}
    data["game_list"] = Game.objects.all()[:40]
    return direct_to_template(request, "casino/games/index.html", data)


def game_page(request, item_id):
    """
    Show single game record
    """
    data = {}
    data["game"] = get_object_or_404(Game, pk=item_id)
    return direct_to_template(request, "casino/games/entry.html", data)
