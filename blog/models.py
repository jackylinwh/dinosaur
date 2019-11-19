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
