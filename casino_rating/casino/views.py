#coding: utf-8
from casino.models import Slot
# from common.models import Comment, CONTENT_TYPE_BLOG
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.simple import direct_to_template


def slot_list(request):
    """
    Show list of last blogs entries
    """
    data = {}
    data["slot_list"] = Slot.objects.all()[:10]
    return direct_to_template(request, "casino/slots/index.html", data)


def slot_page(request, item_id):
    """
    Show single slot record
    """
    data = {}
    data["slot"] = get_object_or_404(Slot, pk=item_id)
    return direct_to_template(request, "casino/slots/entry.html", data)
