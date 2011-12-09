#coding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from utilites.funcs import easy_upload_path
# from versioner.models import Versioner


class TestModel(models.Model):#Versioner):
    """
    Test model for version control
    """
    STATUSES = ((1, _(u"Новый"),), (2, _(u"Не новый"),), (3, _(u"Старый"),), )
    name = models.CharField(_(u"Название"), max_length=100)
    text = models.TextField(_(u"Текст"))
    value = models.IntegerField(_(u"Число"))
    status = models.IntegerField(_(u"Статус"), choices=STATUSES)

    def __unicode__(self):
        """
        Returns an unicode representation.
        """
        return self.name

    class Meta:
        verbose_name = _(u"Тест")
        verbose_name_plural = _(u"Тест")


class Language(models.Model):
    """
    Language model. Need for all text content of site
    """
    code = models.CharField(_(u"Код языка"), max_length=10, unique=True)
    name = models.CharField(_(u"Название"), max_length=100)

    def __unicode__(self):
        """
        Returns an unicode representation.
        """
        return self.name

    class Meta:
        verbose_name = _(u"Язык")
        verbose_name_plural = _(u"Языки")


class PaymentSystem(models.Model):
    """
    Payment system model. It`s need for casino model
    """
    UPLOAD_DIR = "payments"
    name = models.CharField(_(u"Название системы"), max_length=250, unique=True)
    icon = models.ImageField(upload_to=easy_upload_path, verbose_name=_(u"Иконка"))
    text = models.TextField(_(u"Текст о платежке"), blank=True)

    def __unicode__(self):
        """
        Returns an unicode representation.
        """
        return self.name

    class Meta:
        verbose_name = _(u"Платежная система")
        verbose_name_plural = _(u"Платежные системы")
