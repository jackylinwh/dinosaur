from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from tutorials.models import Topic, Tag


# Register your models here.


class TopicAdmin(MPTTModelAdmin):
    list_display = ['title', 'is_article', 'parent']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Tag, TagAdmin)
