from django.contrib import admin
from django.contrib.admin.options import IncorrectLookupParameters
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_text
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter
from mptt.forms import TreeNodeChoiceField

from tutorials.models import Topic, Tag, Article


class TopicAdmin(MPTTModelAdmin):
    list_display = ['title', 'is_article', 'parent']

    def get_form(self, request, obj=None, **kwargs):
        form = super(TopicAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].queryset = Topic.objects.filter(level__lte=1, is_article=False)
        return form


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
    filter_horizontal = ('tags',)
    list_filter = (
        ('topic', TreeRelatedFieldListFilter),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['topic'] = TreeNodeChoiceField(queryset=Topic.objects.all())
        return form


admin.site.register(Topic, TopicAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
