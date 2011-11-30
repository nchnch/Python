# -*- coding: utf8 -*-
import re
from django.contrib import messages
from django.utils.translation import ugettext as _

TOP_MENU = (("/slots/", _(u"Слоты"),), ("/casino/", _(u"Казино"),), ("/faq/", _(u"FAQ"),), )
MAIN_MENU = (("/slots/", _(u"Слоты"),), ("/casino/", _(u"Казино"),), ("/faq/", _(u"FAQ"),), )

def common(request):
    """
    Main context processor. Get user messages to template
    """
    data = {"TOP_MENU" : TOP_MENU, "MAIN_MENU" : MAIN_MENU}
    data["user_messages"] = messages.get_messages(request)

    current_url = request.path
    pos = current_url.find("/", 1)
    if -1 != pos:
        data["TOP_MENU_ACTIVE"] = current_url[:pos+1]

    return data