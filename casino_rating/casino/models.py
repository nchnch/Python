#coding: utf-8
from common.models import Language, PaymentSystem
from django.db import models
from django.utils.translation import ugettext as _
# from ormcache.models import CachedModel
from utilites.funcs import easy_upload_path, make_upload_path


PARAM_VALUES = ((-1, _(u"не определено"),), (0, _(u"нет"),), (1, _(u"да"),), )


class ParagraphCategory(models.Model):
    """
    Category class for text paragraphs for casino and games.
    """
    name = models.CharField(_(u"Название"), max_length=200)

    def __unicode__(self):
        """
        Printable view of object
        """
        return self.name

    class Meta:
        verbose_name = _(u"Категория абзаца")
        verbose_name_plural = _(u"Категории абзацев")


class AbstractParagraph(models.Model):
    """
    Class of text paragraphs for casino and games.
    Need for add comments to each block of text
    """
    lang = models.ForeignKey(Language, verbose_name=_(u"Язык"))
    category = models.ForeignKey(ParagraphCategory, verbose_name=_(u"Категория абзаца"))
    text = models.TextField(_(u"Текст"))

    def __unicode__(self):
        """
        Printable view of object
        """
        return unicode(self.category)

    class Meta:
        abstract = True


class Developer(models.Model):
    """
    Soft developers model. Need for slots and casino
    """
    UPLOAD_DIR = "developers"
    name = models.CharField(_(u"Название"), max_length=200)
    logo = models.ImageField(upload_to=easy_upload_path, verbose_name=_(u"Логотип"))
    old_id = models.IntegerField(_(u"OLDID"), default=0, blank=True)

    def __unicode__(self):
        """
        Printable view of object
        """
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _(u"Разработчик")
        verbose_name_plural = _(u"Разработчики")


class Casino(models.Model):
    """
    Casino item model
    """
    STATUSES = ((1, _(u"рабочее казино"),), (2, _(u"казино закрылось"),), (3, _(u"казино не работает"),), )
    RELATIONS = ((1, _(u"не определено"),), (2, _(u"особо доверенное"),), (3, _(u"сомнительное"),), )
    developers = models.ManyToManyField(Developer, verbose_name=_(u"Разработчики"), blank=False) #get list from parameters
    paymentsystems = models.ManyToManyField(PaymentSystem, verbose_name=_(u"Платежные системы"), blank=False, through='casino.CasinoToPaymentSystem') #create type of paymenttype
    name = models.CharField(_(u"Название"), max_length=200)#, unique=True
    similar_sale = models.BooleanField(_(u"Есть ли похожее на продажу")) #new
    domain = models.URLField(_(u"Домен"))
    urlkey = models.SlugField(_(u"ЧПУ ссылка на инфо"))#, unique=True
    relation = models.SmallIntegerField(_(u"Отношения с казино"), choices=RELATIONS, default=1) #new
    status = models.SmallIntegerField(_(u"Статус казино"), choices=STATUSES, default=1) #new
    link_similar_sale = models.URLField(_(u"Ссылка на купить похожее казино")) #new
    param_mobile = models.SmallIntegerField(_(u"Мобильная версия"), help_text="", choices=PARAM_VALUES, default=-1)
    param_browser = models.SmallIntegerField(_(u"Браузерная версия"), choices=PARAM_VALUES, default=-1)
    param_download = models.SmallIntegerField(_(u"Скачиваемая версия"), choices=PARAM_VALUES, default=-1)
    param_audited = models.SmallIntegerField(_(u"Проходит аудит"), choices=PARAM_VALUES, default=-1)
    param_integrity = models.SmallIntegerField(_(u"Контроль честности"), choices=PARAM_VALUES, default=-1) #cached from games
    param_license = models.SmallIntegerField(_(u"Лицензия"), choices=PARAM_VALUES, default=-1)
    param_shift = models.SmallIntegerField(_(u"Контроль честности со сдвигом"), choices=PARAM_VALUES, default=-1)#cached from games
    param_jackpot = models.SmallIntegerField(_(u"Джекпот"), choices=PARAM_VALUES, default=-1)
    param_dealer = models.SmallIntegerField(_(u"Игры с живым диллером"), choices=PARAM_VALUES, default=-1) #cached from games
    param_multiplayer = models.SmallIntegerField(_(u"Мультиплеерные игры"), choices=PARAM_VALUES, default=-1) #cached from games
    param_tournaments = models.SmallIntegerField(_(u"Турниры"), choices=PARAM_VALUES, default=-1)
    param_nodepositbonus = models.SmallIntegerField(_(u"Бездепозитный бонус"), choices=PARAM_VALUES, default=-1)
    order_google = models.IntegerField(_(u"Сортировка по google"), default=0, blank=True)
    order_hand = models.IntegerField(_(u"Ручная сортировка"), default=0, blank=True)
    order_hand_date = models.DateTimeField(_(u"Окончание ручной сортировки"), blank=True, null=True)
    enabled = models.BooleanField(_(u"Показывать на сайте"), default=False)
    old_id = models.IntegerField(_(u"OLDID"), default=0, blank=True)

    def morelinks(self):
        """
        Additional link for each casino record
        """
        return u"""<a href="%(id)s/screenshots/">Скриншоты</a><br />
            <a href="%(id)s/paragraphs/">Параграфы</a><br />
            <a href="%(id)s/articles/">Статьи</a>""" % {"id" : self.id}
    morelinks.short_description = u"-"
    morelinks.allow_tags = True    

    def __unicode__(self):
        """
        Get name of the entry
        """
        return self.name

    class Meta:
        ordering = ["name"]
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
    # text = models.TextField(_(u"Статья главная"))

    def __unicode__(self):
        """
        Get name of the entry
        """
        return "%s [%s]" % (self.name, unicode(self.lang),)

    class Meta:
        verbose_name = _(u"Языкозависимые поля казино")
        verbose_name_plural = _(u"Языкозависимые поля казино")


class CasinoParagraph(AbstractParagraph):
    """
    Paragraphs for casino
    """
    casino = models.ForeignKey(Casino, verbose_name=_(u"Казино"))

    class Meta:
        unique_together = ["casino", "category", "lang"]
        verbose_name = _(u"Абазац текста")
        verbose_name_plural = _(u"Абзацы текста")


class CasinoArticle(models.Model):
    """
    Articles for casino. Simple text model
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


class CasinoToPaymentSystem(models.Model):
    """
    Casino to paymentsystem through model
    """
    TYPES = ((1, _(u"ввод"),), (2, _(u"вывод"),), (3, _(u"оба направления"),), )
    casino = models.ForeignKey(Casino, verbose_name=_(u"Казино"))
    paymentsystem = models.ForeignKey(PaymentSystem, verbose_name=_(u"Платежная система"))
    type = models.SmallIntegerField(_(u"Тип платежки"), choices=TYPES, default=3) #new

    def __unicode__(self):
        return unicode(self.paymentsystem)

    class Meta:
        unique_together = ("paymentsystem", "casino", )
        verbose_name = _(u"Связка казино с платежной системой")
        verbose_name_plural = _(u"Связки казино с платежной системой")


class BaseGame(models.Model):
    """
    Base (parent) class of games
    """
    UPLOAD_DIR = "slots"
    TYPES = ((1, _(u"Карточные"),), (2, _(u"Гонки"),), (3, _(u"Настольные"),),)
    othercasino = models.ManyToManyField(Casino, verbose_name=_(u"Казино где есть игра"), blank=True, related_name="base_games")
    similarcasino = models.ManyToManyField(Casino, verbose_name=_(u"Казино с похожими играми"), blank=True, related_name="base_similargames")
    name = models.CharField(_(u"Название"), max_length=250, unique=True)
    gametype = models.SmallIntegerField(_(u"Тип игры"), choices=TYPES)
    screenshot = models.ImageField(upload_to=make_upload_path, verbose_name=_(u"Скриншот для главной"))
    rating = models.IntegerField(_(u"Рейтинг показа"), blank=True, default=0)
    param_offline = models.SmallIntegerField(_(u"Есть offline аналог"), choices=PARAM_VALUES, default=-1)
    param_rare = models.SmallIntegerField(_(u"Редкая"), choices=PARAM_VALUES, default=-1)
    param_numberlines = models.SmallIntegerField(_(u"Количество линий"), blank=True, null=True)
    param_numberdrums = models.SmallIntegerField(_(u"Количество барабанов"), blank=True, null=True)
    order_google = models.IntegerField(_(u"Сортировка по google"), default=0, blank=True)
    order_hand = models.IntegerField(_(u"Ручная сортировка"), default=0, blank=True)
    order_hand_date = models.DateTimeField(_(u"Окончание ручной сортировки"), blank=True, null=True)
    enabled = models.BooleanField(_(u"Показывать на сайте"), default=False)

    def morelinks(self):
        """
        Additional link for each casino record
        """
        return u"""<a href="%(id)s/paragraphs/">Параграфы</a>""" % {"id" : self.id}
    morelinks.short_description = u"-"
    morelinks.allow_tags = True    

    def __unicode__(self):
        """
        Get name of the entry
        """
        return self.name

    class Meta:
        # ordering = ["name"]
        verbose_name = _(u"Основная игра")
        verbose_name_plural = _(u"Основные игры")


class BaseGameInfo(models.Model):
    """
    Language-depended fields for base game
    """
    game = models.ForeignKey(BaseGame)
    lang = models.ForeignKey(Language, verbose_name=_(u"Язык"))
    name = models.CharField(_(u"Название"), max_length=250)
    urlkey = models.SlugField(_(u"URL ключ игры"), unique=True, null=True)
    text = models.TextField(_(u"Статья"))
    tags_picture = models.CharField(_(u"Теги картинки на барабанах"), max_length=200, blank=True)
    tags_theme = models.CharField(_(u"Теги темы"), max_length=200, blank=True)
    tags_name = models.CharField(_(u"Теги названия"), max_length=200, blank=True)

    def __unicode__(self):
        """
        Get name of the entry
        """
        return self.name

    class Meta:
        # ordering = ["name"]
        verbose_name = _(u"Информация основной игры")
        verbose_name_plural = _(u"Информация основной игры")


class BaseGameParagraph(AbstractParagraph):
    """
    Text paragraphs for games
    """
    game = models.ForeignKey(BaseGame, verbose_name=_(u"Игра"))

    class Meta:
        unique_together = ["game", "category", "lang"]
        verbose_name = _(u"Абазац текста")
        verbose_name_plural = _(u"Абзацы текста")


class Game(models.Model):
    """
    Casino game object
    """
    UPLOAD_DIR = "slots"
    TYPES = ((1, _(u"Слоты"),), (2, _(u"Рулетка"),),)
    DEMOS = ((0, _(u"неизвестно"),), (1, _(u"с регистрацией"),), (2, _(u"без регистрации у нас на сайте"),), (3, _(u"нет"),),)
    parent = models.ForeignKey(BaseGame, verbose_name=_(u"Главная игра"), null=True)
    interfacelangs = models.ManyToManyField(Language, verbose_name=_(u"Язык интерфейса"))
    developers = models.ManyToManyField(Developer, verbose_name=_(u"Разработчики"))
    # interface_lang = models.ForeignKey(Language, verbose_name=_(u"Язык интерфейса"))
    maincasino = models.ForeignKey(Casino, verbose_name=_(u"Главное казино"))
    othercasino = models.ManyToManyField(Casino, verbose_name=_(u"Казино где есть игра"), blank=True, \
        related_name="games", through="casino.GameToCasino")
    name = models.CharField(_(u"Название"), max_length=250)#, null=True, unique=True
    gametype = models.SmallIntegerField(_(u"Тип игры"), choices=TYPES)
    screenshot = models.ImageField(upload_to=make_upload_path, verbose_name=_(u"Скриншот для главной"))
    order_google = models.IntegerField(_(u"Сортировка по google"), default=0, blank=True)
    order_hand = models.IntegerField(_(u"Ручная сортировка"), default=0, blank=True)
    order_hand_date = models.DateTimeField(_(u"Окончание ручной сортировки"), blank=True, null=True)
    param_demo = models.SmallIntegerField(_(u"Демо"), choices=DEMOS, default=0)
    param_sale = models.SmallIntegerField(_(u"Продается"), choices=PARAM_VALUES, default=-1)
    param_gambling = models.SmallIntegerField(_(u"Азартная"), choices=PARAM_VALUES, default=-1)
    # param_offline = models.SmallIntegerField(_(u"Есть offline аналог"), choices=PARAM_VALUES, default=-1)
    param_mobile = models.SmallIntegerField(_(u"Мобильная версия"), choices=PARAM_VALUES, default=-1)
    param_integrity = models.SmallIntegerField(_(u"Контроль честности"), choices=PARAM_VALUES, default=-1)
    param_shift = models.SmallIntegerField(_(u"Контроль честности со сдвигом"), choices=PARAM_VALUES, default=-1)
    param_dealer = models.SmallIntegerField(_(u"Игра с живым диллером"), choices=PARAM_VALUES, default=-1)
    param_multiplayer = models.SmallIntegerField(_(u"Мультиплеерная игра"), choices=PARAM_VALUES, default=-1)
    param_tele = models.SmallIntegerField(_(u"Телеигра"), choices=PARAM_VALUES, default=-1)
    param_jackpot = models.SmallIntegerField(_(u"Джекпот"), choices=PARAM_VALUES, default=-1)
    param_numberlines = models.SmallIntegerField(_(u"Количество линий"), blank=True, null=True)
    param_numberdrums = models.SmallIntegerField(_(u"Количество барабанов"), blank=True, null=True)
    param_minbet = models.IntegerField(_(u"Минимальная ставка"), blank=True, null=True)
    param_maxbet = models.IntegerField(_(u"Максимальная ставка"), blank=True, null=True)
    param_ratio = models.IntegerField(_(u"Соотношение"), blank=True, null=True)
    flash_width = models.IntegerField(_(u"Ширина флешки"), default=0, blank=True)
    flash_height = models.IntegerField(_(u"Высота флешки"), default=0, blank=True)
    flash_enabled = models.BooleanField(_(u"Показывать"), default=True)
    flash_inframe = models.BooleanField(_(u"Открывать во фрейме"), default=True)
    enabled = models.BooleanField(_(u"Показывать на сайте"), default=False)
    old_id = models.IntegerField(_(u"OLDID"), default=0, blank=True)

    def morelinks(self):
        """
        Additional link for each casino record
        """
        return u"""<a href="%(id)s/paragraphs/">Параграфы</a>""" % {"id" : self.id}
    morelinks.short_description = u"-"
    morelinks.allow_tags = True    

    def __unicode__(self):
        """
        Get name of the entry
        """
        return self.name

    class Meta:
        # ordering = ["name"]
        verbose_name = _(u"Игра")
        verbose_name_plural = _(u"Игры")


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
    name = models.CharField(_(u"Название"), max_length=250)
    urlkey = models.SlugField(_(u"URL на инфо"), unique=True, null=True)
    # text = models.TextField(_(u"Статья"))
    selltext = models.TextField(_(u"Статья (для купить игру)"))
    tags_picture = models.CharField(_(u"Теги картинки на барабанах"), max_length=200, blank=True)
    tags_theme = models.CharField(_(u"Теги темы"), max_length=200, blank=True)
    tags_name = models.CharField(_(u"Теги названия"), max_length=200, blank=True)
    url_buy_our = models.SlugField(_(u"URL купить у нас"), unique=True, null=True, blank=True)
    url_play_our = models.SlugField(_(u"URL играть без регистрации у нас"), unique=True, null=True, blank=True)
    url_flash = models.URLField(_(u"URL на флешку"), unique=True, null=True, blank=True)
    url_buy_side = models.URLField(_(u"URL купить у них"), unique=True, null=True, blank=True)
    # url_play_side = models.URLField(_(u"URL играть без регистрации у них"), null=True, blank=True) #unique=True, 
    url_play_side = models.TextField(_(u"URL играть без регистрации у них"), null=True, blank=True) #unique=True, 

    def __unicode__(self):
        """
        Printable view of object
        """
        return self.name

    class Meta:
        verbose_name = _(u"Языковые поля")
        verbose_name_plural = _(u"Языковые поля")


class GameParagraph(AbstractParagraph):
    """
    Text paragraphs for games
    """
    game = models.ForeignKey(Game, verbose_name=_(u"Игра"))

    class Meta:
        unique_together = ["game", "category", "lang"]
        verbose_name = _(u"Абазац текста")
        verbose_name_plural = _(u"Абзацы текста")


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

