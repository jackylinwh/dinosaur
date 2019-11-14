from abc import abstractmethod
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from mdeditor.fields import MDTextField


class Topic(MPTTModel):
    title = models.CharField(max_length=64, verbose_name='标题')
    is_article = models.BooleanField(default=False)
    content = MDTextField(verbose_name='内容', null=True, blank=True)
    cover = models.ImageField(verbose_name='封面', null=True, blank=True, upload_to='images')
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)
    index = models.IntegerField()
    parent = TreeForeignKey('self', verbose_name='父级分类', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['index']
        verbose_name = "主题/文章"
        verbose_name_plural = "主题/文章"


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
