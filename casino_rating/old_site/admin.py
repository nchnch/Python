# -*- coding: utf-8 -*-
from old_site.models import Country, ParameterGroup, Casino, Parameter, CasinoScreenshot,\
    ParameterToCasino
from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _


class ParameterToCasinoInline(admin.TabularInline):
    model = ParameterToCasino
    extra = 0


class CasinoScreenshotInline(admin.TabularInline):
    model = CasinoScreenshot
    extra = 0


class CasinoAdmin(admin.ModelAdmin):
    '''
    fieldsets = (
        (_(u"Основное инфо"), {"fields" : ("name", "urlkey", "domain", "similar_sale", "status", 
            "relation", "link_similar_sale",)}),
        (_(u"Связи"), {"fields" : ("developers", )}), 
        (_(u"Параметры"), {"fields" : ("param_mobile", "param_browser", "param_download", 
            "param_audited", "param_license", "param_jackpot",
            "param_tournaments", "param_nodepositbonus",)}),
        (_(u"Сортировка"), {"fields" : ("order_hand", "order_hand_date", )}),
    )
    '''
    inlines = (CasinoScreenshotInline, ParameterToCasinoInline, )
    list_display = ("name", "domain", "accept", "otstoy")
    # list_display_links = ("name",)
    list_filter = ("country", "otstoy", "accept", )
    ordering = ("id", "enabled", )
    search_fields = ("name", "domain", )
    save_on_top = True


class ParameterGroupAdmin(admin.ModelAdmin):
    """
    Admin class for parameters groups
    """
    search_fields = ("name",  )
    list_display = ("name", "meta", "order", )
    # list_display_links = ("name",)
    # list_filter = ("type",)
    # inlines = (BaseGameInfoInline, )
    # filter_horizontal = ('similarcasino', 'othercasino', )
    ordering = ("order", )
    save_on_top = True


class ParameterAdmin(admin.ModelAdmin):
    """
    Admin class for Parameter models
    """
    search_fields = ("name",)
    list_display = ("name",  "group", "type", "order")
    # list_display = ("morelinks", "name", "gametype", "enabled", )
    # list_display_links = ("name",)
    list_filter = ("group", "type",)
    # inlines = (BaseGameInfoInline, )
    # filter_horizontal = ('similarcasino', 'othercasino', )
    # ordering = ("group", "order", )
    save_on_top = True


admin.site.register(Country)
admin.site.register(ParameterGroup, ParameterGroupAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Casino, CasinoAdmin)
