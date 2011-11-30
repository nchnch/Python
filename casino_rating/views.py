#coding: utf-8
from django.views.generic.simple import direct_to_template
from django.http import Http404, HttpResponseRedirect, HttpResponse


def home(request):
    """
    Site index page
    """
    data = {}
    return direct_to_template(request, 'index.html', data)

