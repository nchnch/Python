#coding: utf-8
from django.contrib import admin
from common.models import Language, PaymentSystem, TestModel
# from versioner import admin_models as versioner
# from versioner.admin import VersionerAdmin

from reversion.admin import VersionAdmin


class TestModelAdmin(VersionAdmin): #versioner.ModelAdmin, VersionAdmin
    ignore_duplicate_revisions = True
    history_latest_first = True
    list_display = ("name", "status")


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',)


class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Language, LanguageAdmin)
admin.site.register(PaymentSystem, PaymentSystemAdmin)
admin.site.register(TestModel, TestModelAdmin)
