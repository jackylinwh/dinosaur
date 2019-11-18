from abc import abstractmethod
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from mdeditor.fields import MDTextField
from mptt.utils import previous_current_next


class Topic(MPTTModel):
    title = models.CharField(max_length=64, verbose_name='标题')
    is_article = models.BooleanField(default=False, verbose_name='是否文章')
    cover = models.ImageField(verbose_name='封面', null=True, blank=True, upload_to='images')
    parent = TreeForeignKey('self', verbose_name='父级目录', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "目录"
        verbose_name_plural = "目录"


class Article(models.Model):
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, verbose_name="标题", related_name='content')
    content = MDTextField(verbose_name='内容', null=True, blank=True)
    index = models.IntegerField()
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def title(self):
        return self.__str__();

    def __str__(self):
        return self.topic.title

    class Meta:
        ordering = ['index']
        verbose_name = "文章"
        verbose_name_plural = "文章"


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def __str__(self):
        return self.name

    def get_topic_count(self):
        return Topic.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name
