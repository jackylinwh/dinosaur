from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html
from mdeditor.fields import MDTextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from mptt.utils import previous_current_next


class Article(MPTTModel):
    title = models.CharField(max_length=64, verbose_name='标题')
    is_article = models.BooleanField(default=True, verbose_name='是否文章')
    index = models.IntegerField(verbose_name="序号", default=0)
    content = MDTextField(verbose_name='内容', null=True, blank=True)
    cover = models.ImageField(verbose_name='封面', null=True, blank=True, upload_to='images')
    parent = TreeForeignKey('self', verbose_name='父级目录', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    def first_article(self):
        return self.get_root().get_leafnodes()[0]

    def __str__(self):
        return self.title

    def color_title(self):
        if self.is_article:
            title = "<span style='color:lime;'>[{0}]--{1}".format(self.index, self.title)
            return format_html(title)
        return ""

    def next(self):
        articles = self.get_root().get_leafnodes()
        articles = sorted(articles, key=lambda a: a.index)
        for article in articles:
            if article.index > self.index:
                return article

        return None

    def prev(self):
        articles = self.get_root().get_leafnodes()
        articles = sorted(articles, key=lambda a: a.index)
        p = None
        for article in articles:
            if article.index < self.index:
                p = article
            else:
                break
        return p

    class Meta:
        ordering = ['index']
        verbose_name = "文章/目录"
        verbose_name_plural = "文章/目录"

    class MPTTMeta:
        order_insertion_by = ['index']


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
            raise ValidationError(_('只能有一个配置'))

    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from DjangoBlog.utils import cache
        cache.clear()
    """