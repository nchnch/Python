#coding: utf-8
from django.contrib import admin
from publications.models import News, Article


class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'language',)
    list_filter = ("category", "language", )
    search_fields = ("name", )
    date_hierarchy = "date"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'language',)


admin.site.register(News, NewsAdmin)
admin.site.register(Article, ArticleAdmin)
