#coding: utf-8
# from django.contrib.auth.models import User
from django.views.generic.simple import direct_to_template
from django.http import Http404, HttpResponseRedirect, HttpResponse
# from materials.models import Tape, Poster, Sitetop, Artwork, CONTENT_MODELS_CLASSES


def home(request):
    """
    Site index page
    """
    data = {}
    return direct_to_template(request, 'index.html', data)

