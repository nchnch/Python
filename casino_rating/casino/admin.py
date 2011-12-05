# -*- coding: utf-8 -*-
from casino.models import ParagraphCategory, Game, Developer, Casino, CasinoInfo, CasinoImage, \
    CasinoToPaymentSystem, CasinoArticle, CasinoParagraph, GameImage, GameInfo, GameParagraph, \
    GameToCasino, BaseGame, BaseGameInfo, BaseGameParagraph
from django.contrib import admin
# from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext as _
from utilites.admin_models import ModifyModelAdmin
# from versioner.admin_models import ModelAdmin as VersionModelAdmin


class CasinoToPaymentSystemInline(admin.TabularInline):
    model = CasinoToPaymentSystem
    extra = 0


class GameToCasinoInline(admin.StackedInline):
    model = GameToCasino
    extra = 1


class CasinoInfoInline(admin.StackedInline):
    model = CasinoInfo
    extra = 0
    fieldsets = (
        (_(u"Основное"), {"fields" : ("lang", "name", "image", "description", )}),
        (_(u"Партнерские ссылки"), {"fields" : ("purl_main", "purl_download", "purl_bonus", )}),
    )


class CasinoImageInline(admin.TabularInline):
    model = CasinoImage
    extra = 0


class CasinoArticleInline(admin.StackedInline):
    model = CasinoArticle
    extra = 0


class CasinoParagraphInline(admin.StackedInline):
    model = CasinoParagraph
    extra = 0


class CasinoAdmin(ModifyModelAdmin): #VersionModelAdmin, 
    fieldsets = (
        (_(u"Основное инфо"), {"fields" : ("name", "urlkey", "domain", "similar_sale", "status", 
            "relation", "link_similar_sale",)}),
        (_(u"Связи"), {"fields" : ("developers", )}), 
        (_(u"Параметры"), {"fields" : ("param_mobile", "param_browser", "param_download", 
            "param_audited", "param_license", "param_jackpot",
            "param_tournaments", "param_nodepositbonus",)}),
        (_(u"Сортировка"), {"fields" : ("order_hand", "order_hand_date", )}),
    )
    inlines = (CasinoInfoInline, CasinoToPaymentSystemInline, )#GameToCasinoInline,
    filter_horizontal = ('developers', )
    list_display = ("morelinks", "name", "domain", "relation", "status", "enabled", )
    list_display_links = ("name",)
    list_filter = ("developers", "enabled", "status", "relation", )
    ordering = ("enabled", )
    search_fields = ("name", "domain", )
    save_on_top = True
    inlines_formsets_pages = (
        (_(u"Список статей"), "articles", {"models" : (CasinoArticleInline,)}),
        (_(u"Параграфы"), "paragraphs", {"models" : (CasinoParagraphInline,)}),
        (_(u"Скриншоты"), "screenshots", {"models" : (CasinoImageInline,)}),
    )


class BaseGameInfoInline(admin.StackedInline):
    model = BaseGameInfo
    extra = 0


class BaseGameParagraphInline(admin.StackedInline):
    model = BaseGameParagraph
    extra = 0


class BaseGameAdmin(ModifyModelAdmin):
    """
    Admin class for BaseGame models
    """
    fieldsets = (
        (_(u"Основное инфо"), {'fields': ('name', 'gametype', 'screenshot', 'othercasino', 'similarcasino', 
            'rating',)}),
        (_(u"Параметры"), {'fields': ('param_offline', 'param_rare',)}),
        (_(u"Параметры слотов"), {'fields': ('param_numberlines', 'param_numberdrums', )}),
        # (_(u"Параметры рулетки"), {'fields': ('param_minbet', 'param_maxbet', 'param_ratio', )}),
        (_(u"Сортировка"), {'fields': ('order_hand', 'order_hand_date', )}),
    )
    search_fields = ("name",  )
    list_display = ("morelinks", "name", "gametype", "enabled", )
    list_display_links = ("name",)
    list_filter = ("othercasino", "enabled", "gametype", "param_offline", "param_rare",)
    inlines = (BaseGameInfoInline, )
    filter_horizontal = ('similarcasino', 'othercasino', )
    ordering = ("enabled", )
    save_on_top = True
    inlines_formsets_pages = (
        (_(u"Параграфы"), "paragraphs", {"models" : (BaseGameParagraphInline,)}),
        # (_(u"Скриншоты"), "screenshots", {"models" : (CasinoImageInline,)}),
    )


class GameInfoInline(admin.StackedInline):
    model = GameInfo
    extra = 0


class GameImageInline(admin.TabularInline):
    model = GameImage
    extra = 1


class GameParagraphInline(admin.StackedInline):
    model = GameParagraph
    extra = 0


class GameAdmin(ModifyModelAdmin):
    """
    Admin class for casino game object
    """
    fieldsets = (
        (_(u"Основное инфо"), {'fields': ('name', 'gametype', 'screenshot', 'interfacelangs', 
            'developers', 'maincasino', )}),
        (_(u"Общие параметры"), {'fields': ('param_demo', 'param_sale', 'param_gambling', 'param_mobile', 
            'param_integrity', 'param_shift', 'param_dealer', 'param_multiplayer', 'param_tele',
            'param_jackpot', )}),
        (_(u"Параметры слотов"), {'fields': ('param_numberlines', 'param_numberdrums', )}),
        (_(u"Параметры рулетки"), {'fields': ('param_minbet', 'param_maxbet', 'param_ratio', )}),
        (_(u"Сортировка"), {'fields': ('order_hand', 'order_hand_date', )}),
        (_(u"Настройки Flash"), {'fields': ('flash_width', 'flash_height', 'flash_enabled', 
            'flash_inframe', )}),
    )
    search_fields = ("name",  )
    list_display = ("morelinks", "name", "gametype", "enabled", )
    list_display_links = ("name",)
    list_filter = ("developers", "maincasino", "enabled", "gametype", "interfacelangs", )
    # list_select_related = ("maincasino",)
    inlines = (GameInfoInline, GameImageInline, ) #GameToCasinoInline,
    filter_horizontal = ('developers', 'interfacelangs', )
    ordering = ("enabled", )
    save_on_top = True
    inlines_formsets_pages = (
        (_(u"Параграфы"), "paragraphs", {"models" : (GameParagraphInline,)}),
        # (_(u"Скриншоты"), "screenshots", {"models" : (CasinoImageInline,)}),
    )


admin.site.register(Developer)
admin.site.register(ParagraphCategory)
admin.site.register(BaseGame, BaseGameAdmin)
admin.site.register(Casino, CasinoAdmin)
admin.site.register(Game, GameAdmin)
