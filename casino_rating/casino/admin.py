# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _
from casino.models import Slot, Roulette, Developer, Casino, CasinoInfo, CasinoImage, \
    CasinoArticle, GameImage, GameInfo, GameToCasino


class GameToCasinoInline(admin.StackedInline):
    model = GameToCasino
    extra = 1


class CasinoInfoInline(admin.StackedInline):
    model = CasinoInfo
    extra = 1
    fieldsets = (
        (_(u"Основное"), {"fields" : ("lang", "name", "image", "description", "text")}),
        (_(u"Партнерские ссылки"), {"fields" : ("purl_main", "purl_download", "purl_bonus", )}),
    )


class CasinoImageInline(admin.TabularInline):
    model = CasinoImage
    extra = 1


class CasinoArticleInline(admin.StackedInline):
    model = CasinoArticle
    extra = 1


class CasinoAdmin(admin.ModelAdmin):
    fieldsets = (
        (_(u"Основное инфо"), {"fields" : ("name", "urlkey", "domain", "similar_sale", "status", 
            "link_similar_sale",)}),
        (_(u"Связи"), {"fields" : ("developers", "paymentsystems",)}), 
        # (_(u"Партнерские ссылки"), {"fields" : ("name", )}),
        (_(u"Параметры"), {"fields" : ("param_mobile", "param_browser", "param_audited", "param_integrity",
            "param_license", "param_shift", "param_jackpot", "param_dealer", "param_multiplayer", 
            "param_tournaments", "param_nodepositbonus",)}),
        (_(u"Сортировка"), {"fields" : ("order_hand", "order_hand_date", )}),
    )
    inlines = (CasinoInfoInline, CasinoImageInline, CasinoArticleInline, GameToCasinoInline,)
    filter_horizontal = ('developers', 'paymentsystems', )
    list_display = ("name", "domain", "enabled", )
    list_filter = ("enabled", "status", )
    ordering = ("enabled", )
    search_fields = ("name", "domain", )


class GameInfoInline(admin.StackedInline):
    model = GameInfo
    extra = 1


class GameImageInline(admin.TabularInline):
    model = GameImage
    extra = 1


class GameAdmin(admin.ModelAdmin):
    """
    """
    _params = None
    search_fields = ("name",  )
    list_display = ("name", "enabled", )
    list_filter = ("enabled", )
    inlines = (GameInfoInline, GameImageInline, GameToCasinoInline,)
    filter_horizontal = ('developers', )
    ordering = ("enabled", )


class SlotAdmin(GameAdmin):
    """
    """
    _params = ('param_numberlines', 'param_numberdrums', )
    fieldsets = (
        (_(u"Основное инфо"), {'fields': ('name', 'gametype', 'screenshot', 'developers', 'maincasino', )}),
        (_(u"Параметры"), {'fields': ('param_sale', 'param_gambling', 'param_offline', 'param_mobile', 
            'param_integrity', 'param_jackpot', 'param_numberlines', 'param_numberdrums', )}),
        (_(u"Сортировка"), {'fields': ('order_hand', 'order_hand_date', )}),
        (_(u"Настройки Flash"), {'fields': ('flash_width', 'flash_height', 'flash_enabled', 
            'flash_inframe', )}),
    )
# SlotAdmin.fieldsets = list(GameAdmin.fieldsets)
# SlotAdmin.fieldsets[1][1]["fields"] += SlotAdmin._params


class RouletteAdmin(GameAdmin, admin.ModelAdmin):
    """
    """
    _params = ('param_minbet', 'param_maxbet', 'param_ratio', )
    fieldsets = (
        (_(u"Основное инфо"), {'fields': ('name', 'gametype', 'screenshot', 'developers', 'maincasino', )}),
        (_(u"Параметры"), {'fields': ('param_sale', 'param_gambling', 'param_offline', 'param_mobile', 
            'param_integrity', 'param_jackpot', 'param_minbet', 'param_maxbet', 'param_ratio', )}),
        (_(u"Сортировка"), {'fields': ('order_hand', 'order_hand_date', )}),
        (_(u"Настройки Flash"), {'fields': ('flash_width', 'flash_height', 'flash_enabled', 
            'flash_inframe', )}),
    )
# RouletteAdmin.fieldsets = list(GameAdmin.fieldsets)
# RouletteAdmin.fieldsets[1][1]["fields"] += RouletteAdmin._params


admin.site.register(Developer)
admin.site.register(Casino, CasinoAdmin)

admin.site.register(Slot, SlotAdmin)
admin.site.register(Roulette, RouletteAdmin)

'''
admin.site.register(CatalogFlowers, CatalogFlowersAdmin)
admin.site.register(CatalogGifts, CatalogGiftsAdmin)
admin.site.register(CatalogCards, CatalogCardsAdmin)
admin.site.register(GoodFlower, GoodFlowerAdmin)
admin.site.register(GoodGift, GoodGiftAdmin)
admin.site.register(GoodCard, GoodCardAdmin)
admin.site.register(Occasion, OccasionAdmin)
admin.site.register(GoodPriceFilter)



'''