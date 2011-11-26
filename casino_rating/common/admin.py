#coding: utf-8
from django.contrib import admin
from common.models import Language, PaymentSystem


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',)


class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Language, LanguageAdmin)
admin.site.register(PaymentSystem, PaymentSystemAdmin)
