#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: context_processors.py
@time: 2016/11/6 下午4:23
"""

from datetime import datetime
import logging

from blog.models import BlogSettings, BlogConfig

logger = logging.getLogger(__name__)


def config_processor(requests):
    configs = {}
    models = BlogConfig.objects.all()
    if len(models) == 0:
        BlogConfig.insert_default_config()
        models = BlogConfig.objects.all()
    for item in models:
        configs[item.key] = item.get_value()
    return configs


def seo_processor(requests):
    key = 'seo_processor'
    value = None  # cache.get(key)
    if value:
        return value
    else:
        logger.info('set processor cache.')
        setting = BlogSettings.objects.first()
        if not setting:
            setting = BlogSettings(sitename='site1')
            setting.save()
        value = {
            'SITE_NAME': setting.sitename,
            'SHOW_GOOGLE_ADSENSE': setting.show_google_adsense,
            'GOOGLE_ADSENSE_CODES': setting.google_adsense_codes,
            'SITE_SEO_DESCRIPTION': setting.site_seo_description,
            'SITE_DESCRIPTION': setting.site_description,
            'SITE_KEYWORDS': setting.site_keywords,
            'SITE_BASE_URL': requests.scheme + '://' + requests.get_host() + '/',
            'ARTICLE_SUB_LENGTH': setting.article_sub_length,
            # 'nav_category_list': Category.objects.all(),
            # 'nav_pages': Article.objects.filter(type='p', status='p'),
            'OPEN_SITE_COMMENT': setting.open_site_comment,
            'BEIAN_CODE': setting.beiancode,
            'ANALYTICS_CODE': setting.analyticscode,
            "BEIAN_CODE_GONGAN": setting.gongan_beiancode,
            "SHOW_GONGAN_CODE": setting.show_gongan_code,
            "CURRENT_YEAR": datetime.now().year

        }
        # cache.set(key, value, 60 * 60 * 10)
        return value
