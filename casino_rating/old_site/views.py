#coding: utf-8
# from common.models import Comment, CONTENT_TYPE_BLOG
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.simple import direct_to_template
from old_site.models import Casino


PER_PAGE_LIST = (5, 10, 20, 50)
DEFAULT_PER_PAGE = 20


def index(request, nonslash=None):
    """
    Show list of casino
    """
    if nonslash:
        return HttpResponseRedirect("/")

    data = {}
    casino_list = Casino.objects.filter(enabled=True, accept=True).order_by("-rating", "id")
    if len(casino_list):
        data["max_rating"] = casino_list[0].rating

    try:
        page = int(request.GET.get('page'))
    except Exception:
        page = 1

    try:
        per_page = int(request.GET.get('per_page'))
        if per_page not in PER_PAGE_LIST:
            raise
        if per_page != DEFAULT_PER_PAGE:
            data["add_page_url"] = "&per_page=%s" % per_page
    except Exception:
        per_page = DEFAULT_PER_PAGE

    paginator = Paginator(casino_list, per_page)
    try:
        casinos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        casinos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        casinos = paginator.page(paginator.num_pages)
    
    data["casino_list"] = casinos
    data["current_page"] = page
    data["per_page"] = per_page
    data["PER_PAGE_LIST"] = PER_PAGE_LIST
    return direct_to_template(request, "old_site/index.html", data)


def casino(request):
    """
    Show single casino page
    """
    try:
        item_id = int(request.GET.get("cid", None))
    except Exception:
        raise Http404
    data = {}
    data["casino"] = get_object_or_404(Casino, pk=item_id)
    return direct_to_template(request, "old_site/casino.html", data)
