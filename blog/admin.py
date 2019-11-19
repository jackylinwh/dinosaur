from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from blog.models import Article


class ArticleAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'color_title', 'is_article', 'index', 'parent']

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].queryset = Article.objects.filter(level__lte=1, is_article=False)
        return form

admin.site.register(Article, ArticleAdmin)