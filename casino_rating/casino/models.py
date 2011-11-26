#coding: utf-8
from common.models import Language, PaymentSystem
from django.db import models
from django.utils.translation import ugettext as _
from utilites.funcs import easy_upload_path, make_upload_path


class Developer(models.Model):
    """
    Soft developers model. Need for slots and casino
    """
    UPLOAD_DIR = "developers"
    name = models.CharField(_(u"Название"), max_length=200)
    logo = models.ImageField(upload_to=easy_upload_path, verbose_name=_(u"Логотип"))

    def __unicode__(self):
        """
        Printable view of object
        """
        return self.name

    class Meta:
        verbose_name = _(u"Разработчик")
        verbose_name_plural = _(u"Разработчики")


class Casino(models.Model):
    """
    Casino item model
    """
    STATUSES = ((1, _(u"рабочее казино"),), (2, _(u"казино закрылось"),), (3, _(u"казино не работает"),), )
    developers = models.ManyToManyField(Developer, verbose_name=_(u"Разработчики"), blank=False)
    paymentsystems = models.ManyToManyField(PaymentSystem, verbose_name=_(u"Платежные системы"), blank=False)
    name = models.CharField(_(u"Название"), max_length=200)
    similar_sale = models.BooleanField(_(u"Есть ли похожее на продажу"))
    domain = models.URLField(_(u"Домен"))
    urlkey = models.SlugField(_(u"Ссылка"))
    status = models.SmallIntegerField(_(u"Статус казино"), choices=STATUSES, default=1)
    link_similar_sale = models.URLField(_(u"Ссылка на купить похожее казино"))
    param_mobile = models.BooleanField(_(u"Мобильная версия"))
    param_browser = models.BooleanField(_(u"Браузерная версия"))
    param_audited = models.BooleanField(_(u"Проходит аудит"))
    param_integrity = models.BooleanField(_(u"Контроль честности"))
    param_license = models.BooleanField(_(u"Лицензия"))
    param_shift = models.BooleanField(_(u"Сдвиг"))
    param_jackpot = models.BooleanField(_(u"Джекпот"))
    param_dealer = models.BooleanField(_(u"Игры с живым диллером"))
    param_multiplayer = models.BooleanField(_(u"Мультиплеерные игры"))
    param_tournaments = models.BooleanField(_(u"Турниры"))
    param_nodepositbonus = models.BooleanField(_(u"Бездепозитный бонус"))
    order_google = models.IntegerField(_(u"Сортировка по google"), default=0, blank=True)
    order_hand = models.IntegerField(_(u"Ручная сортировка"), default=0, blank=True)
    order_hand_date = models.DateTimeField(_(u"Окончание ручной сортировки"), blank=True, null=True)
    enabled = models.BooleanField(_(u"Показывать на сайте"), default=False)

    def __unicode__(self):
        """
        Get name of the entry
        """
        return self.name

    class Meta:
        verbose_name = _(u"Казино")
        verbose_name_plural = _(u"Казино")


class CasinoImage(models.Model):
    """
    Screenshots for casino
    """
    UPLOAD_DIR = "casino"
    casino = models.ForeignKey(Casino)
    lang = models.ForeignKey(Language, verbose_name=_(u"Язык"))
    name = models.CharField(_(u"Название"), max_length=200)
    image = models.ImageField(upload_to=make_upload_path, verbose_name=_(u"Изображение"))

    def __unicode__(self):
        """
        Get name of the screenshot
        """
        return self.name

    class Meta:
        verbose_name = _(u"Скриншот казино")
        verbose_name_plural = _(u"Скриншоты казино")


class CasinoInfo(models.Model):
    """
    Casino language-depended values
    """
    UPLOAD_DIR = "casino"
    casino = models.ForeignKey(Casino, verbose_name=_(u"Казино"))
    lang = models.ForeignKey(Language, verbose_name=_(u"Язык"))
    name = models.CharField(_(u"Название"), max_length=200)
    image = models.ImageField(upload_to=make_upload_path, verbose_name=_(u"Картинка на главную"))
    description = models.TextField(_(u"Короткое описание на главную"))
    purl_main = models.URLField(_(u"Главная"))
    purl_download = models.URLField(_(u"Скачать"), blank=True)
    purl_bonus = models.URLField(_(u"Бонусы"), blank=True)
    text = models.TextField(_(u"Статья главная"))
    # articles = models.ManyToManyField(CasinoArticle, verbose_name=_(u"Статьи остальные"), blank=True)

    def __unicode__(self):
        """
        Get name of the entry
        """
        return self.name

    class Meta:
        verbose_name = _(u"Языкозависимые поля казино")
        verbose_name_plural = _(u"Языкозависимые поля казино")


class CasinoArticle(models.Model):
    """
    Articles for casino. Used like casino text bun need ManyToMany relate
    """
    casino = models.ForeignKey(Casino, verbose_name=_(u"Казино"))
    lang = models.ForeignKey(Language, verbose_name=_(u"Язык"))
    name = models.CharField(_(u"Название статьи"), max_length=250)
    text = models.TextField(_(u"Текст статьи"))

    def __unicode__(self):
        """
        Get title of the article
        """
        return self.name

    class Meta:
        verbose_name = _(u"Статья о казино")
        verbose_name_plural = _(u"Статьи о казино")


class Game(models.Model):
    """
    Casino game object
    """
    UPLOAD_DIR = "slots"
    TYPES = ((1, _(u"first"),), (2, _(u"second"),), (3, _(u"third"),), )
    developers = models.ManyToManyField(Developer, verbose_name=_(u"Разработчики"), blank=False)
    maincasino = models.ForeignKey(Casino, verbose_name=_(u"Главное казино"), blank=False)
    othercasino = models.ManyToManyField(Casino, verbose_name=_(u"Казино где есть игра"), blank=True, \
        related_name="games", through="casino.GameToCasino")
    name = models.CharField(_(u"Название"), max_length=200, unique=True)
    gametype = models.SmallIntegerField(_(u"Тип игры"), choices=TYPES)
    screenshot = models.ImageField(upload_to=make_upload_path, verbose_name=_(u"Скриншот для главной"))
    order_google = models.IntegerField(_(u"Сортировка по google"), default=0, blank=True)
    order_hand = models.IntegerField(_(u"Ручная сортировка"), default=0, blank=True)
    order_hand_date = models.DateTimeField(_(u"Окончание ручной сортировки"), blank=True, null=True)
    param_sale = models.BooleanField(_(u"Продается"))
    param_gambling = models.BooleanField(_(u"Азартная"))
    param_offline = models.BooleanField(_(u"Есть offline аналог"))
    param_mobile = models.BooleanField(_(u"Мобильная версия"))
    param_integrity = models.BooleanField(_(u"Контроль честности"))
    param_jackpot = models.BooleanField(_(u"Джекпот"))
    flash_width = models.IntegerField(_(u"Ширина флешки"), default=0, blank=True)
    flash_height = models.IntegerField(_(u"Высота флешки"), default=0, blank=True)
    flash_enabled = models.BooleanField(_(u"Показывать"), default=True)
    flash_inframe = models.BooleanField(_(u"Открывать во фрейме"), default=True)
    enabled = models.BooleanField(_(u"Показывать на сайте"), default=False)

    def __unicode__(self):
        """
        Get name of the entry
        """
        return self.name


class Slot(Game):
    """
    Slot type of game.
    """
    param_numberlines = models.IntegerField(_(u"Количество линий"), blank=True, null=True)
    param_numberdrums = models.IntegerField(_(u"Количество барабанов"), blank=True, null=True)

    class Meta:
        verbose_name = _(u"Слот")
        verbose_name_plural = _(u"Слоты")


class Roulette(Game):
    """
    Roulette type of game.
    """
    param_minbet = models.IntegerField(_(u"Минимальная ставка"), blank=True, null=True)
    param_maxbet = models.IntegerField(_(u"Максимальная ставка"), blank=True, null=True)
    param_ratio = models.IntegerField(_(u"Соотношение"), blank=True, null=True)

    class Meta:
        verbose_name = _(u"Рулетка")
        verbose_name_plural = _(u"Рулетки")


class GameImage(models.Model):
    """
    Screenshots for games
    """
    UPLOAD_DIR = "slots"
    game = models.ForeignKey(Game)
    lang = models.ForeignKey(Language, verbose_name=_(u"Язык"))
    name = models.CharField(_(u"Название"), max_length=200)
    image = models.ImageField(upload_to=make_upload_path, verbose_name=_(u"Изображение"))

    def __unicode__(self):
        """
        Get name of the entry
        """
        return self.name

    class Meta:
        verbose_name = _(u"Скриншот игры")
        verbose_name_plural = _(u"Скриншоты игры")


class GameInfo(models.Model):
    """
    Language-depended fields for game
    """
    game = models.ForeignKey(Game)
    lang = models.ForeignKey(Language, verbose_name=_(u"Язык"))
    name = models.CharField(_(u"Название"), max_length=200)
    tags_picture = models.CharField(_(u"Теги картинки на барабанах"), max_length=200, blank=True)
    tags_theme = models.CharField(_(u"Теги темы"), max_length=200, blank=True)
    tags_name = models.CharField(_(u"Теги названия"), max_length=200, blank=True)
    text = models.TextField(_(u"Статья"))
    selltext = models.TextField(_(u"Статья (для купить игру)"))
    url_info = models.SlugField(_(u"URL инфо"), unique=True)
    url_buy_our = models.SlugField(_(u"URL купить у нас"), unique=True, null=True, blank=True)
    url_play_our = models.SlugField(_(u"URL играть без регистрации у нас"), unique=True, null=True, blank=True)
    url_flash = models.URLField(_(u"URL на флешку"), unique=True, null=True, blank=True)
    url_buy_side = models.URLField(_(u"URL купить у них"), unique=True, null=True, blank=True)
    url_play_side = models.URLField(_(u"URL играть без регистрации у них"), unique=True, null=True, blank=True)

    def __unicode__(self):
        """
        Printable view of object
        """
        return self.name

    class Meta:
        verbose_name = _(u"Языковые поля")
        verbose_name_plural = _(u"Языковые поля")


class GameToCasino(models.Model):
    """
    Game to casino through model
    """
    game = models.ForeignKey(Game, verbose_name=_(u"Игра"))
    casino = models.ForeignKey(Casino, verbose_name=_(u"Казино"))
    frame_urlkey = models.SlugField(_(u"URL на фрейм"), max_length=200)
    flash_url = models.URLField(_(u"URL на flash во фрейме"), max_length=200)
    main_show = models.BooleanField(_(u"Показывать на главной"))

    class Meta:
        unique_together = ("game", "casino", )
        verbose_name = _(u"Связка игры с казино")
        verbose_name_plural = _(u"Связка игры с казино")

