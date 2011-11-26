#coding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from utilites.funcs import easy_upload_path


class Language(models.Model):
    """
    Language model. Need for all text content of site
    """
    code = models.CharField(_(u"Код языка"), max_length=10, unique=True)
    name = models.CharField(_(u"Название"), max_length=100)

    def __unicode__(self):
        """
        Get name of language
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
        Printable view for object
        """
        return self.name

    class Meta:
        verbose_name = _(u"Платежная система")
        verbose_name_plural = _(u"Платежные системы")
