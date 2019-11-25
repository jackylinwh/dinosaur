from django.contrib import admin

# Register your models here.
from django import forms
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from blog.models import Article, BlogSettings, BlogConfig


class ArticleAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'is_article', 'parent']

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].queryset = Article.objects.filter(level__lte=1, is_category=True)
        form.base_fields['summary'] = forms.CharField(widget=forms.Textarea)
        return form

    def indented_title(self, item):
        """
        Generate a short title for an object, indent it depending on
        the object's depth in the hierarchy.
        """
        color = "color:green;" if item.is_article else None
        return format_html(
            '<div style="text-indent:{}px;{}">{}</div>',
            item._mpttfield('level') * self.mptt_level_indent,
            color,
            item,
        )


class BlogSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return BlogSettings.objects.count() == 0


class BlogConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'value', 'value_type', 'desc']

admin.site.register(Article, ArticleAdmin)
#admin.site.register(BlogSettings, BlogSettingsAdmin)
admin.site.register(BlogConfig, BlogConfigAdmin)