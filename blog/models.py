from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html
from django.utils.timezone import now
from mdeditor.fields import MDTextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Article(MPTTModel):
    ARTICLE_STATUS = (
        ('p', '发布'),
        ('d', '草稿')
    )
    title = models.CharField(max_length=64, verbose_name='标题')
    is_article = models.BooleanField(default=True, verbose_name='是否文章')
    is_category = models.BooleanField(default=False, verbose_name='是否分类目录')  # 允许一篇文章有子节点，即作为一个分类
    content = MDTextField(verbose_name='内容', null=True, blank=True)
    cover = models.ImageField(verbose_name='封面', null=True, blank=True, upload_to='images')
    summary = models.CharField(max_length=200, verbose_name='摘要', null=True, blank=True)
    status = models.CharField(max_length=1, verbose_name="状态", choices=ARTICLE_STATUS, default='p')
    pub_date = models.DateTimeField(verbose_name="发表日期", default=now)
    views = models.PositiveIntegerField('浏览量', default=0)
    parent = TreeForeignKey('self', verbose_name='父级目录', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    def first_article(self):
        articles = self.get_root().get_descendants()
        for article in articles:
            if article.is_article and article.status == 'p':
                return article
        return None

    def __str__(self):
        return self.title

    def color_title(self):
        if self.is_article:
            title = "<span style='color:lime;'>{0}</span>".format(self.title)
            return format_html(title)
        return ""

    def next(self):
        root = self.get_root();
        articles = root.get_descendants()
        found = False
        for article in articles:
            if found and article.is_article and article.status == 'p':
                return article
            if article.id == self.id:
                found = True
        return None

    def prev(self):
        articles = self.get_root().get_descendants()
        p = None
        for article in articles:
            if article.id == self.id:
                break
            elif article.is_article and article.status == 'p':
                p = article
        return p

    class Meta:
        verbose_name = "文章/目录"
        verbose_name_plural = "文章/目录"

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    class MPTTMeta:
        pass


class BlogSettings(models.Model):
    '''站点设置 '''
    sitename = models.CharField("网站名称", max_length=200, null=False, blank=False, default='')
    site_description = models.TextField("网站描述", max_length=1000, null=False, blank=False, default='')
    site_seo_description = models.TextField("网站SEO描述", max_length=1000, null=False, blank=False, default='')
    site_keywords = models.TextField("网站关键字", max_length=1000, null=False, blank=False, default='')
    article_sub_length = models.IntegerField("文章摘要长度", default=300)
    sidebar_article_count = models.IntegerField("侧边栏文章数目", default=10)
    sidebar_comment_count = models.IntegerField("侧边栏评论数目", default=5)
    show_google_adsense = models.BooleanField('是否显示谷歌广告', default=False)
    google_adsense_codes = models.TextField('广告内容', max_length=2000, null=True, blank=True, default='')
    open_site_comment = models.BooleanField('是否打开网站评论功能', default=True)
    beiancode = models.CharField('备案号', max_length=2000, null=True, blank=True, default='')
    analyticscode = models.TextField("网站统计代码", max_length=1000, null=True, blank=True, default='')
    show_gongan_code = models.BooleanField('是否显示公安备案号', default=False, null=False)
    gongan_beiancode = models.TextField('公安备案号', max_length=2000, null=True, blank=True, default='')
    resource_path = models.CharField("静态文件保存地址", max_length=300, null=False, default='/var/www/resource/')

    class Meta:
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sitename

    def clean(self):
        if BlogSettings.objects.exclude(id=self.id).count():
            raise ValidationError('只能有一个配置')

    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from DjangoBlog.utils import cache
        cache.clear()
    """


class BlogConfig(models.Model):
    VALUE_TYPE = (
        ('s', "字符串"),
        ('i', "整数"),
        ('d', '小数'),
        ('b', "布尔值")
    )
    name = models.CharField(verbose_name="配置名称", max_length=20, unique=True)
    key = models.CharField(verbose_name="Key", max_length=20, unique=True)
    value = models.CharField(verbose_name="值", max_length=300, blank=True, null=True)
    desc = models.TextField(verbose_name="配置项描述", blank=True, null=True)
    value_type = models.CharField('值类型', max_length=1, choices=VALUE_TYPE, default='s')

    def __str__(self):
        return self.name + " => " + self.value

    def get_value(self):
        if self.value:
            if self.value_type == 'i':
                return int(self.value)
            elif self.value_type == 'b':
                return bool(self.value)
            elif self.value_type == 'd':
                return float(self.value)
            else:
                return self.value
        return None

    @staticmethod
    def insert_default_config():
        BlogConfig(name="Github", key="GITHUB_HOME", value="", desc="Github", value_type="s").save()
        BlogConfig(name='网站名称', key='SITE_NAME', value="", desc="", value_type="s").save()
        BlogConfig(name='网站SEO描述', key='SITE_SEO_DESCRIPTION', value="", desc="", value_type="s").save()
        BlogConfig(name='网站描述', key='SITE_DESCRIPTION', value="", desc="", value_type="s").save()
        BlogConfig(name='网站关键字', key='SITE_KEYWORDS', value="", desc="", value_type="s").save()
        BlogConfig(name='网站URL', key='SITE_BASE_URL', value="", desc="", value_type="s").save()
        BlogConfig(name='文章摘要字数', key='ARTICLE_SUB_LENGTH', value="", desc="", value_type="i").save()
        BlogConfig(name='开启评论', key='OPEN_SITE_COMMENT', value="", desc="", value_type="s").save()
        BlogConfig(name='备案代码', key='BEIAN_CODE', value="", desc="", value_type="s").save()
        BlogConfig(name='统计代码', key='ANALYTICS_CODE', value="", desc="", value_type="s").save()
        BlogConfig(name='公安备案', key="BEIAN_CODE_GONGAN", value="", desc="", value_type="s").save()
        BlogConfig(name='显示公安备案', key="SHOW_GONGAN_CODE", value="", desc="", value_type="b").save()

    class Meta:
        verbose_name = '参数配置'
        verbose_name_plural = verbose_name
