#coding: utf-8
# from common.models import Language, PaymentSystem
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
# from ormcache.models import CachedModel
from utilites.funcs import easy_upload_path, make_upload_path


PARAM_VALUES = ((-1, _(u"не определено"),), (0, _(u"нет"),), (1, _(u"да"),), )


class Country(models.Model):
    """
    Country model. Need for casino
    """
    UPLOAD_DIR = "country"
    name = models.CharField(_(u"Название"), max_length=200)
    code = models.CharField(_(u"Код"), max_length=50, help_text=_("ru, en, fr и т.п."))
    flag = models.ImageField(_(u"Флаг"), upload_to=easy_upload_path, blank=True)

    def __unicode__(self):
        """
        Object string representation
        """
        return self.name

    class Meta:
        verbose_name = _(u"Страна")
        verbose_name_plural = _(u"Страны")


class ParameterGroup(models.Model):
    """
    List of parameter groups
    """
    name = models.CharField(_(u"Название"), max_length=200)
    description = models.TextField(_(u"Описание"), blank=True)
    meta = models.BooleanField(_(u"Meta"))
    order = models.SmallIntegerField(_(u"Порядок"), default=0)

    def __unicode__(self):
        """
        Object string representation
        """
        return self.name

    class Meta:
        verbose_name = _(u"Группа параметров")
        verbose_name_plural = _(u"Группы параметров")


class Parameter(models.Model):
    """
    Casino parameters
    """
    TYPES = ((1, "label",), (2, "image",), (3, "digit",), (4, "text",), )
    group = models.ForeignKey(ParameterGroup, verbose_name=_(u"Группа параметра"))
    name = models.CharField(_(u"Название"), max_length=200)
    order = models.SmallIntegerField(_(u"Порядок"), default=0)
    type = models.SmallIntegerField(_(u"Тип параметра"), choices=TYPES, default=1)
    description = models.TextField(_(u"Описание"), blank=True)
    view_description = models.TextField(_(u"View Описание"), blank=True)
    min = models.SmallIntegerField(_(u"Min"), blank=True, default=0)
    max = models.SmallIntegerField(_(u"Max"), blank=True, default=0)
    percent = models.IntegerField(_(u"Percent"), blank=True, default=0)
    basic = models.BooleanField(_(u"Basic"))
    type_casinos = models.BooleanField(_(u"Тип казино"))
    type_roulettes = models.BooleanField(_(u"Тип рулетка"))
    type_pokers = models.BooleanField(_(u"Тип покер"))
    managers_editable = models.BooleanField(_(u"Редактируемо менеджерами"))
    visible_main = models.BooleanField(_(u"visible main"))
    visible_info = models.BooleanField(_(u"visible info"))
    visible_compare = models.BooleanField(_(u"isible cmpare"))
    faq = models.TextField(_(u"FAQ"), blank=True)
    faq_managers = models.TextField(_(u"FAQ для менеджеров"), blank=True)

    def __unicode__(self):
        """
        Object string representation
        """
        return self.name

    class Meta:
        ordering = ["group", "order"]
        verbose_name = _(u"Параметр")
        verbose_name_plural = _(u"Параметры")



class Casino(models.Model):
    """
    Casino object model
    """
    UPLOAD_DIR = "casino"
    user = models.ForeignKey(User, verbose_name=_(u"Менеджер"))
    country = models.ForeignKey(Country, verbose_name=_(u"Страна"), null=True, blank=True)
    parameters = models.ManyToManyField(Parameter, verbose_name=_(u"Параметры"), blank=True, \
        through="old_site.ParameterToCasino")
    name = models.CharField(_(u"Название"), max_length=255)
    ru_name = models.CharField(_(u"RU"), max_length=255, blank=True)
    logo = models.ImageField(upload_to=make_upload_path, verbose_name=_(u"Логотип"))
    domain = models.URLField(_(u"Домен"))
    email = models.EmailField(_(u"E-mail"), blank=True)
    path = models.TextField(_(u"Ссылка или рефер"), max_length=200, blank=True)
    roulettes = models.BooleanField(_(u"Рулетки"))
    pokerrooms = models.BooleanField(_(u"Покер румы"))
    ready = models.BooleanField(_(u"Наличные"))
    accept = models.BooleanField(_(u"Принять"))
    sell = models.BooleanField(_(u"Отдать"))
    otstoy = models.BooleanField(_(u"Отстой"))
    otstoy_desc = models.TextField(_(u"Описание отстоя"), blank=True)
    max_show_slots = models.IntegerField(_(u"Слоты"), blank=True, default=1000)
    # order_google = models.IntegerField(_(u"Сортировка по google"), default=0, blank=True)
    rating = models.FloatField(_(u"Рейтинг"), default=0, blank=True)
    description = models.TextField(_(u"Описание"), blank=True)
    article = models.TextField(_(u"Статья"))
    comment = models.TextField(_(u"Комментарий"),blank=True)
    enabled = models.BooleanField(_(u"Показывать на сайте"), default=False)

    def __unicode__(self):
        """
        Object string representation
        """
        return self.name

    def get_url(self):
        """
        Get URL human title like http://urlfield/
        """
        url = self.domain if -1 == self.domain.find("http://") else self.domain[7:]
        if -1 != url.find("/"):
            url = url[:url.find("/")]
        return "http://%s" % url


    class Meta:
        verbose_name = _(u"Казино")
        verbose_name_plural = _(u"Казино")


class CasinoScreenshot(models.Model):
    """
    Screenshots for casino
    """
    TYPES = ((1, _(u"Игры"),), (2, _(u"Личный кабинет"),), (3, _(u"Сайт"),), (4, _(u"Прочее"),), )
    UPLOAD_DIR = "casino"
    casino = models.ForeignKey(Casino)
    name = models.CharField(_(u"Название"), max_length=200)
    image = models.ImageField(upload_to=make_upload_path, verbose_name=_(u"Изображение"))
    type = models.SmallIntegerField(_(u"Тип скриншота"), choices=TYPES)

    def __unicode__(self):
        """
        Object string representation
        """
        return self.name

    class Meta:
        verbose_name = _(u"Скриншот казино")
        verbose_name_plural = _(u"Скриншоты казино")


class CasinoArticle(models.Model):
    """
    Model of casino articles. Show on casino page.
    """
    TYPES = ((1, _(u""),), (2, _(u""),), (3, _(u"Акции"),), (4, _(u"Новости"),), )
    casino = models.ForeignKey(Casino)
    owner_id = models.SmallIntegerField(_(u"Автор"), default=0)
    type = models.SmallIntegerField(_(u"Тип статьи"), choices=TYPES)
    title = models.CharField(_(u"Заголовок"), max_length=255)
    text = models.TextField(_(u"Текст"))
    date = models.DateTimeField(_(u"Дата публикации"))

    def __unicode__(self):
        """
        Object string representation
        """
        return self.title

    class Meta:
        ordering = ["date"]
        verbose_name = _(u"Статья о казино")
        verbose_name_plural = _(u"Статьи о казино")


class ParameterToCasino(models.Model):
    """
    Parameters to casino through model
    """
    # manager = models.ForeignKey(User, verbose_name=_(u"Менеджер"), null=True)
    manager_id = models.IntegerField(_(u"Менеджер"))
    parameter = models.ForeignKey(Parameter, verbose_name=_(u"Параметр"))
    casino = models.ForeignKey(Casino, verbose_name=_(u"Казино"))
    # value = models.CharField(_(u"Значение"), max_length=1000)
    value = models.TextField(_(u"Значение"))
    comment = models.TextField(_(u"Комментарий"))
    author = models.IntegerField(_(u"Автор"))
    # select = models.SmallIntegerField(_(u"Выбор из списка"))
    # boolean = models.SmallIntegerField(_(u"да/нет"), choices=PARAM_VALUES, default=-1)
    # string = models.CharField(_(u"Другое значение"), max_length=255, blank=True)

    def a__init__(self, *args, **kwargs):
        """
        Init fields types
        """
        self._meta.fields[3]._choices = PARAM_VALUES
        # self._meta.fields[3] = models.CharField(_(u"Значение"), max_length=255)
        a = self._meta.fields
        aa = self._meta.fields[3].choices
        # assert 0
        # if self.parameter_id:
            # print self.parameter.description
        super(ParameterToCasino, self).__init__(*args, **kwargs)
        # print self.parameter.description


    class Meta:
        unique_together = ("parameter", "casino", )
        verbose_name = _(u"Параметр казино")
        verbose_name_plural = _(u"Параметры казино")


class CasinoParameterVote(models.Model):
    """
    Votes for casino parameter
    """
    parameter = models.ForeignKey(Parameter, verbose_name=_(u"Параметр"))
    casino = models.ForeignKey(Casino, verbose_name=_(u"Казино"))
    value = models.BooleanField(_(u"Положительный голос"))
    ip = models.IPAddressField(_(u"IP"))
    user_agent = models.CharField(_(u"User Agent"), max_length=255)
    browser = models.CharField(_(u"Браузер"), max_length=150, blank=True)
    os = models.CharField(_(u"ОС"), max_length=150, blank=True)
    comment = models.TextField(_(u"Комментарий"), blank=True)
    date = models.DateTimeField(_(u"Дата"), auto_now_add=True)

    def __unicode__(self):
        """
        Object string representation
        """
        return self.ip

    class Meta:
        verbose_name = _(u"Отзыв о параметре")
        verbose_name_plural = _(u"Отзывы о параметрах")

