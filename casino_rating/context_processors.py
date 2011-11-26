# -*- coding: utf8 -*-
import re
from django.contrib import messages
# from profile import USER_MENU

# TOP_MENU = (("/tape/", u"Лента",), ("/poster/", u"Афиша",), ("/sitetop/", u"Сайтоп",), 
# ("/artwork/", u"Творчество",), ("/photo/", u"Фото",), ("/rating/", u"Люди",), )

def common(request):
    """
    Main context processor. Get user messages to template
    """
    data = {}
    # current_url = request.path
    # data = {"TOP_MENU" : TOP_MENU, "USER_MENU" : USER_MENU,}
    # pos = current_url.find("/", 1)
    # if -1 != pos:
        # data["TOP_MENU_ACTIVE"] = current_url[:pos+1]

    data["user_messages"] = messages.get_messages(request)
    return data