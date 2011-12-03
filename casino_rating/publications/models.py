#coding: utf-8
from casino.models import Casino
from common.models import Language
from django.db import models
from django.utils.translation import ugettext as _
# from utilites.funcs import easy_upload_path


class News(models.Model):
    """
    News model. Have some categories
    """
    CATEGORY = ((1, _(u"Общее"),), (2, _(u"Бонусы"),), (3, _(u"Акции"),), (3, _(u"Турниры"),), )
    language = models.ForeignKey(Language, verbose_name=_(u"Язык"))
    casino = models.ForeignKey(Casino, verbose_name=_(u"Относится к казино"))#, blank=True
    urlkey = models.SlugField(_(u"URL ключ"), max_length=250)
    name = models.CharField(_(u"Заголовок новости"), max_length=250)
    category = models.SmallIntegerField(_(u"Категория"), choices=CATEGORY)
    description = models.TextField(_(u"Краткое описание"))
    text = models.TextField(_(u"Текст"))
    date = models.DateTimeField(_(u"Дата публикации"), auto_now_add=True)

    def __unicode__(self):
        """
        Get name of news publication
        """
        return self.name

    class Meta:
        verbose_name = _(u"Новость о казино")
        verbose_name_plural = _(u"Новости о казино")


class Article(models.Model):
    """
    Article model. Simple site text content
    """
    language = models.ForeignKey(Language, verbose_name=_(u"Язык"))
    urlkey = models.SlugField(_(u"URL ключ"), max_length=250)
    name = models.CharField(_(u"Название"), max_length=250)
    description = models.CharField(_(u"Краткое описание"), max_length=250)
    text = models.TextField(_(u"Подробный текст"))
    tags = models.CharField(_(u"Тэги"), max_length=100)
    date = models.DateTimeField(_(u"Дата публикации"), auto_now_add=True)

    def __unicode__(self):
        """
        Get name of article
        """
        return self.name

    class Meta:
        verbose_name = _(u"Статья")
        verbose_name_plural = _(u"Статьи")

