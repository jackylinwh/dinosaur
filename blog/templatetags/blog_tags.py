from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite',
                                                         'markdown.extensions.toc', ], safe_mode=True,
                                       enable_attributes=False))
